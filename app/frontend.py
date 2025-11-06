from flask import Blueprint, render_template, request, redirect, url_for, make_response
from app import shared


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



@bp.route("/select_type")
def select_type():
    return render_template("select_type.html")


@bp.route("/save_type", methods=['POST'])
def save_type():
    selected_type = request.form["question_type"]
    resp = redirect(url_for('frontend.question'))
    resp.set_cookie("type", selected_type, max_age=60*60*24*365, httponly=True,
        secure=True,
        samesite="Lax")  # 1 year)
    return resp
