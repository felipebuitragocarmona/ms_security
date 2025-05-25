from flask import Blueprint, request, jsonify
from app.business.controllers.user_role_controller import UserRoleController

user_role_bp = Blueprint('user_role_bp', __name__)

@user_role_bp.route('/', methods=['GET'])
def get_all_user_roles():
    """Get all user-role relationships"""
    result, status_code = UserRoleController.get_all()
    return jsonify(result), status_code

@user_role_bp.route('/<string:user_role_id>', methods=['GET'])
def get_user_role(user_role_id):
    """Get a specific user-role relationship by ID"""
    result, status_code = UserRoleController.get_by_id(user_role_id)
    return jsonify(result), status_code

@user_role_bp.route('/user/<int:user_id>', methods=['GET'])
def get_roles_by_user(user_id):
    """Get all roles for a specific user"""
    result, status_code = UserRoleController.get_by_user_id(user_id)
    return jsonify(result), status_code

@user_role_bp.route('/role/<int:role_id>', methods=['GET'])
def get_users_by_role(role_id):
    """Get all users for a specific role"""
    result, status_code = UserRoleController.get_by_role_id(role_id)
    return jsonify(result), status_code

@user_role_bp.route('/user/<int:user_id>/role/<int:role_id>', methods=['POST'])
def create_user_role(user_id, role_id):
    """Create a new user-role relationship"""
    data = request.json
    result, status_code = UserRoleController.create(user_id, role_id, data)
    return jsonify(result), status_code

@user_role_bp.route('/<string:user_role_id>', methods=['PUT'])
def update_user_role(user_role_id):
    """Update a user-role relationship"""
    data = request.json
    result, status_code = UserRoleController.update(user_role_id, data)
    return jsonify(result), status_code

@user_role_bp.route('/<string:user_role_id>', methods=['DELETE'])
def delete_user_role(user_role_id):
    """Delete a user-role relationship"""
    result, status_code = UserRoleController.delete(user_role_id)
    return jsonify(result), status_code