import logging
from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.services.auth_service import AuthenticationService, token_required
from app.models.models import User, Base
from app.utils.helpers import validate_json_request, handle_errors

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


def get_db_session():
    """Get database session"""
    from app.config.config import Config
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


@auth_bp.route('/signup', methods=['POST'])
@validate_json_request
@handle_errors
def signup():
    """User signup endpoint"""
    logger.info("Signup request received")
    
    data = request.get_json()
    
    # Validate input
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    name = data.get('name', '').strip()
    
    logger.debug(f"Signup attempt - Email: {email}, Name: {name}")
    
    if not email or not password or not name:
        logger.warning("Signup validation failed: Missing email, password, or name")
        return jsonify({'success': False, 'error': 'Email, password, and name are required'}), 400
    
    if len(password) < 6:
        logger.warning(f"Signup validation failed: Password too short for email {email}")
        return jsonify({'success': False, 'error': 'Password must be at least 6 characters'}), 400
    
    # Get database session
    db = get_db_session()
    
    try:
        # Check if user already exists
        logger.debug(f"Checking if user exists - Email: {email}")
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            logger.warning(f"Signup failed: User already exists - Email: {email}")
            return jsonify({'success': False, 'error': 'User with this email already exists'}), 409
        
        # Create new user
        logger.debug(f"Creating new user - Email: {email}, Name: {name}")
        user = User(email=email, name=name)
        user.set_password(password)
        
        logger.debug(f"Hashing password for user - Email: {email}")
        
        db.add(user)
        db.commit()
        
        logger.info(f"User registered successfully - Email: {email}, ID: {user.id}")
        
        # Generate token
        logger.debug(f"Generating JWT token for new user - ID: {user.id}")
        token = AuthenticationService.generate_token(user.id)
        
        return jsonify({
            'success': True,
            'data': {
                'user': user.to_dict(),
                'token': token
            }
        }), 201
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error during signup: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Failed to create user'}), 500
    finally:
        db.close()


@auth_bp.route('/login', methods=['POST'])
@validate_json_request
@handle_errors
def login():
    """User login endpoint"""
    logger.info("Login request received")
    
    data = request.get_json()
    
    # Validate input
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    
    logger.debug(f"Login attempt - Email: {email}")
    
    if not email or not password:
        logger.warning("Login validation failed: Missing email or password")
        return jsonify({'success': False, 'error': 'Email and password are required'}), 400
    
    # Get database session
    db = get_db_session()
    
    try:
        # Find user
        logger.debug(f"Querying database for user - Email: {email}")
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            logger.warning(f"Login failed: User not found - Email: {email}")
            return jsonify({'success': False, 'error': 'Invalid email or password'}), 401
        
        logger.debug(f"User found, verifying password - Email: {email}")
        if not user.verify_password(password):
            logger.warning(f"Login failed: Invalid password - Email: {email}")
            return jsonify({'success': False, 'error': 'Invalid email or password'}), 401
        
        logger.info(f"User logged in successfully - Email: {email}, ID: {user.id}")
        
        # Generate token
        logger.debug(f"Generating JWT token for logged-in user - ID: {user.id}")
        token = AuthenticationService.generate_token(user.id)
        
        return jsonify({
            'success': True,
            'data': {
                'user': user.to_dict(),
                'token': token
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error during login: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Login failed'}), 500
    finally:
        db.close()


@auth_bp.route('/verify', methods=['POST'])
@token_required
def verify(user_id):
    """Verify token and get user info"""
    logger.info(f"Token verification request - User ID: {user_id}")
    
    db = get_db_session()
    
    try:
        logger.debug(f"Querying database for user - ID: {user_id}")
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            logger.warning(f"Token verification failed: User not found - ID: {user_id}")
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        logger.info(f"Token verified successfully - User ID: {user_id}, Email: {user.email}")
        
        return jsonify({
            'success': True,
            'data': {
                'user': user.to_dict()
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error verifying token: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Verification failed'}), 500
    finally:
        db.close()
