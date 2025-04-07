import os
from flask import Flask
from config import config
from flask_cors import CORS


def create_app(config_name='default'):
    """
    Application factory function to create and configure the Flask app.
    
    Args:
        config_name: The configuration to use (default, development, testing, production)
        
    Returns:
        A configured Flask application instance
    """
    app = Flask(__name__)
    CORS(app)

    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Ensure the upload and output folders exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
    
    # Register blueprints
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    @app.route('/health')
    def health_check():
        """Health check endpoint to verify the application is running."""
        return {'status': 'OK', 'message': 'Presentation Builder API is running'}
    
    return app