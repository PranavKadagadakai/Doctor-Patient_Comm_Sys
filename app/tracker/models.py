from ..extensions import db
from datetime import datetime

class MedicalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    entry_type = db.Column(db.String(50), nullable=False)  # "symptom", "medication", "diagnosis"
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
