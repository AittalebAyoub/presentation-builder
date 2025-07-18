import os

class Config:
    """Base configuration class for the application."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
# API Configuration
    API_KEY = os.environ.get('OPENAI_API_KEY') or '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'
    BASE_URL = "https://openrouter.ai/api/v1"
    MODEL = "deepseek/deepseek-chat:free"
    
    # Application configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app/static/uploads')
    OUTPUT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app/static/outputs')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = False
    TESTING = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    # In production, ensure all sensitive values are set via environment variables
    SECRET_KEY = os.environ.get('SECRET_KEY')
    API_KEY = os.environ.get('OPENAI_API_KEY')

# Dictionary to easily access different configurations
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}