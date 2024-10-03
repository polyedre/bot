#!/usr/bin/env python3

import os

import json
import random
from flask import Flask
from flask import request

class Button:

    def __init__(self, name, string):
        self.name = name
        self.string = string

    def __repr__(self):
        return f"{self.name}"

    def __str__(self):
        return f"{self.name}"

B       = Button(name="B"       ,string="100000000000")
Y       = Button(name="Y"       ,string="010000000000")
UP      = Button(name="UP"      ,string="000010000000")
DOWN    = Button(name="DOWN"    ,string="000001000000")
LEFT    = Button(name="LEFT"    ,string="000000100000")
RIGHT   = Button(name="RIGHT"   ,string="000000010000")
A       = Button(name="A"       ,string="000000001000")
X       = Button(name="X"       ,string="000000000100")
L       = Button(name="L"       ,string="000000000010")
R       = Button(name="R"       ,string="000000000001")
NOTHING = Button(name="NOTHING" ,string="000000000000")

def xor(b1, b2):
    return bin(int(b1, 2) ^ int(b2, 2))

class Player:

    def __init__(self):
        self.position = "P1"
        self.action_count = 0
        self.queue = [A] + [NOTHING] * 30

    def set_position(self, position):
        self.position = position

        # Let's select DHALSIM
        if position == "P1":
            self.queue = [DOWN]

        self.queue += [RIGHT] * 3 + [A]

    def get_action(self):
        self.action_count += 1

        if not self.queue:
            self.queue.append(R)
            self.queue.append(NOTHING)

        return self.queue.pop(0)

player = None

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
            global player
            player = Player()
            if position in ["P1", "P2"]:
                print(f"Setting position {position}")
                player.set_position(position)
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

        return action.string

    return app
