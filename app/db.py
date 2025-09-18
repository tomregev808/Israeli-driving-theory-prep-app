import sqlite3
from datetime import datetime

import click
from flask import current_app, g
from app.question_make import questionmaker
from app.config import paths

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()



def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    if current_app.testing is False:
        maker = questionmaker(paths ['table'])
        list = maker.makeList()
        with current_app.app_context():
          fillTable(list)

    else:
        maker = questionmaker(paths ['test_table'])
        list = maker.makeList()
        with current_app.app_context():
          fillTable(list)






@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def fillRow (question):
    db = get_db()
    db.execute ('INSERT into all_questions '
                        '(id, title,'
                         'answer_0, answer_1, answer_2, answer_3,'
                        'correct_answer, category, image)'
                        'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (question.id, question.title, question.answers [0], question.answers [1], question.answers [2], question.answers [3], 
                        question.correct_answer, question.category, question.image))
    db.commit()

def fillTable (list): 
    for question in list:
        fillRow (question)
        


sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

