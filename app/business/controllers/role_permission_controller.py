import uuid
from datetime import datetime
from app.data.database import db
from app.business.models.role_permission import RolePermission
from app.business.models.role import Role
from app.business.models.permission import Permission
from sqlalchemy.exc import SQLAlchemyError

class RolePermissionController:
    @staticmethod
    def get_all():
        """Get all role-permission relationships"""
        try:
            role_permissions = RolePermission.query.all()
            return [rp.to_dict() for rp in role_permissions], 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_by_id(role_permission_id):
        """Get a role-permission relationship by ID"""
        try:
            role_permission = RolePermission.query.get(role_permission_id)
            if not role_permission:
                return {"error": "Role-Permission relationship not found"}, 404
            return role_permission.to_dict(), 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500
    
    @staticmethod
    def get_by_role_id(role_id):
        """Get all permissions for a specific role"""
        try:
            role_permissions = RolePermission.query.filter_by(role_id=role_id).all()
            return [rp.to_dict() for rp in role_permissions], 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500
    
    @staticmethod
    def get_by_permission_id(permission_id):
        """Get all roles for a specific permission"""
        try:
            role_permissions = RolePermission.query.filter_by(permission_id=permission_id).all()
            return [rp.to_dict() for rp in role_permissions], 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500

    @staticmethod
    def create(role_id, permission_id, data=None):
        """Create a new role-permission relationship"""
        try:
            # Check if role exists
            role = Role.query.get(role_id)
            if not role:
                return {"error": "Role not found"}, 404
                
            # Check if permission exists
            permission = Permission.query.get(permission_id)
            if not permission:
                return {"error": "Permission not found"}, 404
                
            # Check if relationship already exists
            existing = RolePermission.query.filter_by(
                role_id=role_id, 
                permission_id=permission_id
            ).first()
            
            if existing:
                return {"error": "This role already has this permission"}, 400
            
            # Process optional data
            if data is None:
                data = {}
                
            new_role_permission = RolePermission(
                id=str(uuid.uuid4()),
                role_id=role_id,
                permission_id=permission_id
            )
            
            db.session.add(new_role_permission)
            db.session.commit()
            
            return new_role_permission.to_dict(), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500


    @staticmethod
    def delete(role_id, permission_id):
        """Delete a role-permission relationship by role and permission IDs"""
        try:
            role_permission = RolePermission.query.filter_by(
                role_id=role_id,
                permission_id=permission_id
            ).first()
            
            if not role_permission:
                return {"error": "Role-Permission relationship not found"}, 404
            
            db.session.delete(role_permission)
            db.session.commit()
            
            return {"message": "Role-Permission relationship deleted successfully"}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500
    
    @staticmethod
    def delete_by_id(role_permission_id):
        """Delete a role-permission relationship by ID"""
        try:
            role_permission = RolePermission.query.get(role_permission_id)
            if not role_permission:
                return {"error": "Role-Permission relationship not found"}, 404
            
            db.session.delete(role_permission)
            db.session.commit()
            
            return {"message": "Role-Permission relationship deleted successfully"}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500