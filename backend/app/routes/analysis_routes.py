import logging
from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.services.bias_detection_service import BiasDetectionService
from app.services.document_parser import DocumentParser
from app.services.auth_service import token_required
from app.models.models import AnalysisResult, Base
from app.config.config import Config
from app.utils.helpers import validate_json_request, handle_errors

logger = logging.getLogger(__name__)

analysis_bp = Blueprint('analysis', __name__, url_prefix='/api/analysis')

bias_detection = BiasDetectionService()


def get_db_session():
    """Get database session"""
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


@analysis_bp.route('/analyze', methods=['POST'])
@handle_errors
def analyze():
    """Analyze policy for bias"""
    logger.info("Received analysis request")
    logger.debug(f"Request method: {request.method}")
    logger.debug(f"Request content type: {request.content_type}")
    
    user_id = None
    
    # Check for authentication
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            logger.debug("Authorization header found, attempting to extract user_id...")
            from app.services.auth_service import AuthenticationService
            token = auth_header.split()[1]
            payload = AuthenticationService.verify_token(token)
            user_id = payload.get('user_id')
            logger.debug(f"User authenticated: {user_id}")
        except Exception as e:
            logger.warning(f"Failed to authenticate user: {str(e)}, proceeding as anonymous")
            pass
    else:
        logger.debug("No authorization header, processing as anonymous user")
    
    # Handle JSON request
    if request.is_json:
        logger.debug("Processing JSON request body")
        data = request.get_json()
        policy_text = data.get('policyText', '').strip()
        policy_name = data.get('policyName', 'Untitled Policy').strip()
        logger.debug(f"Policy name: {policy_name}, text length: {len(policy_text)} characters")
    # Handle file upload
    elif 'file' in request.files:
        logger.debug("Processing file upload")
        file = request.files['file']
        
        # Get policy name from form data or file name
        policy_name = request.form.get('policyName', file.filename)
        
        logger.debug(f"File received: {file.filename}, size: {file.size} bytes, policy_name: {policy_name}")
        
        if not file or file.filename == '':
            logger.warning("No file provided or empty filename")
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        if file.size > Config.MAX_FILE_SIZE:
            logger.warning(f"File size exceeds limit: {file.size} > {Config.MAX_FILE_SIZE}")
            return jsonify({'success': False, 'error': 'File size exceeds limit'}), 413
        
        try:
            file_ext = DocumentParser.get_file_extension(file.filename)
            logger.debug(f"Parsing file with extension: {file_ext}")
            policy_text = DocumentParser.parse_file(file.read(), file_ext)
            logger.debug(f"File parsed successfully, extracted text length: {len(policy_text)} characters")
        except ValueError as e:
            logger.error(f"File parsing error: {str(e)}")
            return jsonify({'success': False, 'error': str(e)}), 400
    else:
        logger.warning("Request missing both JSON body and file upload")
        return jsonify({'success': False, 'error': 'Either JSON body or file upload required'}), 400
    
    # Validate policy text
    if not policy_text:
        logger.warning("Policy text is empty")
        return jsonify({'success': False, 'error': 'Policy text is required'}), 400
    
    if len(policy_text) > 1000000:  # 1MB of text
        logger.warning(f"Policy text exceeds size limit: {len(policy_text)} > 1000000 characters")
        return jsonify({'success': False, 'error': 'Policy text is too long'}), 413
    
    # Analyze policy
    try:
        logger.info(f"Starting policy analysis - Name: {policy_name}, User: {user_id}")
        analysis = bias_detection.analyze_policy(policy_text, policy_name, user_id)
        logger.debug(f"Analysis completed successfully - ID: {analysis.id}")
        
        # Save to database if user is logged in
        db = get_db_session()
        try:
            logger.debug("Saving analysis to database...")
            db.add(analysis)
            db.commit()
            analysis_id = analysis.id
            db.refresh(analysis)
            logger.info(f"Analysis saved to database - ID: {analysis_id}")
        finally:
            db.close()
        
        return jsonify({
            'success': True,
            'data': {
                'id': analysis.id,
                'policyName': analysis.policy_name,
                'policyText': analysis.policy_text,
                'analyzedAt': analysis.analyzed_at.isoformat() if analysis.analyzed_at else None,
                'totalBiasCount': analysis.total_bias_count,
                'overallSeverity': analysis.overall_severity,
                'biasInstances': [b.to_dict() for b in analysis.bias_instances],
                'biasByCategory': bias_detection.get_bias_by_category(analysis),
            }
        }), 200
        
    except ValueError as e:
        logger.error(f"Validation error during analysis: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error during policy analysis: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Analysis failed'}), 500


@analysis_bp.route('/<analysis_id>', methods=['GET'])
def get_analysis(analysis_id):
    """Get analysis by ID"""
    logger.info(f"Retrieving analysis - ID: {analysis_id}")
    
    db = get_db_session()
    
    try:
        logger.debug(f"Querying database for analysis ID: {analysis_id}")
        analysis = db.query(AnalysisResult).filter(AnalysisResult.id == analysis_id).first()
        
        if not analysis:
            logger.warning(f"Analysis not found - ID: {analysis_id}")
            return jsonify({'success': False, 'error': 'Analysis not found'}), 404
        
        logger.info(f"Analysis found and returning - ID: {analysis_id}")
        
        return jsonify({
            'success': True,
            'data': {
                'id': analysis.id,
                'policyName': analysis.policy_name,
                'policyText': analysis.policy_text,
                'analyzedAt': analysis.analyzed_at.isoformat() if analysis.analyzed_at else None,
                'totalBiasCount': analysis.total_bias_count,
                'overallSeverity': analysis.overall_severity,
                'biasInstances': [b.to_dict() for b in analysis.bias_instances],
                'biasByCategory': bias_detection.get_bias_by_category(analysis),
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error retrieving analysis: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Failed to retrieve analysis'}), 500
    finally:
        db.close()


@analysis_bp.route('/user/analyses', methods=['GET'])
@token_required
def get_user_analyses(user_id):
    """Get all analyses for a user"""
    logger.info(f"Retrieving analyses for user - ID: {user_id}")
    
    db = get_db_session()
    
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        logger.debug(f"Pagination - Page: {page}, Per Page: {per_page}")
        
        query = db.query(AnalysisResult).filter(AnalysisResult.user_id == user_id)
        total = query.count()
        
        logger.debug(f"Total analyses for user {user_id}: {total}")
        
        analyses = query.order_by(AnalysisResult.analyzed_at.desc())\
            .offset((page - 1) * per_page)\
            .limit(per_page)\
            .all()
        
        logger.info(f"Retrieved {len(analyses)} analyses for user - ID: {user_id}")
        
        return jsonify({
            'success': True,
            'data': {
                'analyses': [a.to_dict(include_text=False) for a in analyses],
                'total': total,
                'page': page,
                'per_page': per_page,
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error retrieving user analyses: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Failed to retrieve analyses'}), 500
    finally:
        db.close()


@analysis_bp.route('/<analysis_id>', methods=['DELETE'])
@token_required
def delete_analysis(user_id, analysis_id):
    """Delete an analysis"""
    logger.info(f"Deleting analysis - ID: {analysis_id}, User: {user_id}")
    
    db = get_db_session()
    
    try:
        logger.debug(f"Querying database for analysis ID: {analysis_id} owned by user: {user_id}")
        analysis = db.query(AnalysisResult).filter(
            AnalysisResult.id == analysis_id,
            AnalysisResult.user_id == user_id
        ).first()
        
        if not analysis:
            logger.warning(f"Analysis not found or unauthorized - ID: {analysis_id}, User: {user_id}")
            return jsonify({'success': False, 'error': 'Analysis not found'}), 404
        
        logger.debug(f"Deleting analysis from database - ID: {analysis_id}")
        db.delete(analysis)
        db.commit()
        
        logger.info(f"Analysis deleted successfully - ID: {analysis_id}, User: {user_id}")
        
        return jsonify({'success': True, 'data': {'message': 'Analysis deleted'}}), 200
        
    except Exception as e:
        logger.error(f"Error deleting analysis: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Failed to delete analysis'}), 500
    finally:
        db.close()


@analysis_bp.route('/<analysis_id>/export-pdf', methods=['GET'])
def export_analysis_pdf(analysis_id):
    """Export analysis as PDF"""
    logger.info(f"Exporting analysis as PDF - ID: {analysis_id}")
    
    db = get_db_session()
    
    try:
        logger.debug(f"Querying database for analysis ID: {analysis_id}")
        analysis = db.query(AnalysisResult).filter(AnalysisResult.id == analysis_id).first()
        
        if not analysis:
            logger.warning(f"Analysis not found for PDF export - ID: {analysis_id}")
            return jsonify({'success': False, 'error': 'Analysis not found'}), 404
        
        logger.debug(f"Generating PDF for analysis - ID: {analysis_id}")
        
        # Try to import reportlab for PDF generation
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib import colors
            from io import BytesIO
            
            logger.debug("ReportLab imported successfully")
            
            # Create PDF in memory
            pdf_buffer = BytesIO()
            doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            elements = []
            
            # Add title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#000000'),
                spaceAfter=6,
                alignment=1
            )
            elements.append(Paragraph(f"Policy Bias Analysis Report", title_style))
            elements.append(Spacer(1, 0.2*inch))
            
            # Add metadata
            meta_style = styles['Normal']
            elements.append(Paragraph(f"<b>Policy Name:</b> {analysis.policy_name}", meta_style))
            elements.append(Paragraph(f"<b>Analysis Date:</b> {analysis.analyzed_at.strftime('%B %d, %Y') if analysis.analyzed_at else 'N/A'}", meta_style))
            elements.append(Spacer(1, 0.3*inch))
            
            # Add summary section
            elements.append(Paragraph("Summary", styles['Heading2']))
            summary_data = [
                ['Metric', 'Value'],
                ['Total Issues Found', str(analysis.total_bias_count)],
                ['Overall Severity', analysis.overall_severity.upper()],
            ]
            summary_table = Table(summary_data, colWidths=[2.5*inch, 2*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e0e0e0')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(summary_table)
            elements.append(Spacer(1, 0.3*inch))
            
            # Add bias instances
            if analysis.bias_instances:
                elements.append(Paragraph("Detected Issues", styles['Heading2']))
                for i, bias in enumerate(analysis.bias_instances, 1):
                    elements.append(Paragraph(
                        f"<b>Issue {i}: {bias.bias_type.upper()}</b> - Severity: <b>{bias.severity.upper()}</b>",
                        styles['Heading3']
                    ))
                    elements.append(Paragraph(f"<i>Text:</i> \"{bias.original_text}\"", meta_style))
                    elements.append(Paragraph(f"<i>Explanation:</i> {bias.explanation}", meta_style))
                    elements.append(Paragraph(f"<i>Suggested Fix:</i> {bias.suggested_rewrite}", meta_style))
                    elements.append(Spacer(1, 0.2*inch))
            else:
                elements.append(Paragraph("<b>No bias detected in this policy!</b>", styles['Heading2']))
            
            # Build PDF
            doc.build(elements)
            pdf_buffer.seek(0)
            
            logger.info(f"PDF generated successfully - ID: {analysis_id}, size: {len(pdf_buffer.getvalue())} bytes")
            
            # Return PDF file
            from flask import send_file
            return send_file(
                pdf_buffer,
                mimetype='application/pdf',
                as_attachment=True,
                attachment_filename=f"{analysis.policy_name.replace(' ', '_')}_analysis_{analysis_id}.pdf"
            )
            
        except ImportError as ie:
            logger.warning(f"ReportLab not installed: {str(ie)}, returning JSON fallback")
            # Fallback: return JSON that can be converted to PDF on frontend
            return jsonify({
                'success': True,
                'data': {
                    'policyName': analysis.policy_name,
                    'analyzedAt': analysis.analyzed_at.isoformat() if analysis.analyzed_at else None,
                    'totalBiasCount': analysis.total_bias_count,
                    'overallSeverity': analysis.overall_severity,
                    'biasInstances': [b.to_dict() for b in analysis.bias_instances],
                }
            }), 200
        
    except Exception as e:
        logger.error(f"Error exporting PDF: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        db.close()

