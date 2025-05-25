from flask import Blueprint, request, jsonify
from app.business.controllers.address_controller import AddressController

address_bp = Blueprint('address_bp', __name__)

@address_bp.route('/', methods=['GET'])
def get_all_addresses():
    """Get all addresses"""
    result, status_code = AddressController.get_all()
    return jsonify(result), status_code

@address_bp.route('/<int:address_id>', methods=['GET'])
def get_address(address_id):
    """Get a specific address by ID"""
    result, status_code = AddressController.get_by_id(address_id)
    return jsonify(result), status_code

@address_bp.route('/user/<int:user_id>', methods=['GET'])
def get_address_by_user(user_id):
    """Get an address by user ID"""
    result, status_code = AddressController.get_by_user_id(user_id)
    return jsonify(result), status_code

@address_bp.route('/user/<int:user_id>', methods=['POST'])
def create_address(user_id):
    """Create a new address for a user"""
    data = request.json
    result, status_code = AddressController.create(user_id, data)
    return jsonify(result), status_code

@address_bp.route('/<int:address_id>', methods=['PUT'])
def update_address(address_id):
    """Update an address"""
    data = request.json
    result, status_code = AddressController.update(address_id, data)
    return jsonify(result), status_code

@address_bp.route('/<int:address_id>', methods=['DELETE'])
def delete_address(address_id):
    """Delete an address"""
    result, status_code = AddressController.delete(address_id)
    return jsonify(result), status_code