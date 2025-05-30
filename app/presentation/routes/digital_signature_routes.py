from flask import Blueprint, request, jsonify
from app.business.controllers.digital_signature_controller import DigitalSignatureController
from flask import send_file, abort,send_from_directory
import os
from flask import current_app
digital_signature_bp = Blueprint('digital_signature_bp', __name__)

@digital_signature_bp.route('/', methods=['GET'])
def get_all_signatures():
    """Get all digital signatures"""
    result, status_code = DigitalSignatureController.get_all()
    return jsonify(result), status_code

@digital_signature_bp.route('/<int:signature_id>', methods=['GET'])
def get_signature(signature_id):
    """Get a specific digital signature by ID"""
    result, status_code = DigitalSignatureController.get_by_id(signature_id)
    return jsonify(result), status_code

@digital_signature_bp.route('/user/<int:user_id>', methods=['GET'])
def get_signature_by_user(user_id):
    """Get a digital signature by user ID"""
    result, status_code = DigitalSignatureController.get_by_user_id(user_id)
    return jsonify(result), status_code

@digital_signature_bp.route('/user/<int:user_id>', methods=['POST'])
def create_signature(user_id):
    """Create a new digital signature for a user"""
    photo = request.files.get('photo')
    result, status_code = DigitalSignatureController.create(user_id, photo)
    return jsonify(result), status_code

@digital_signature_bp.route('/<int:signature_id>', methods=['PUT'])
def update_signature(signature_id):
    """Update a digital signature"""
    photo = request.files.get('photo')
    result, status_code = DigitalSignatureController.update(signature_id, photo)
    return jsonify(result), status_code

@digital_signature_bp.route('/<int:signature_id>', methods=['DELETE'])
def delete_signature(signature_id):
    """Delete a digital signature"""
    result, status_code = DigitalSignatureController.delete(signature_id)
    return jsonify(result), status_code
@digital_signature_bp.route('/<path:filename>', methods=['GET'])
def get_image(filename):
    image_path = os.path.join(current_app.root_path,'static' ,'uploads', 'digital-signatures', filename)
    if os.path.isfile(image_path):
        return send_file(image_path, mimetype='image/png')