#!/usr/bin/env python3

import os

from flask import Flask
from flask import request

class Button:

    B = "100000000000"
    Y = "010000000000"
    UP = "000010000000"
    DOWN = "000001000000"
    LEFT = "000000100000"
    RIGHT = "000000010000"
    A = "000000001000"
    X = "000000000100"
    L = "000000000010"
    R = "000000000001"

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.post('/start')
    def start():
        return 'Hello, World!'

    @app.post('/frame/<frameid>')
    def frame(frameid: int):
        frame_count = request.headers.get("X-Frame-Count")
        player_clock = request.headers.get("X-Player-Clock")
        player_timeout = request.headers.get("X-Player-Timeout")

        return "".join(Button.A for _ in frame_count)

    return app
