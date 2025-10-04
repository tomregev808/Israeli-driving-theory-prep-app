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

                    
            
def test_get_failed_questions(client):
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

                post = client.post('/frontend/check_answer', data={
                    'question_id': id,
                    'answer': correct_answer + 1,
                })

            elif correct_answer == 3:
                    post = client.post('/frontend/check_answer', data={
                    'question_id': id,
                    'answer': 2,
                })
                    

        response = client.get ('/api/get_failed_questions')


                    
        assert response.status_code == 200
        body = response.data.decode()
        assert str(id) in body

                    








    