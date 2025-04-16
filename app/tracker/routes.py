from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import MedicalEntry
from .decorators import patient_only
from ..extensions import db
from datetime import datetime

tracker_bp = Blueprint('tracker', __name__)

@tracker_bp.route('/entries', methods=['POST'])
@jwt_required()
@patient_only
def add_entry():
    data = request.get_json()
    identity = get_jwt_identity()

    entry = MedicalEntry(
        user_id=identity['id'],
        entry_type=data['entry_type'],
        description=data['description'],
        date=datetime.strptime(data['date'], '%Y-%m-%d') if 'date' in data else datetime.utcnow()
    )
    db.session.add(entry)
    db.session.commit()
    return jsonify({"msg": "Entry added", "id": entry.id}), 201

@tracker_bp.route('/entries', methods=['GET'])
@jwt_required()
def get_user_entries():
    identity = get_jwt_identity()
    entries = MedicalEntry.query.filter_by(user_id=identity['id']).order_by(MedicalEntry.date.asc()).all()
    return jsonify([{
        "id": e.id,
        "entry_type": e.entry_type,
        "description": e.description,
        "date": e.date.strftime('%Y-%m-%d')
    } for e in entries])
