import uuid
from datetime import datetime
from app.data.database import db
from app.business.models.user_role import UserRole
from app.business.models.user import User
from app.business.models.role import Role
from sqlalchemy.exc import SQLAlchemyError

class UserRoleController:
    @staticmethod
    def get_all():
        """Get all user-role relationships"""
        try:
            user_roles = UserRole.query.all()
            return [ur.to_dict() for ur in user_roles], 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_by_id(user_role_id):
        """Get a user-role relationship by ID"""
        try:
            user_role = UserRole.query.get(user_role_id)
            if not user_role:
                return {"error": "User-Role relationship not found"}, 404
            return user_role.to_dict(), 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500
    
    @staticmethod
    def get_by_user_id(user_id):
        """Get all roles for a specific user"""
        try:
            user_roles = UserRole.query.filter_by(user_id=user_id).all()
            return [ur.to_dict() for ur in user_roles], 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500
    
    @staticmethod
    def get_by_role_id(role_id):
        """Get all users for a specific role"""
        try:
            user_roles = UserRole.query.filter_by(role_id=role_id).all()
            return [ur.to_dict() for ur in user_roles], 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500

    @staticmethod
    def create(user_id, role_id, data=None):
        """Create a new user-role relationship"""
        try:
            # Check if user exists
            if 'startAt' not in data:
                return {"error": "startAt content is required"}, 400
            if 'endAt' not in data:
                return {"error": "endAt content is required"}, 400
            user = User.query.get(user_id)
            if not user:
                return {"error": "User not found"}, 404
                
            # Check if role exists
            role = Role.query.get(role_id)
            if not role:
                return {"error": "Role not found"}, 404
                
            # Check if relationship already exists
            existing = UserRole.query.filter_by(
                user_id=user_id, 
                role_id=role_id
            ).first()
            
            if existing:
                return {"error": "This user already has this role"}, 400
            
            # Process optional data
            if data is None:
                data = {}
            startAt = datetime.strptime(data.get('endAt'), "%Y-%m-%d %H:%M:%S")
            endAt = datetime.strptime(data.get('endAt'), "%Y-%m-%d %H:%M:%S")
            new_user_role = UserRole(
                id=str(uuid.uuid4()),
                user_id=user_id,
                role_id=role_id,
                startAt=startAt,
                endAt=endAt
            )
            
            db.session.add(new_user_role)
            db.session.commit()
            
            return new_user_role.to_dict(), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def update(user_role_id, data):
        """Update a user-role relationship"""
        try:
            user_role = UserRole.query.get(user_role_id)
            if not user_role:
                return {"error": "User-Role relationship not found"}, 404
            
            if 'startAt' in data:
                user_role.startAt = data['startAt']
            if 'endAt' in data:
                user_role.endAt = data['endAt']
                
            db.session.commit()
            return user_role.to_dict(), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def delete(user_role_id):
        """Delete a user-role relationship"""
        try:
            user_role = UserRole.query.get(user_role_id)
            if not user_role:
                return {"error": "User-Role relationship not found"}, 404
            
            db.session.delete(user_role)
            db.session.commit()
            
            return {"message": "User-Role relationship deleted successfully"}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500