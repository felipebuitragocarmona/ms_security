from flask import Blueprint, request, jsonify
from app.business.controllers.role_controller import RoleController

role_bp = Blueprint('role_bp', __name__)

@role_bp.route('/', methods=['GET'])
def get_all_roles():
    """Get all roles"""
    result, status_code = RoleController.get_all()
    return jsonify(result), status_code

@role_bp.route('/<int:role_id>', methods=['GET'])
def get_role(role_id):
    """Get a specific role by ID"""
    result, status_code = RoleController.get_by_id(role_id)
    return jsonify(result), status_code

@role_bp.route('/', methods=['POST'])
def create_role():
    """Create a new role"""
    data = request.json
    result, status_code = RoleController.create(data)
    return jsonify(result), status_code

@role_bp.route('/<int:role_id>', methods=['PUT'])
def update_role(role_id):
    """Update a role"""
    data = request.json
    result, status_code = RoleController.update(role_id, data)
    return jsonify(result), status_code

@role_bp.route('/<int:role_id>', methods=['DELETE'])
def delete_role(role_id):
    """Delete a role"""
    result, status_code = RoleController.delete(role_id)
    return jsonify(result), status_code