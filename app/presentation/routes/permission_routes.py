from flask import Blueprint, request, jsonify
from app.business.controllers.permission_controller import PermissionController

permission_bp = Blueprint('permission_bp', __name__)

@permission_bp.route('/', methods=['GET'])
def get_all_permissions():
    """Get all permissions"""
    result, status_code = PermissionController.get_all()
    return jsonify(result), status_code

@permission_bp.route('/<int:permission_id>', methods=['GET'])
def get_permission(permission_id):
    """Get a specific permission by ID"""
    result, status_code = PermissionController.get_by_id(permission_id)
    return jsonify(result), status_code

@permission_bp.route('/', methods=['POST'])
def create_permission():
    """Create a new permission"""
    data = request.json
    result, status_code = PermissionController.create(data)
    return jsonify(result), status_code

@permission_bp.route('/<int:permission_id>', methods=['PUT'])
def update_permission(permission_id):
    """Update a permission"""
    data = request.json
    result, status_code = PermissionController.update(permission_id, data)
    return jsonify(result), status_code

@permission_bp.route('/<int:permission_id>', methods=['DELETE'])
def delete_permission(permission_id):
    """Delete a permission"""
    result, status_code = PermissionController.delete(permission_id)
    return jsonify(result), status_code
@permission_bp.route('/grouped/role/<int:role_id>', methods=['GET'])
def get_permissions_grouped(role_id):
    return PermissionController.get_grouped_permissions(role_id)