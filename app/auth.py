import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

import sqlite3

bp = Blueprint('auth', __name__, url_prefix='/auth')



@bp.route ("/register", methods = ['GET','POST'])
def register():
    if request.method == 'POST':

        db = get_db()
        error = None
        username = request.form ["username"]
        password = request.form ["password"]
        if not username:
            error ="Username Required"  
        if not password:
            error ="PassworD Required"  

        if error is None:
            try:
                if request.method == 'POST':
                    db.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, 
                                                                            generate_password_hash(password)))
                    db.commit()
            except sqlite3.IntegrityError:
                error = f"User {username} is already registered."

            else:
                return redirect(url_for("auth.login"))
            
        flash (error)
    return render_template('register.html')
            

@bp.route ("/login", methods = ['GET','POST'])
def login():
    db = get_db()

    if request.method == 'POST':

        error = None
        username = request.form ["username"]
        password = request.form ["password"]
        user = db.execute("SELECT * FROM user WHERE username = ?", (username, )).fetchone()
        if user is None:
             error = "incorrect username"
    
        elif not check_password_hash(user ["password"], password): 
                        error = f"Incorrect password."

                
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        
        flash(error)
        return render_template('login.html')



    

    return render_template('login.html')



@bp.before_app_request
def load_logged_in_user():
     user_id = session.get('user_id')

     if user_id is None:
          g.user = None
     else:
          g.user = get_db().execute ('SELECT * FROM user WHERE id = ?', (user_id, )).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        

        return view(**kwargs)

    return wrapped_view
