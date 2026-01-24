
from flask import Blueprint, request, jsonify
from app.db import get_db
from app.shared import get_question_by_id
bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route("/get_questions")
def get_questions():
    ids = request.args.get("ids")  # e.g. "12,34,56"
    results = []

    if ids:
        id_list = [int(i) for i in ids.split(",") if i.strip().isdigit()]
        for id in id_list:
            results.append(get_question_by_id(id))

    return jsonify(results)

    
@bp.route('/get_type_questions', methods=['GET'])
def get_type_questions (type=None):
        if type is None:
            type = request.args.get("type") 
        data = get_db()
        db_types_rows = data.execute(
                        "SELECT DISTINCT question_id FROM question_types WHERE type = ? COLLATE NOCASE;", (type,)  
                    ).fetchall()
        db_types = [row["question_id"] for row in db_types_rows]
        results = []
        for id in db_types:
             results.append(get_question_by_id(id))
             
        return jsonify(results)
    
@bp.route('/get_distinct_type', methods=['GET'])
def get_distinct_type ():
        type = request.args.get("type") 
        data = get_db()
        db_types_rows = data.execute(
                        "SELECT DISTINCT type FROM question_types"
                    ).fetchall()
        db_types = [row["type"] for row in db_types_rows]


        return jsonify(db_types)
