# decorators.py
from functools import wraps
from flask import redirect, url_for, abort
from flask_login import current_user

def patient_only(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.profile.role != 'patient':
            return abort(403)
        return fn(*args, **kwargs)
    return wrapper
