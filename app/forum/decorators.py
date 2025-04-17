from flask_login import current_user
from functools import wraps
from flask import abort

def doctor_only(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.profile.role != 'doctor':
            return abort(403)
        return fn(*args, **kwargs)
    return wrapper
