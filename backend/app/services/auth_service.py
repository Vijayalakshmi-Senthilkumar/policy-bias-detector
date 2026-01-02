import jwt
import logging
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app
from app.config.config import Config
from app.models.models import User

logger = logging.getLogger(__name__)


class AuthenticationService:
    """Service for handling authentication"""
    
    @staticmethod
    def generate_token(user_id: str) -> str:
        """
        Generate JWT token for user
        
        Args:
            user_id: User ID
            
        Returns:
            JWT token string
        """
        try:
            logger.info(f"Generating JWT token for user: {user_id}")
            
            payload = {
                'user_id': user_id,
                'exp': datetime.utcnow() + Config.JWT_EXPIRATION_DELTA,
                'iat': datetime.utcnow(),
            }
            
            logger.debug(f"Token payload: {payload}")
            logger.debug(f"JWT secret length: {len(Config.JWT_SECRET)} characters")
            
            token = jwt.encode(
                payload,
                Config.JWT_SECRET,
                algorithm='HS256'
            )
            
            logger.info(f"JWT token generated successfully for user: {user_id}")
            logger.debug(f"Token length: {len(token)} characters")
            
            return token
        except Exception as e:
            logger.error(f"Error generating JWT token for user {user_id}: {str(e)}", exc_info=True)
            raise
    
    @staticmethod
    def verify_token(token: str) -> dict:
        """
        Verify JWT token
        
        Args:
            token: JWT token string
            
        Returns:
            Decoded token payload
            
        Raises:
            ValueError: If token is invalid or expired
        """
        try:
            logger.debug(f"Verifying JWT token, length: {len(token)} characters")
            
            payload = jwt.decode(
                token,
                Config.JWT_SECRET,
                algorithms=['HS256']
            )
            
            logger.info(f"JWT token verified successfully for user: {payload.get('user_id')}")
            logger.debug(f"Token payload: {payload}")
            
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("JWT token verification failed: Token has expired")
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError as e:
            logger.warning(f"JWT token verification failed: Invalid token - {str(e)}")
            raise ValueError("Invalid token")
    
    @staticmethod
    def get_token_from_request() -> str:
        """
        Extract token from request headers
        
        Returns:
            Token string
            
        Raises:
            ValueError: If no token found
        """
        logger.debug("Extracting token from request headers...")
        
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            logger.warning("Token extraction failed: Missing Authorization header")
            raise ValueError("Missing Authorization header")
        
        logger.debug(f"Authorization header found, length: {len(auth_header)} characters")
        
        parts = auth_header.split()
        
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            logger.warning(f"Token extraction failed: Invalid Authorization header format. Parts: {len(parts)}")
            raise ValueError("Invalid Authorization header format")
        
        token = parts[1]
        logger.debug(f"Token extracted successfully, length: {len(token)} characters")
        
        return token


def token_required(f):
    """Decorator to protect routes that require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        logger.debug("Token authentication check started...")
        try:
            logger.debug("Extracting token from request...")
            token = AuthenticationService.get_token_from_request()
            
            logger.debug("Verifying token...")
            payload = AuthenticationService.verify_token(token)
            
            user_id = payload.get('user_id')
            logger.info(f"Token authentication successful for user: {user_id}")
            
            kwargs['user_id'] = user_id
            return f(*args, **kwargs)
        except ValueError as e:
            logger.warning(f"Authentication error: {str(e)}")
            return jsonify({'success': False, 'error': str(e)}), 401
        except Exception as e:
            logger.error(f"Unexpected error during authentication: {str(e)}", exc_info=True)
            return jsonify({'success': False, 'error': 'Authentication failed'}), 401
    
    return decorated_function
