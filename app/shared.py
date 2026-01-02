from app.db import get_db
from flask import url_for
from urllib.parse import urlparse, unquote
import os


def filename_from_url(url, fallback="downloaded_file"):
    parsed = urlparse(url)
    path = unquote(parsed.path or "")
    name = os.path.basename(path)
    if name and "." in name:
        return name
    # fallback to hostname + simple suffix
    host = parsed.netloc.replace(":", "_") or "host"
    return f"{host}_{fallback}"

def get_question_by_id(id):
    db = get_db()

    question = db.execute(
        "SELECT * FROM all_questions WHERE id = ?",
        (id,)
    ).fetchone()

    if not question:
        return None

    db_types_rows = db.execute(
        "SELECT type FROM question_types WHERE question_id = ?",
        (id,)
    ).fetchall()

    db_types = [row["type"] for row in db_types_rows]

    image_url = (
        url_for("static", filename=f"images/{filename_from_url (question['image'])}")
        if question["image"]
        else None
    )

    return {
        "id": question["id"],
        "title": question["title"],
        "answer_0": question["answer_0"],
        "answer_1": question["answer_1"],
        "answer_2": question["answer_2"],
        "answer_3": question["answer_3"],
        "correct_answer": question["correct_answer"],
        "category": question["category"],
        "image": image_url,
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
            






