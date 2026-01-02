import logging
from typing import Dict, Any, List
from datetime import datetime
from app.services.groq_service import get_groq_service
from app.models.models import AnalysisResult, BiasInstance

logger = logging.getLogger(__name__)


class BiasDetectionService:
    """Service for detecting bias in policies"""
    
    def __init__(self):
        """Initialize bias detection service"""
        logger.info("Initializing BiasDetectionService...")
        self.groq_service = get_groq_service()
        logger.debug("BiasDetectionService initialized successfully")
    
    def analyze_policy(self, policy_text: str, policy_name: str = "Untitled Policy", user_id: str = None) -> AnalysisResult:
        """
        Analyze a policy for bias
        
        Args:
            policy_text: The policy text to analyze
            policy_name: Name of the policy
            user_id: Optional user ID for saving analysis
            
        Returns:
            AnalysisResult object
        """
        try:
            logger.info(f"Starting bias analysis for policy: {policy_name}")
            logger.debug(f"Policy text length: {len(policy_text)} characters")
            logger.debug(f"User ID: {user_id}")
            
            # Call Groq API for analysis
            logger.debug("Calling GroqService.analyze_policy()...")
            groq_response = self.groq_service.analyze_policy(policy_text)
            logger.debug("GroqService.analyze_policy() returned successfully")
            
            # Create AnalysisResult object
            logger.debug(f"Creating AnalysisResult object for policy: {policy_name}")
            analysis = AnalysisResult(
                policy_name=policy_name,
                policy_text=policy_text,
                user_id=user_id,
                analyzed_at=datetime.utcnow(),
            )
            logger.debug(f"AnalysisResult object created with ID: {analysis.id}")
            
            # Process bias instances from Groq response
            bias_instances_data = groq_response.get('bias_instances', [])
            summary = groq_response.get('summary', {})
            
            logger.debug(f"Processing {len(bias_instances_data)} bias instances...")
            
            # Create BiasInstance objects
            for idx, instance_data in enumerate(bias_instances_data):
                logger.debug(f"Processing bias instance {idx}: {instance_data.get('type')} ({instance_data.get('severity')})")
                
                bias_instance = BiasInstance(
                    analysis=analysis,
                    original_text=instance_data.get('text', ''),
                    bias_type=instance_data.get('type', 'other'),
                    severity=instance_data.get('severity', 'low'),
                    explanation=instance_data.get('explanation', ''),
                    suggested_rewrite=instance_data.get('suggested_rewrite', ''),
                    start_index=instance_data.get('start_index', 0),
                    end_index=instance_data.get('end_index', 0),
                )
                analysis.bias_instances.append(bias_instance)
                logger.debug(f"Bias instance {idx} created and appended to analysis")
            
            # Update summary fields
            analysis.total_bias_count = summary.get('total_bias_count', 0)
            analysis.overall_severity = summary.get('overall_severity', 'low')
            
            logger.info(f"Analysis completed for policy: {policy_name}")
            logger.info(f"  Total bias instances: {analysis.total_bias_count}")
            logger.info(f"  Overall severity: {analysis.overall_severity}")
            logger.debug(f"  Summary: {summary}")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error during bias analysis for policy '{policy_name}': {str(e)}", exc_info=True)
            raise
    
    def get_bias_by_category(self, analysis: AnalysisResult) -> Dict[str, int]:
        """
        Get breakdown of bias by category
        
        Args:
            analysis: AnalysisResult object
            
        Returns:
            Dictionary with bias counts by category
        """
        logger.debug(f"Calculating bias breakdown by category for analysis ID: {analysis.id}")
        
        bias_breakdown = {
            'gender': 0,
            'age': 0,
            'disability': 0,
            'racial': 0,
            'other': 0,
        }
        
        for instance in analysis.bias_instances:
            if instance.bias_type in bias_breakdown:
                bias_breakdown[instance.bias_type] += 1
                logger.debug(f"Counted {instance.bias_type} bias instance")
        
        logger.debug(f"Bias breakdown calculated: {bias_breakdown}")
        return bias_breakdown
