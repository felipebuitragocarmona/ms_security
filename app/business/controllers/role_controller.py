from app.data.database import db
from app.business.models.role import Role
from sqlalchemy.exc import SQLAlchemyError

class RoleController:
    @staticmethod
    def get_all():
        """Get all roles"""
        try:
            roles = Role.query.all()
            return [role.to_dict() for role in roles], 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_by_id(role_id):
        """Get a role by ID"""
        try:
            role = Role.query.get(role_id)
            if not role:
                return {"error": "Role not found"}, 404
            return role.to_dict(), 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500

    @staticmethod
    def create(data):
        """Create a new role"""
        try:
            # Validate required fields
            if 'name' not in data:
                return {"error": "Role name is required"}, 400
            
            # Check if role with the same name already exists
            if Role.query.filter_by(name=data['name']).first():
                return {"error": "Role with this name already exists"}, 400
                
            new_role = Role(
                name=data['name'],
                description=data.get('description', '')
            )
            
            db.session.add(new_role)
            db.session.commit()
            
            return new_role.to_dict(), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def update(role_id, data):
        """Update a role"""
        try:
            role = Role.query.get(role_id)
            if not role:
                return {"error": "Role not found"}, 404
            
            if 'name' in data:
                # Check if the new name is already in use by another role
                existing_role = Role.query.filter_by(name=data['name']).first()
                if existing_role and existing_role.id != role_id:
                    return {"error": "Role name already in use"}, 400
                role.name = data['name']
                
            if 'description' in data:
                role.description = data['description']
                
            db.session.commit()
            return role.to_dict(), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def delete(role_id):
        """Delete a role"""
        try:
            role = Role.query.get(role_id)
            if not role:
                return {"error": "Role not found"}, 404
            
            db.session.delete(role)
            db.session.commit()
            
            return {"message": "Role deleted successfully"}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500