import sqlite3
from flask import Flask, render_template
import os
from app import db
from flask import jsonify


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    #remember changing the config!!!!!
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'db.sqlite'),
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent = True)
    else:
        app.config.from_mapping (test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    db.init_app(app)

    @app.route('/', methods=['GET'])
    def index():
        data = db.get_db()
        test = data.execute(
            "SELECT title, answer_0, answer_1 FROM all_questions WHERE id = ?", (434,)
        ).fetchall()
        if test:
            # Convert row to dictionary with column names
            result = {
                "title": test[0][0],
                "answer_0": test[0][1], 
                "answer_1": test[0][2]
            }
        return jsonify(result)

    return app



