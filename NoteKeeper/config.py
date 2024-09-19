# config.py
import os

# Set data directory based on environment variable, defaulting to ~/data if not set
DATA_DIR = os.getenv('DATA_DIR', os.path.join(os.path.expanduser('~'), 'data'))

class Config:
    SECRET_KEY = 'ENTER-KEY'
    
    # Use os.path.join to ensure correct paths for different environments
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(DATA_DIR, "PVWebAppDB.db")}'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable tracking to save resources
    DEBUG = False
    TESTING = False

    # Ensure the data directory exists
    @staticmethod
    def ensure_directories():
        os.makedirs(DATA_DIR, exist_ok=True)

class TestingConfig(Config):
    TESTING = True  #Enable testing mode
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_PVWebAppDB.db'  #Use a separate database for tests
    WTF_CSRF_ENABLED = False  #Disable CSRF for easier testing
