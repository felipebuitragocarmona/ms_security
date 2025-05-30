from app.data.database import db
from app.business.models.permission import Permission
from sqlalchemy.exc import SQLAlchemyError
from app.business.models.role_permission import RolePermission
class PermissionController:
    @staticmethod
    def get_all():
        """Get all permissions"""
        try:
            permissions = Permission.query.all()
            return [permission.to_dict() for permission in permissions], 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_by_id(permission_id):
        """Get a permission by ID"""
        try:
            permission = Permission.query.get(permission_id)
            if not permission:
                return {"error": "Permission not found"}, 404
            return permission.to_dict(), 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500

    @staticmethod
    def create(data):
        """Create a new permission"""
        try:
            # Validate required fields
            if 'url' not in data or 'method' not in data:
                return {"error": "URL and method are required"}, 400
            
            # Check if a permission with the same URL and method already exists
            existing = Permission.query.filter_by(
                url=data['url'],
                method=data['method'],
                entity=data['entity']
            ).first()
            
            if existing:
                return {"error": "Permission with this URL and method already exists"}, 400
                
            new_permission = Permission(
                url=data['url'],
                method=data['method'],
                entity=data['entity']
            )
            
            db.session.add(new_permission)
            db.session.commit()
            
            return new_permission.to_dict(), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def update(permission_id, data):
        """Update a permission"""
        try:
            permission = Permission.query.get(permission_id)
            if not permission:
                return {"error": "Permission not found"}, 404
            
            # If updating URL or method, check for duplicates
            if ('url' in data and data['url'] != permission.url) or \
               ('method' in data and data['method'] != permission.method):
                
                new_url = data.get('url', permission.url)
                new_method = data.get('method', permission.method)
                
                existing = Permission.query.filter_by(
                    url=new_url,
                    method=new_method,
                    entity=data['entity']
                ).first()
                
                if existing and existing.id != permission_id:
                    return {"error": "Permission with this URL and method already exists"}, 400
            
            if 'url' in data:
                permission.url = data['url']
            if 'method' in data:
                permission.method = data['method']
            if 'entity' in data:
                permission.entity = data['entity']
                
            db.session.commit()
            return permission.to_dict(), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def delete(permission_id):
        """Delete a permission"""
        try:
            permission = Permission.query.get(permission_id)
            if not permission:
                return {"error": "Permission not found"}, 404
            
            db.session.delete(permission)
            db.session.commit()
            
            return {"message": "Permission deleted successfully"}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500
    @staticmethod
    def get_grouped_permissions(role_id):
        """Obtiene los permisos agrupados por entidad e indica si el rol tiene cada permiso"""
        try:
            # Obtener todos los permisos
            permissions = Permission.query.all()

            # Obtener todos los ID de permisos asociados al rol
            role_permission_ids = db.session.query(RolePermission.permission_id)\
                                            .filter_by(role_id=role_id)\
                                            .all()
            role_permission_ids = set(pid for (pid,) in role_permission_ids)

            grouped = {}

            for p in permissions:
                permiso_dict = p.to_dict()
                permiso_dict["has_permission"] = p.id in role_permission_ids

                entity = p.entity
                if entity not in grouped:
                    grouped[entity] = []
                grouped[entity].append(permiso_dict)

            result = [{"entity": entity, "permissions": perms} for entity, perms in grouped.items()]
            return result, 200

        except SQLAlchemyError as e:
            return {"error": str(e)}, 500
"""
    @staticmethod
    def get_grouped_permissions(role_id):
        try:
            permissions = Permission.query.all()
            grouped = {}

            for p in permissions:
                entity = p.entity
                if entity not in grouped:
                    grouped[entity] = []
                grouped[entity].append(p.to_dict())

            result = [{"entity": entity, "permissions": perms} for entity, perms in grouped.items()]
            return result, 200

        except SQLAlchemyError as e:
            return {"error": str(e)}, 500
"""