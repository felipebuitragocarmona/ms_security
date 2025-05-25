from app.data.database import db
from datetime import datetime

class DigitalSignature(db.Model):
    __tablename__ = 'digital_signatures'
    
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String(255))  # Path to the stored signature image
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign key for One-to-One relationship with User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    user = db.relationship('User', back_populates='digital_signature')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'photo': self.photo,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }