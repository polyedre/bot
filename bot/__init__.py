#!/usr/bin/env python3

import os

import json
from flask import Flask
from flask import request

class Button:

    B       = "100000000000"
    Y       = "010000000000"
    UP      = "000010000000"
    DOWN    = "000001000000"
    LEFT    = "000000100000"
    RIGHT   = "000000010000"
    A       = "000000001000"
    X       = "000000000100"
    L       = "000000000010"
    R       = "000000000001"
    NOTHING = "000000000000"

def xor(b1, b2):
    return bin(int(b1, 2) ^ int(b2, 2))

class Player:

    def __init__(self):
        self.position = "P1"
        self.action_count = 0

    def set_position(self, position):
        self.position = position

    def get_action(self):
        self.action_count += 1
        if self.position == "P1":
            direction_button = Button.RIGHT
        else:
            direction_button = Button.LEFT

        # if self.action_count % 2 == 0:
        #     action = Button.A # xor(Button.A, direction_button)[2:].zfill(12)
        # else:
        action = direction_button
        return action

player = Player()

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
        try:
            data = request.json
            position = data.get("position", None)
            print(data)
            if position in ["P1", "P2"]:
                player.position = position
            game_id = data.get("game_id", None)
        except:
            return "blabla"
        return f"I start with position {position}, game id {game_id}"

    @app.post('/frame/<frameid>')
    def frame(frameid: int):
        frame_count = request.headers.get("X-Frame-Count", 0)
        player_clock = request.headers.get("X-Player-Clock", 0)
        player_timeout = request.headers.get("X-Player-Timeout", 0)

        action = player.get_action()
        print(f"ID: {frameid}, Count: {frame_count}, clock: {player_clock}, timeout: {player_timeout}, action: {action}")

        return action

    return app
