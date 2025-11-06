from flask import Blueprint, render_template, request
from app import shared, db
import json
import random


bp = Blueprint('frontend', __name__, url_prefix='/frontend')


@bp.route('/random_question', methods=['GET'])
def question():
    return render_template("question.html", type="c1")

@bp.route('/check_answer', methods=['GET','POST'])
def check():
    if request.method == 'POST':
        id = request.form.get('question_id')
        user_answer = int (request.form.get('answer'))
        q = shared.get_question_by_id(id)

        correct = shared.check_answer (id, user_answer)
        review_mode = request.args.get('review', '0') in ['1', 'true', 'True']

        


    return render_template ('check_question.html', question = q, correct = correct, review_mode = review_mode)


@bp.route("/review_failed")
def review_failed():
    return render_template("review_failed.html")


