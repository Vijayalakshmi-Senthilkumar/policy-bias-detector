import logging
from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.config import get_config, Config
from app.models.models import Base
from app.utils.helpers import setup_logging
from app.routes.auth_routes import auth_bp
from app.routes.analysis_routes import analysis_bp


def create_app(config_class=None):
    """
    Application factory for Flask app
    
    Args:
        config_class: Configuration class to use
        
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    if config_class is None:
        config_class = get_config()
    
    app.config.from_object(config_class)
    
    # Setup logging
    setup_logging(
        log_level=Config.LOG_LEVEL,
        log_file=Config.LOG_FILE if Config.ENV == 'production' else None
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Creating Flask app with config: {config_class.__name__}")
    logger.debug(f"Config details - ENV: {Config.ENV}, DEBUG: {Config.DEBUG}, HOST: {Config.SERVER_HOST}:{Config.SERVER_PORT}")
    
    # Setup CORS
    logger.debug(f"Setting up CORS with origins: {Config.CORS_ORIGINS}")
    CORS(app, resources={
        r"/api/*": {
            "origins": Config.CORS_ORIGINS,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    logger.info("CORS configured successfully")
    
    # Initialize database
    try:
        logger.info(f"Initializing database at: {Config.SQLALCHEMY_DATABASE_URI}")
        engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
        Base.metadata.create_all(engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}", exc_info=True)
        raise
    
    # Register blueprints
    logger.debug("Registering blueprints...")
    app.register_blueprint(auth_bp)
    logger.debug("Auth blueprint registered")
    
    app.register_blueprint(analysis_bp)
    logger.debug("Analysis blueprint registered")
    
    logger.info("All blueprints registered successfully")
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health():
        """Health check endpoint"""
        logger.debug("Health check requested")
        return jsonify({'success': True, 'status': 'healthy'}), 200
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def root():
        """Root endpoint"""
        logger.debug("Root endpoint requested")
        return jsonify({
            'success': True,
            'name': 'Policy Bias Detector API',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth',
                'analysis': '/api/analysis',
                'health': '/api/health'
            }
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        """Handle 404 errors"""
        logger.warning(f"404 error: {e}")
        return jsonify({'success': False, 'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(e):
        """Handle 500 errors"""
        logger.error(f"500 Internal server error: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Internal server error'}), 500
    
    logger.info("Flask app created and configured successfully")
    
    return app


def initialize_db():
    """Initialize database tables"""
    logger = logging.getLogger(__name__)
    
    try:
        engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
        Base.metadata.create_all(engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {str(e)}")
        raise
