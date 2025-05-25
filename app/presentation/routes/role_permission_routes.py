from flask import Blueprint, request, jsonify
from app.business.controllers.role_permission_controller import RolePermissionController

role_permission_bp = Blueprint('role_permission_bp', __name__)

@role_permission_bp.route('/', methods=['GET'])
def get_all_role_permissions():
    """Get all role-permission relationships"""
    result, status_code = RolePermissionController.get_all()
    return jsonify(result), status_code

@role_permission_bp.route('/<string:role_permission_id>', methods=['GET'])
def get_role_permission(role_permission_id):
    """Get a specific role-permission relationship by ID"""
    result, status_code = RolePermissionController.get_by_id(role_permission_id)
    return jsonify(result), status_code

@role_permission_bp.route('/role/<int:role_id>', methods=['GET'])
def get_permissions_by_role(role_id):
    """Get all permissions for a specific role"""
    result, status_code = RolePermissionController.get_by_role_id(role_id)
    return jsonify(result), status_code

@role_permission_bp.route('/permission/<int:permission_id>', methods=['GET'])
def get_roles_by_permission(permission_id):
    """Get all roles for a specific permission"""
    result, status_code = RolePermissionController.get_by_permission_id(permission_id)
    return jsonify(result), status_code

@role_permission_bp.route('/role/<int:role_id>/permission/<int:permission_id>', methods=['POST'])
def create_role_permission(role_id, permission_id):
    """Create a new role-permission relationship"""
    data = request.json
    print("role_id",role_id)
    print("permission_id", permission_id)
    result, status_code = RolePermissionController.create(role_id, permission_id, data)
    return jsonify(result), status_code

@role_permission_bp.route('/<string:role_permission_id>', methods=['PUT'])
def update_role_permission(role_permission_id):
    """Update a role-permission relationship"""
    data = request.json
    result, status_code = RolePermissionController.update(role_permission_id, data)
    return jsonify(result), status_code

@role_permission_bp.route('/role/<int:role_id>/permission/<int:permission_id>', methods=['DELETE'])
def delete_role_permission(role_id, permission_id):
    """Delete a role-permission relationship by role and permission IDs"""
    result, status_code = RolePermissionController.delete(role_id, permission_id)
    return jsonify(result), status_code

@role_permission_bp.route('/<string:role_permission_id>', methods=['DELETE'])
def delete_role_permission_by_id(role_permission_id):
    """Delete a role-permission relationship by ID"""
    result, status_code = RolePermissionController.delete_by_id(role_permission_id)
    return jsonify(result), status_code