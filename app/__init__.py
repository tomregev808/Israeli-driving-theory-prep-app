import sqlite3
from flask import Flask, render_template
import os
from app import db
from flask import jsonify
import random

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


    @app.route('/random_question', methods=['GET', 'POST'])
    def random_question():
        data = db.get_db()
        
        # Get a random question ID
        max_id = data.execute("SELECT MAX(id) FROM all_questions").fetchone()[0]
        random_id = random.randint(1, max_id)
        
        question = data.execute(
            "SELECT * FROM all_questions WHERE id = ?", (random_id,)
        ).fetchone()
        
        if question:
            # Assuming columns: id, title, answer_0, answer_1, answer_2, answer_3
            q = {
                "id": question[0],
                "title": question[1],
                "answer_0": question[2], 
                "answer_1": question[3],
                "answer_2": question[4],
                "answer_3": question[5],
                "correct_answer": question[6],
                "category": question[7],
                "image": question[8]
            }
            return render_template("question.html", question=q)
        else:
            return jsonify({"error": "Question not found"}), 404

    @app.route('/', methods=['GET'])
    def index():
        return jsonify("hi")


    @app.route('/check', methods=['GET', 'POST'])
    def check_answer():
        return jsonify("hi")
    return app



