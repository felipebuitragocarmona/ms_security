from flask import Blueprint, request, jsonify
from app.business.controllers.security_question_controller import SecurityQuestionController

security_question_bp = Blueprint('security_question_bp', __name__)

@security_question_bp.route('/', methods=['GET'])
def get_all_security_questions():
    """Get all security questions"""
    result, status_code = SecurityQuestionController.get_all()
    return jsonify(result), status_code

@security_question_bp.route('/<int:question_id>', methods=['GET'])
def get_security_question(question_id):
    """Get a specific security question by ID"""
    result, status_code = SecurityQuestionController.get_by_id(question_id)
    return jsonify(result), status_code

@security_question_bp.route('/', methods=['POST'])
def create_security_question():
    """Create a new security question"""
    data = request.json
    result, status_code = SecurityQuestionController.create(data)
    return jsonify(result), status_code

@security_question_bp.route('/<int:question_id>', methods=['PUT'])
def update_security_question(question_id):
    """Update a security question"""
    data = request.json
    result, status_code = SecurityQuestionController.update(question_id, data)
    return jsonify(result), status_code

@security_question_bp.route('/<int:question_id>', methods=['DELETE'])
def delete_security_question(question_id):
    """Delete a security question"""
    result, status_code = SecurityQuestionController.delete(question_id)
    return jsonify(result), status_code