from flask import Blueprint, request, jsonify
from app.business.controllers.user_controller import UserController

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/', methods=['GET'])
def get_all_users():
    """Get all users"""
    result, status_code = UserController.get_all()
    return jsonify(result), status_code

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user by ID"""
    result, status_code = UserController.get_by_id(user_id)
    return jsonify(result), status_code

@user_bp.route('/', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.json
    result, status_code = UserController.create(data)
    return jsonify(result), status_code

@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a user"""
    data = request.json
    result, status_code = UserController.update(user_id, data)
    return jsonify(result), status_code

@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    result, status_code = UserController.delete(user_id)
    return jsonify(result), status_code