from flask import Blueprint, jsonify
from app.db import get_db
import json 
bp = Blueprint('api', __name__, url_prefix='/api')



def get_question_by_id(id):
    data = get_db()
    question = data.execute(
        "SELECT * FROM all_questions WHERE id = ?", (id,)
    ).fetchone()
    db_types_rows = data.execute(
                    "SELECT type FROM question_types WHERE question_id = ?", (id,)
                ).fetchall()
    db_types = [row["type"] for row in db_types_rows]
    if question:
        return {
            "id": question[0],
            "title": question[1],
            "answer_0": question[2],
            "answer_1": question[3],
            "answer_2": question[4],
            "answer_3": question[5],
            "correct_answer": question[6],
            "category": question[7],
            "image": question[8],
            "types": db_types
        }
 


def check_answer (id, user_answer):
        if id not in range (0,1805) or id is not int:
            message = f"bad id"

        if user_answer not in range (0, 3) or user_answer is not int:
            message = f'bad answer'

        if user_answer is None:
            message = f'no answer'
            
        q = get_question_by_id(id)
        if user_answer == q ['correct_answer']:
            return  True
        else:
            return False
            






