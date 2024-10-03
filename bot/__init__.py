#!/usr/bin/env python3

import os

import json
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
        data = json.loads(list(request.form.keys())[0])
        position = data.get("position", None)
        game_id = data.get("game_id", None)
        return f"I start with position {position}, game id {game_id}"

    @app.post('/frame/<frameid>')
    def frame(frameid: int):
        frame_count = request.headers.get("X-Frame-Count", 0)
        player_clock = request.headers.get("X-Player-Clock", 0)
        player_timeout = request.headers.get("X-Player-Timeout", 0)

        return "".join(Button.A for _ in range(frame_count))

    return app
