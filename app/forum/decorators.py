from flask_jwt_extended import get_jwt_identity
from functools import wraps
from flask import jsonify

def doctor_only(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        if identity.get('role') != 'doctor':
            return jsonify({"error": "Doctor access only"}), 403
        return fn(*args, **kwargs)
    return wrapper
