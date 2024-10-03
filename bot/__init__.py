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

    def __xor__(self, b2):
        return Button(name=f"{self.name} ^ {b2.name}", string=bin(int(self.string, 2) ^ int(b2.string, 2)).zfill(12))

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

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

class Player:

    def __init__(self):
        self.position = "P1"
        self.queue = []

    def set_position(self, position):
        self.position = position
        self.dhalsim()

    def dhalsim(self):
        # Let's select DHALSIM
        if self.position == "P1":
            self.push(DOWN)

        self.push(RIGHT)
        self.push(RIGHT)
        self.push(RIGHT)
        self.push(A)

    def get_direction(self):
        if self.position == "P1":
            return RIGHT
        return LEFT

    def push(self, action: Button) -> None:
        self.queue.append([action])

    def get_action(self) -> list[Button]:
        if not self.queue:
            # Boule de feu
            fireball = [DOWN, DOWN ^ self.get_direction(), self.get_direction() ^ X] # + [NOTHING] * 39
            balayette = [DOWN ^ R] * 10 # + [ DOWN ] * 11
            punch = [Y] # + [NOTHING] * 18
            low_punch = [DOWN ^ L] # + [NOTHING] * 24

            action = []

            for _ in range(5):
                rand = random.random()

                if rand < 1:
                    action += balayette
                elif 0.2 > rand > 0.8:
                    action += fireball
                elif 0.8 > rand > 0.9:
                    action += low_punch
                else:
                    action += punch

            for frames in split(action, 7):
                self.queue.append(frames)

            print(self.queue)

        return self.queue.pop(0)

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

        actions = player.get_action()
        print(actions)
        str_actions = ", ".join([a.name for a in actions])
        print(f"ID: {frameid}, Count: {frame_count}, clock: {player_clock}, timeout: {player_timeout}, action: {str_actions}")

        return "".join(action.string for action in actions)

    return app
