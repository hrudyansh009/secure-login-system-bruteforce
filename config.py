# Imports
import os
from datetime import timedelta

class Config:
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production-XYZ123'
    
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///secure_login.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session security
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Security settings
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_DURATION = 15
    RATE_LIMIT_PER_MINUTE = 20
    
    # Password requirements
    MIN_PASSWORD_LENGTH = 8
    REQUIRE_UPPERCASE = True
    REQUIRE_LOWERCASE = True
    REQUIRE_DIGIT = True
    REQUIRE_SPECIAL_CHAR = True
    BCRYPT_LOG_ROUNDS = 12
