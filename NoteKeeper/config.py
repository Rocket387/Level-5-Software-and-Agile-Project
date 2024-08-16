# config.py
import os

# config.py
#config file to setup database for webapp in production, development and Test
class Config:
    SECRET_KEY = 'ENTER-KEY'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///PVWebAppDB.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable tracking to save resources
    DEBUG = False  # Disable debugging by default
    TESTING = False  # Disable testing by default


class DevelopmentConfig(Config):
    DEBUG = True  # Enable debugging for development


class TestingConfig(Config):
    TESTING = True  # Enable testing mode
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_PVWebAppDB.db'  # Use a separate database for tests
    WTF_CSRF_ENABLED = False  # Disable CSRF for easier testing
