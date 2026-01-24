from flask import Blueprint, render_template, request, redirect, url_for, session
from app import shared, api
import random
import json
bp = Blueprint('frontend', __name__, url_prefix='/frontend')


@bp.route('/random_question', methods=['GET'])
def question():
    select_type = request.cookies.get("type")
    if select_type is None:
        return redirect(url_for('frontend.select_type'))
    else:
        return render_template("question.html", type=select_type)

@bp.route('/check_answer', methods=['GET','POST'])
def check():
    id = request.form.get('question_id')
    user_answer = int (request.form.get('answer'))
    q = shared.get_question_by_id(id)

    correct = shared.check_answer (id, user_answer)
    review_mode = request.args.get('review', '0') in ['1', 'true', 'True']

        


    return render_template ('check_question.html', question = q, correct = correct, review_mode = review_mode)


@bp.route("/review_failed")
def review_failed():
    return render_template("review_failed.html")



@bp.route("/select_type")
def select_type():
    return render_template("select_type.html")


@bp.route("/save_type", methods=['POST'])
def save_type():
    selected_type = request.form["question_type"]
    resp = redirect(url_for('index'))
    resp.set_cookie("type", selected_type, max_age=60*60*24*365, httponly=True,
        secure=True,
        samesite="Lax")  # 1 year)
    return resp

@bp.route("/test/start")
def start_test():
    selected_type = request.cookies.get("type")
    if not selected_type:
        return "Error: No type selected", 400

    questions = api.get_type_questions(selected_type)
    questions_list = questions.get_json()  

    if not questions_list or len(questions_list) < 30:
        return "Error: Not enough questions for this type", 400

    selected_questions = random.sample(questions_list, k=30)

    session["test"] = {
        "question_ids": [q["id"] for q in selected_questions],
        "current_index": 0,
        "correct_count": 0,
        "answers": {}
    }

    return redirect(url_for("frontend.test_question"))

@bp.route("/test/question")
def test_question():
    test = session.get("test")
    if not test:
        return redirect(url_for("frontend.start_test"))

    idx = test["current_index"]

    if idx >= 30:
        return redirect(url_for("frontend.test_result"))

    question_id = test["question_ids"][idx]
    question = shared.get_question_by_id(question_id)

    print 

    return render_template(
        "test_question.html",
        question=question,
        index=idx + 1,
        total=30
    )


@bp.route("/test/answer", methods=["POST"])
def test_answer():
    test = session["test"]
    question_id = int(request.form["question_id"])
    selected = int(request.form["answer"])

    correct = shared.check_answer(question_id, selected)

    test["answers"][question_id] = selected
    if correct:
        test["correct_count"] += 1

    test["current_index"] += 1
    session.modified = True

    return redirect(url_for("frontend.test_question"))

@bp.route("/test/result")
def test_result():
    test = session.get("test")
    if not test:
        return redirect(url_for("start_test"))

    passed = test["correct_count"] >= 26

    return render_template(
        "test_result.html",
        score=test["correct_count"],
        passed=passed
    )
