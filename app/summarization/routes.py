from flask import Blueprint, request, jsonify
from .utils import extract_text
from .summarizer.py import summarize_text
from flask_jwt_extended import jwt_required

summarization_bp = Blueprint('summarization', __name__)

@summarization_bp.route('/summarize', methods=['POST'])
@jwt_required()
def summarize():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    try:
        raw_text = extract_text(file)
        summary = summarize_text(raw_text)
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
