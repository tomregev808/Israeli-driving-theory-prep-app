from app import config
from app.db import get_db
from app.question_make import questionmaker
import csv

    


def load_table():
    table_path = config.paths ['test_table']

def test_database_has_20_rows(app):
    with app.app_context(): 
        data = get_db()  
        count = data.execute("SELECT COUNT(*) FROM all_questions").fetchone()[0]
        assert count == 20

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

            response = client.post('/frontend/check_answer', data={
                'question_id': id,
                'answer': correct_answer,
            })

            assert response.status_code == 200
            body = response.data.decode()
            assert f"צדקת!" in body


def test_wrong(client):
    tablepath = config.paths ['test_table']
    maker = questionmaker(None)
    with open(tablepath, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        for i, row in enumerate (reader, start=2):
            title_dict = maker.splitTitle (row["title2"])
            id = title_dict['id']
            readtext = maker.readHTML(row["description4"])
            correct_answer = int(readtext["correct_answer"])

            if correct_answer in range (0,3):

                response = client.post('/frontend/check_answer', data={
                    'question_id': id,
                    'answer': correct_answer + 1,
                })

            elif correct_answer == 3:
                    response = client.post('/frontend/check_answer', data={
                    'question_id': id,
                    'answer': 2,
                })
                    
            assert response.status_code == 200
            body = response.data.decode()
            assert f"טעית" in body

                    
def test_types():
    tablepath = config.paths['test_table']
    maker = questionmaker(None)

    with open(tablepath, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for i, row in enumerate(reader, start=2):
            readtext = maker.readHTML(row["description4"])
            types = readtext['types']

            # --- Assertions ---
            # 1. Ensure it's a list
            assert isinstance(types, list), f"Row {i}: types should be a list, got {type(types)}"

            # 2. Ensure no empty strings
            assert all(t.strip() for t in types), f"Row {i}: found empty type in {types}"

            # 3. Optional sanity checks (depending on your dataset)
            for t in types:
                assert len(t) <= 3, f"Row {i}: suspiciously long type '{t}'"
                assert all(c.isalnum() for c in t), f"Row {i}: invalid character in type '{t}'"




        

def test_types(app):
    with app.app_context(): 
        tablepath = config.paths['test_table']
        maker = questionmaker(None)
        db = get_db ()



        with open(tablepath, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for i, row in enumerate(reader, start=2):
                readtext = maker.readHTML(row["description4"])
                types = readtext['types']
                title_dict = maker.splitTitle (row["title2"])
                id = title_dict ['id']


                db_types_rows = db.execute(
                    "SELECT type FROM question_types WHERE question_id = ?", (id,)
                ).fetchall()
                db_types = [row["type"] for row in db_types_rows]

                # --- Assertions ---
                assert set(types) == set(db_types), (
                    f"Row {i}, question {id}: mismatch between parsed types and DB\n"
                    f"Parsed: {types}\n"
                    f"DB: {str (db_types)}"
                )












    