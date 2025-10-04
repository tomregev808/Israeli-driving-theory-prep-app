
from flask import Blueprint, request, jsonify
from app.db import get_db
from app.shared import get_question_by_id
bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route("/get_questions")
def get_failed_questions():
    ids = request.args.get("ids")  # e.g. "12,34,56"
    results = []


    for id in ids:
        results.append(get_question_by_id (id))

    return jsonify(results)

    
