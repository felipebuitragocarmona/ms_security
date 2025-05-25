from app.data.database import db
from app.business.models.user import User
from sqlalchemy.exc import SQLAlchemyError


class UserController:
    @staticmethod
    def get_all():
        """Get all users"""
        try:
            users = User.query.all()
            return [user.to_dict() for user in users], 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def get_by_id(user_id):
        """Get a user by ID"""
        try:
            user = User.query.get(user_id)
            if not user:
                return {"error": "User not found"}, 404
            return user.to_dict(), 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500

    @staticmethod
    def create(data):
        """Create a new user"""
        try:
            # Check if user with the same email already exists
            if User.query.filter_by(email=data['email']).first():
                return {"error": "Email already registered"}, 400

            
            new_user = User(
                name=data['name'],
                email=data['email']
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            return new_user.to_dict(), 201
        except KeyError as e:
            return {"error": f"Missing required field: {str(e)}"}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def update(user_id, data):
        """Update a user"""
        try:
            user = User.query.get(user_id)
            if not user:
                return {"error": "User not found"}, 404
                
            if 'name' in data:
                user.name = data['name']
            if 'email' in data:
                # Check if new email is already in use by another user
                existing_user = User.query.filter_by(email=data['email']).first()
                if existing_user and existing_user.id != user_id:
                    return {"error": "Email already in use"}, 400
                user.email = data['email']
                
            db.session.commit()
            return user.to_dict(), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def delete(user_id):
        """Delete a user"""
        try:
            user = User.query.get(user_id)
            if not user:
                return {"error": "User not found"}, 404
                
            db.session.delete(user)
            db.session.commit()
            
            return {"message": "User deleted successfully"}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500