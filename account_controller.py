from flask import redirect, session, flash, url_for
from functools import wraps

class AccountController:

    # login required decorator
    @staticmethod
    def login_required(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if 'logged_in' in session:
                return f(*args, **kwargs)
            else:
                flash('You need to login first.')
                return redirect(url_for('login'))
        return wrap


    def __init__(self, socketio):
        self.socketio = socketio