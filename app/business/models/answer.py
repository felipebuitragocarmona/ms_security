from app.data.database import db
from datetime import datetime

class Answer(db.Model):
    __tablename__ = 'answers'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys for Many-to-Many relationship between User and SecurityQuestion
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    security_question_id = db.Column(db.Integer, db.ForeignKey('security_questions.id'), nullable=False)
    
    # Relationships
    user = db.relationship('User', back_populates='answers')
    security_question = db.relationship('SecurityQuestion', back_populates='answers')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'security_question_id': self.security_question_id,
            'content': self.content,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }