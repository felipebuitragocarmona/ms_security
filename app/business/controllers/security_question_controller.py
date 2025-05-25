from app.data.database import db
from app.business.models.security_question import SecurityQuestion
from sqlalchemy.exc import SQLAlchemyError

class SecurityQuestionController:
    @staticmethod
    def get_all():
        """Get all security questions"""
        try:
            questions = SecurityQuestion.query.all()
            return [question.to_dict() for question in questions], 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_by_id(question_id):
        """Get a security question by ID"""
        try:
            question = SecurityQuestion.query.get(question_id)
            if not question:
                return {"error": "Security question not found"}, 404
            return question.to_dict(), 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500

    @staticmethod
    def create(data):
        """Create a new security question"""
        try:
            # Validate required fields
            if 'name' not in data:
                return {"error": "Security question name is required"}, 400
            
            new_question = SecurityQuestion(
                name=data['name'],
                description=data.get('description', '')
            )
            
            db.session.add(new_question)
            db.session.commit()
            
            return new_question.to_dict(), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def update(question_id, data):
        """Update a security question"""
        try:
            question = SecurityQuestion.query.get(question_id)
            if not question:
                return {"error": "Security question not found"}, 404
            
            if 'name' in data:
                question.name = data['name']
            if 'description' in data:
                question.description = data['description']
                
            db.session.commit()
            return question.to_dict(), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def delete(question_id):
        """Delete a security question"""
        try:
            question = SecurityQuestion.query.get(question_id)
            if not question:
                return {"error": "Security question not found"}, 404
            
            db.session.delete(question)
            db.session.commit()
            
            return {"message": "Security question deleted successfully"}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500