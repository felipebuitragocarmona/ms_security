from flask import Blueprint, request, jsonify
from app.business.controllers.device_controller import DeviceController

device_bp = Blueprint('device_bp', __name__)

@device_bp.route('/', methods=['GET'])
def get_all_devices():
    """Get all devices"""
    result, status_code = DeviceController.get_all()
    return jsonify(result), status_code

@device_bp.route('/<int:device_id>', methods=['GET'])
def get_device(device_id):
    """Get a specific device by ID"""
    result, status_code = DeviceController.get_by_id(device_id)
    return jsonify(result), status_code

@device_bp.route('/user/<int:user_id>', methods=['GET'])
def get_devices_by_user(user_id):
    """Get all devices for a specific user"""
    result, status_code = DeviceController.get_by_user_id(user_id)
    return jsonify(result), status_code

@device_bp.route('/user/<int:user_id>', methods=['POST'])
def create_device(user_id):
    """Create a new device for a user"""
    data = request.json
    result, status_code = DeviceController.create(user_id, data)
    return jsonify(result), status_code

@device_bp.route('/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    """Update a device"""
    data = request.json
    result, status_code = DeviceController.update(device_id, data)
    return jsonify(result), status_code

@device_bp.route('/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    """Delete a device"""
    result, status_code = DeviceController.delete(device_id)
    return jsonify(result), status_code
