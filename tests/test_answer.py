from app import config
from app.db import get_db
from app.question_make import questionmaker
import csv

def load_table():
    table_path = config.paths ['test_table']

def test_database_has_6_rows(app):
    with app.app_context():  # <-- this pushes the app context
        data = get_db()  # now it's safe to use get_db()
        count = data.execute("SELECT COUNT(*) FROM all_questions").fetchone()[0]
        assert count == 6

def test_correct(client):
    tablepath = config.paths ['test_table']
    maker = questionmaker(None)
    with open(tablepath, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        for i, row in enumerate (reader, start=2):
            title_dict = maker.splitTitle (row["title2"])
            id = title_dict['id']
            readtext = maker.readHTML(row["description4"])
            correct_answer = readtext["correct_answer"]

            response = client.post('/check', data={
                'question_id': id,
                'answer': correct_answer,
            })

            assert response.status_code == 200
            body = response.data.decode()
            print ("hi")
            assert f"he was correct" in body



    