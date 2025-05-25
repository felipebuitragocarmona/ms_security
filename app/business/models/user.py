from app.data.database import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # One-to-One relationships
    profile = db.relationship('Profile', uselist=False, back_populates='user', cascade='all, delete-orphan')
    address = db.relationship('Address', uselist=False, back_populates='user', cascade='all, delete-orphan')
    digital_signature = db.relationship('DigitalSignature', uselist=False, back_populates='user', cascade='all, delete-orphan')
    
    # One-to-Many relationships
    sessions = db.relationship('Session', back_populates='user', cascade='all, delete-orphan')
    passwords = db.relationship('Password', back_populates='user', cascade='all, delete-orphan')
    devices = db.relationship('Device', back_populates='user', cascade='all, delete-orphan')
    
    # Many-to-Many relationships through intermediary tables
    user_roles = db.relationship('UserRole', back_populates='user', cascade='all, delete-orphan')
    answers = db.relationship('Answer', back_populates='user', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }