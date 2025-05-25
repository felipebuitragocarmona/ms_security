from flask import Blueprint, request, jsonify
from app.business.controllers.password_controller import PasswordController

password_bp = Blueprint('password_bp', __name__)

@password_bp.route('/', methods=['GET'])
def get_all_passwords():
    """Get all passwords"""
    result, status_code = PasswordController.get_all()
    return jsonify(result), status_code

@password_bp.route('/<int:password_id>', methods=['GET'])
def get_password(password_id):
    """Get a specific password by ID"""
    result, status_code = PasswordController.get_by_id(password_id)
    return jsonify(result), status_code

@password_bp.route('/user/<int:user_id>', methods=['GET'])
def get_passwords_by_user(user_id):
    """Get all passwords for a specific user"""
    result, status_code = PasswordController.get_by_user_id(user_id)
    return jsonify(result), status_code

@password_bp.route('/user/<int:user_id>/current', methods=['GET'])
def get_current_password(user_id):
    """Get the current password for a specific user"""
    result, status_code = PasswordController.get_current_password(user_id)
    return jsonify(result), status_code

@password_bp.route('/user/<int:user_id>', methods=['POST'])
def create_password(user_id):
    """Create a new password for a user"""
    data = request.json
    result, status_code = PasswordController.create(user_id, data)
    return jsonify(result), status_code

@password_bp.route('/<int:password_id>', methods=['PUT'])
def update_password(password_id):
    """Update a password"""
    data = request.json
    result, status_code = PasswordController.update(password_id, data)
    return jsonify(result), status_code

@password_bp.route('/<int:password_id>', methods=['DELETE'])
def delete_password(password_id):
    """Delete a password"""
    result, status_code = PasswordController.delete(password_id)
    return jsonify(result), status_code