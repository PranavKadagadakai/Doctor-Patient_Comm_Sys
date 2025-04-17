# routes.py
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from .models import MedicalEntry
from .decorators import patient_only
from ..extensions import db
from datetime import datetime

tracker_bp = Blueprint('tracker', __name__)

@tracker_bp.route('/', methods=['GET'])
@login_required
@patient_only
def tracker_page():
    entries = MedicalEntry.query.filter_by(user_id=current_user.id).order_by(MedicalEntry.date.desc()).limit(5).all()
    return render_template('tracker.html', entries=entries)

@tracker_bp.route('/full-history')
@login_required
def full_history():
    entries = MedicalEntry.query.filter_by(user_id=current_user.id).order_by(MedicalEntry.date.desc()).all()
    return render_template('tracker_full_history.html', entries=entries)

from flask import redirect, url_for, flash

@tracker_bp.route('/entries', methods=['POST'])
@login_required
@patient_only
def add_entry():
    data = request.form
    entry = MedicalEntry(
        user_id=current_user.id,
        entry_type=data['entry_type'],
        description=data['description'],
        date=datetime.strptime(data['date'], '%Y-%m-%d') if data.get('date') else datetime.utcnow()
    )
    db.session.add(entry)
    db.session.commit()
    flash("Entry added successfully!", "success")
    return redirect(url_for('tracker.tracker_page'))

@tracker_bp.route('/entries', methods=['GET'])
@login_required
@patient_only
def get_user_entries():
    entries = MedicalEntry.query.filter_by(user_id=current_user.id).order_by(MedicalEntry.date.asc()).all()
    return jsonify([
        {
            "id": e.id,
            "entry_type": e.entry_type,
            "description": e.description,
            "date": e.date.strftime('%Y-%m-%d')
        } for e in entries
    ])
