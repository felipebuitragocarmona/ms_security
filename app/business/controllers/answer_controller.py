from app.data.database import db
from app.business.models.answer import Answer
from app.business.models.user import User
from app.business.models.security_question import SecurityQuestion
from sqlalchemy.exc import SQLAlchemyError

class AnswerController:
    @staticmethod
    def get_all():
        """Get all answers"""
        try:
            answers = Answer.query.all()
            return [answer.to_dict() for answer in answers], 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_by_id(answer_id):
        """Get an answer by ID"""
        try:
            answer = Answer.query.get(answer_id)
            if not answer:
                return {"error": "Answer not found"}, 404
            return answer.to_dict(), 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500
    
    @staticmethod
    def get_by_user_id(user_id):
        """Get all answers for a specific user"""
        try:
            answers = Answer.query.filter_by(user_id=user_id).all()
            return [answer.to_dict() for answer in answers], 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500
    
    @staticmethod
    def get_by_question_id(question_id):
        """Get all answers for a specific security question"""
        try:
            answers = Answer.query.filter_by(security_question_id=question_id).all()
            return [answer.to_dict() for answer in answers], 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500
    
    @staticmethod
    def get_by_user_and_question(user_id, question_id):
        """Get a user's answer for a specific security question"""
        try:
            answer = Answer.query.filter_by(
                user_id=user_id,
                security_question_id=question_id
            ).first()
            
            if not answer:
                return {"error": "Answer not found for this user and question"}, 404
                
            return answer.to_dict(), 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500

    @staticmethod
    def create(user_id, question_id, data):
        """Create a new answer for a user and security question"""
        try:
            # Check if user exists
            user = User.query.get(user_id)
            if not user:
                return {"error": "User not found"}, 404
                
            # Check if security question exists
            question = SecurityQuestion.query.get(question_id)
            if not question:
                return {"error": "Security question not found"}, 404
                
            # Check if an answer already exists for this user and question
            existing = Answer.query.filter_by(
                user_id=user_id,
                security_question_id=question_id
            ).first()
            
            if existing:
                return {"error": "An answer already exists for this user and question"}, 400
            
            # Validate required fields
            if 'content' not in data:
                return {"error": "Answer content is required"}, 400
            
            new_answer = Answer(
                user_id=user_id,
                security_question_id=question_id,
                content=data['content']
            )
            
            db.session.add(new_answer)
            db.session.commit()
            
            return new_answer.to_dict(), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def update(answer_id, data):
        """Update an answer"""
        try:
            answer = Answer.query.get(answer_id)
            if not answer:
                return {"error": "Answer not found"}, 404
            
            if 'content' in data:
                answer.content = data['content']
                
            db.session.commit()
            return answer.to_dict(), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def delete(answer_id):
        """Delete an answer"""
        try:
            answer = Answer.query.get(answer_id)
            if not answer:
                return {"error": "Answer not found"}, 404
            
            db.session.delete(answer)
            db.session.commit()
            
            return {"message": "Answer deleted successfully"}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500