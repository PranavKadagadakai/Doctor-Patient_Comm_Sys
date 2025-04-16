from flask import session, redirect, url_for
from functools import wraps

def login_required_ui(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'token' not in session:
            return redirect(url_for('main.login_page'))
        return fn(*args, **kwargs)
    return wrapper
