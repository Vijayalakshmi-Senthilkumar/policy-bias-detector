#!/usr/bin/env python3
"""
Policy Bias Detector Backend
Main entry point for the Flask application
"""

import os
import logging
from app import create_app, initialize_db
from app.config.config import Config

# Setup logging
logging.basicConfig(
    level=Config.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Main function to run the Flask app"""
    
    logger.info("=" * 80)
    logger.info("STARTING POLICY BIAS DETECTOR BACKEND")
    logger.info("=" * 80)
    
    # Validate required environment variables
    if not Config.GROQ_API_KEY:
        logger.error("GROQ_API_KEY environment variable is not set!")
        raise ValueError("GROQ_API_KEY is required")
    
    logger.info(f"Configuration loaded successfully")
    logger.info(f"  Environment: {Config.ENV}")
    logger.info(f"  Debug Mode: {Config.DEBUG}")
    logger.info(f"  Log Level: {Config.LOG_LEVEL}")
    logger.info(f"  Database: {Config.SQLALCHEMY_DATABASE_URI}")
    logger.info(f"  Groq Model: {Config.GROQ_MODEL}")
    
    # Create Flask app
    logger.info("Creating Flask application...")
    app = create_app()
    logger.info("Flask application created successfully")
    
    # Initialize database
    try:
        logger.info("Initializing database...")
        initialize_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}", exc_info=True)
        raise
    
    # Get host and port from environment or use defaults
    host = os.getenv('SERVER_HOST', '0.0.0.0')
    port = int(os.getenv('SERVER_PORT', 5000))
    
    logger.info("=" * 80)
    logger.info(f"Flask server starting on {host}:{port}")
    logger.info(f"API health check: http://{host}:{port}/api/health")
    logger.info(f"API endpoints base: http://{host}:{port}/api")
    logger.info("=" * 80)
    
    # Run the app
    app.run(
        host=host,
        port=port,
        debug=Config.DEBUG,
        use_reloader=Config.DEBUG
    )


if __name__ == '__main__':
    main()
