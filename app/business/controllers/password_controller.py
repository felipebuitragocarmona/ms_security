from datetime import datetime
from app.data.database import db
from app.business.models.password import Password
from app.business.models.user import User
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash

class PasswordController:
    @staticmethod
    def get_all():
        """Get all passwords"""
        try:
            passwords = Password.query.all()
            return [password.to_dict() for password in passwords], 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_by_id(password_id):
        """Get a password by ID"""
        try:
            password = Password.query.get(password_id)
            if not password:
                return {"error": "Password record not found"}, 404
            return password.to_dict(), 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500
    
    @staticmethod
    def get_by_user_id(user_id):
        """Get all password history for a specific user"""
        try:
            passwords = Password.query.filter_by(user_id=user_id).order_by(Password.startAt.desc()).all()
            return [password.to_dict() for password in passwords], 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500
    
    @staticmethod
    def get_current_password(user_id):
        """Get the current active password for a user"""
        try:
            # Current password is the one with startAt <= now and endAt is either NULL or > now
            now = datetime.utcnow()
            password = Password.query.filter_by(user_id=user_id)\
                .filter(Password.startAt <= now)\
                .filter((Password.endAt == None) | (Password.endAt > now))\
                .order_by(Password.startAt.desc())\
                .first()
            
            if not password:
                return {"error": "No active password found for this user"}, 404
                
            return password.to_dict(), 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500

    @staticmethod
    def create(user_id, data):
        """Create a new password for a user"""
        try:
            # Check if user exists
            user = User.query.get(user_id)
            if not user:
                return {"error": "User not found"}, 404
            
            # Validate required fields
            if 'content' not in data:
                return {"error": "Password content is required"}, 400
            if 'startAt' not in data:
                return {"error": "startAt content is required"}, 400
            if 'endAt' not in data:
                return {"error": "endAt content is required"}, 400
            
            # If this is a new password, end the current one
            current_password = Password.query.filter_by(user_id=user_id, endAt=None).first()
            if current_password:
                current_password.endAt = datetime.utcnow()
            startAt=datetime.strptime(data.get('startAt'), "%Y-%m-%d %H:%M:%S")
            endAt=datetime.strptime(data.get('endAt'), "%Y-%m-%d %H:%M:%S")
            # Create the new password record
            new_password = Password(
                user_id=user_id,
                content=generate_password_hash(data['content']),
                startAt=startAt,
                endAt=endAt
            )
            
            # Update the user's current password too
            user.password = generate_password_hash(data['content'])
            
            db.session.add(new_password)
            db.session.commit()
            
            return new_password.to_dict(), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def update(password_id, data):
        """Update a password record"""
        try:
            password = Password.query.get(password_id)
            if not password:
                return {"error": "Password record not found"}, 404
            
            if 'content' in data:
                password.content = generate_password_hash(data['content'])
            if 'startAt' in data:
                startAt = datetime.strptime(data.get('startAt'), "%Y-%m-%d %H:%M:%S")
                password.startAt = startAt
            if 'endAt' in data:
                endAt = datetime.strptime(data.get('endAt'), "%Y-%m-%d %H:%M:%S")
                password.endAt = endAt
                
            db.session.commit()
            return password.to_dict(), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def delete(password_id):
        """Delete a password record"""
        try:
            password = Password.query.get(password_id)
            if not password:
                return {"error": "Password record not found"}, 404
            
            db.session.delete(password)
            db.session.commit()
            
            return {"message": "Password record deleted successfully"}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500