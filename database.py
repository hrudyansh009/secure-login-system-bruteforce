# Imports
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# SQLAlchemy ORM
db = SQLAlchemy()

# User model
class User(db.Model):
    __tablename__ = 'users'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # User info
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Security fields
    failed_login_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime, nullable=True)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def is_locked(self):
        if self.locked_until is None:
            return False
        return datetime.utcnow() < self.locked_until

# Database init
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")

