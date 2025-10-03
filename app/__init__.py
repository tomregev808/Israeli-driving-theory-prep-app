from flask import Flask, render_template, request
import os
from app import db
from flask import jsonify
import random
from app import frontend


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    #remember changing the config!!!!!
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'db.sqlite'),
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent = True)
    else:
        app.config.from_mapping (test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    db.init_app(app)



    app.register_blueprint (frontend.bp)

    @app.route('/', methods=['GET'])
        return render_template("idnex.html")


    return app



