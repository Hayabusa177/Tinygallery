import functools
import time
import json
import re
from flask import(
    Blueprint, flash, g, redirect, 
    render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from tinyGallery.db import get_db
    

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        regular_expression_pattern = "^[A-Za-z0-9]+$"
        user_name_length_limit = 12

        username = request.form.get("registerUserName")
        password = request.form.get("registerPassword")
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        db = get_db()

        error = None

        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"
        elif not re.match(regular_expression_pattern,username):
            error = "Username must be a combination of letters and numbers"
        elif not re.match(regular_expression_pattern, password):
            error = "Username must be a combination of letters and numbers"
        elif not len(username) <= user_name_length_limit:
            error = "The length of username must be less 12 or equal to  12"
        
        if error is None:
            try:
                db.execute(
                    "INSERT INTO users (userName, passWord, date) VALUES(?, ?, ?)",
                    (username, password, date),
                )
                db.commit()
            except db.IntegrityError:
                erorr = f"User {username} is alreadyy registered"
            else:
                return redirect(url_for("index_page"))
        flash(error)
    return "<h1>" + error + "</h1>"

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        regular_expression_pattern = "^[A-Za-z0-9]+$"
        user_name_length_limit = 12

        username = request.form.get("loginUserName")
        password = request.form.get("loginPassword")

        db = get_db()

        error = None

        user = db.execute(
            'SELECT * FROM users WHERE userName = ?', (username,)
        ).fetchone()

        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"
        elif not re.match(regular_expression_pattern,username):
            error = "Username must be a combination of letters and numbers"
        elif not re.match(regular_expression_pattern, password):
            error = "Username must be a combination of letters and numbers"
        elif not len(username) <= user_name_length_limit:
            error = "The length of username must be less 12 or equal to  12"
        elif user is None:
            error = 'Incorrect username.'
        elif password != str(user['passWord']):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['userName']
            return redirect(url_for('index_page'))

        flash(error)
        return error

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE userName = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index_page'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view