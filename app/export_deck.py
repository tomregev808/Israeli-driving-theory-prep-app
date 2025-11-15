



import genanki
from flask import request, send_file, Blueprint
import requests
from app.shared import get_question_by_id
bp = Blueprint('export_deck', __name__, url_prefix='/export_deck')
import os
MODEL_ID = 1234567890
DECK_ID = 9876543210

anki_model = genanki.Model(
    MODEL_ID,
    'Driving Theory Model',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Question}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
        },
    ])

@bp.route("/", methods=["POST"], strict_slashes=False)
def anki_export():
    data = request.get_json()
    ids = data.get("ids", [])

    deck = genanki.Deck(DECK_ID, "Driving Theory Practice")
    media_files = []

    for qid in ids:
        q = get_question_by_id(qid)

        # Build question front
        question_html = f"<b>{q['title']}</b><br>"
        if q["image"]:
            # Download image locally
            img_filename = f"img_{qid}.jpg"
            img_path = os.path.join("/tmp", img_filename)
            r = requests.get(q["image"])
            with open(img_path, "wb") as f:
                f.write(r.content)
            question_html += f'<img src="{img_filename}"><br>'
            media_files.append(img_path)

        # Add answers
        question_html += "<ol>"
        for i in range(4):
            question_html += f"<li>{q[f'answer_{i}']}</li>"
        question_html += "</ol>"

        # Back side (correct answer)
        answer_html = f"<b>נכון:</b> {q['correct_answer']}"

        note = genanki.Note(
            model=anki_model,
            fields=[question_html, answer_html]
        )

        deck.add_note(note)

    # Export deck
    pkg = genanki.Package(deck)
    pkg.media_files = media_files
    outpath = "/tmp/driving_deck.apkg"
    pkg.write_to_file(outpath)

    return send_file(outpath, as_attachment=True, download_name="driving_deck.apkg")
