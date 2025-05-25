from app.data.database import db
from datetime import datetime

class Session(db.Model):
    __tablename__ = 'sessions'
    
    id = db.Column(db.String(36), primary_key=True)
    token = db.Column(db.String(255), nullable=False)
    expiration = db.Column(db.DateTime, nullable=False)
    FACode = db.Column(db.String(10))
    state = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign key for Many-to-One relationship with User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='sessions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'token': self.token,
            'expiration': self.expiration,
            'FACode': self.FACode,
            'state': self.state,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }