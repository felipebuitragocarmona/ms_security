from flask import Blueprint, request, jsonify
from app.business.controllers.answer_controller import AnswerController

answer_bp = Blueprint('answer_bp', __name__)

@answer_bp.route('/', methods=['GET'])
def get_all_answers():
    """Get all answers"""
    result, status_code = AnswerController.get_all()
    return jsonify(result), status_code

@answer_bp.route('/<int:answer_id>', methods=['GET'])
def get_answer(answer_id):
    """Get a specific answer by ID"""
    result, status_code = AnswerController.get_by_id(answer_id)
    return jsonify(result), status_code

@answer_bp.route('/user/<int:user_id>', methods=['GET'])
def get_answers_by_user(user_id):
    """Get all answers for a specific user"""
    result, status_code = AnswerController.get_by_user_id(user_id)
    return jsonify(result), status_code

@answer_bp.route('/question/<int:question_id>', methods=['GET'])
def get_answers_by_question(question_id):
    """Get all answers for a specific security question"""
    result, status_code = AnswerController.get_by_question_id(question_id)
    return jsonify(result), status_code

@answer_bp.route('/user/<int:user_id>/question/<int:question_id>', methods=['GET'])
def get_user_answer_for_question(user_id, question_id):
    """Get a user's answer for a specific security question"""
    result, status_code = AnswerController.get_by_user_and_question(user_id, question_id)
    return jsonify(result), status_code

@answer_bp.route('/user/<int:user_id>/question/<int:question_id>', methods=['POST'])
def create_answer(user_id, question_id):
    """Create a new answer for a user and security question"""
    data = request.json
    result, status_code = AnswerController.create(user_id, question_id, data)
    return jsonify(result), status_code

@answer_bp.route('/<int:answer_id>', methods=['PUT'])
def update_answer(answer_id):
    """Update an answer"""
    data = request.json
    result, status_code = AnswerController.update(answer_id, data)
    return jsonify(result), status_code

@answer_bp.route('/<int:answer_id>', methods=['DELETE'])
def delete_answer(answer_id):
    """Delete an answer"""
    result, status_code = AnswerController.delete(answer_id)
    return jsonify(result), status_code