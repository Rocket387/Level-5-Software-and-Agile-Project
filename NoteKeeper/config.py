# config.py
import os

# config.py
#config file to setup database for webapp in production, development and Test
class Config:
    SECRET_KEY = '1e02e0be94a7e186c84d92712e250cc4'
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
