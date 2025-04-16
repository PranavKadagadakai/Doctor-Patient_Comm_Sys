from flask_jwt_extended import get_jwt_identity
from functools import wraps
from flask import jsonify

def patient_only(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        if identity.get('role') != 'patient':
            return jsonify({"error": "Patients only"}), 403
        return fn(*args, **kwargs)
    return wrapper
