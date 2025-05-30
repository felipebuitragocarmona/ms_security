from app.data.database import db
from datetime import datetime

class Permission(db.Model):
    __tablename__ = 'permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    method = db.Column(db.String(10), nullable=False)  # GET, POST, PUT, DELETE, etc.
    entity = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Many-to-Many relationship with Role through RolePermission
    role_permissions = db.relationship('RolePermission', back_populates='permission', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'method': self.method,
            'entity': self.entity,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }