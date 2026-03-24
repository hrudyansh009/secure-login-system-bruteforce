# Imports
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify

# Password hashing
def hash_password(password):
    return generate_password_hash(
        password,
        method='pbkdf2:sha256',
        salt_length=16
    )

def verify_password(password_hash, password):
    return check_password_hash(password_hash, password)

# Rate limiting
login_attempts = {}

def check_rate_limit(ip_address, max_attempts=5, time_window=60):
    current_time = datetime.utcnow()
    
    if ip_address not in login_attempts:
        login_attempts[ip_address] = []
    
    # Remove old attempts
    login_attempts[ip_address] = [
        timestamp for timestamp in login_attempts[ip_address]
        if (current_time - timestamp).total_seconds() < time_window
    ]
    
    attempts_count = len(login_attempts[ip_address])
    
    if attempts_count >= max_attempts:
        return False, 0
    
    login_attempts[ip_address].append(current_time)
    return True, max_attempts - attempts_count - 1

# Account lockout
def lock_account(user, duration_minutes=15):
    from database import db
    user.locked_until = datetime.utcnow() + timedelta(minutes=duration_minutes)
    db.session.commit()

def unlock_account(user):
    from database import db
    user.locked_until = None
    user.failed_login_attempts = 0
    db.session.commit()

def increment_failed_attempts(user, max_attempts=5):
    from database import db
    user.failed_login_attempts += 1
    
    if user.failed_login_attempts >= max_attempts:
        lock_account(user)
        db.session.commit()
        return True
    
    db.session.commit()
    return False

# Security headers
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
    return response
