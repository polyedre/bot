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
NOTHING = Button(name="_" ,string="000000000000")

def xor(b1, b2):
    return bin(int(b1, 2) ^ int(b2, 2))

class Player:

    def __init__(self):
        self.position = "P1"
        self.queue = []

    def set_position(self, position):
        self.position = position
        self.select_player()

    def frame(self, moves):
        if type(moves)!=list:
            moves = [moves]
        nothing_fill_count = 10 - len(moves)
        self.queue.extend(moves + [NOTHING] * nothing_fill_count)

    def select_player(self):
        # Let's select DHALSIM
        if self.position == "P1":
            self.frame(DOWN)

        self.frame(RIGHT)
        self.frame(RIGHT)
        self.frame(RIGHT)
        self.frame(A)

    def get_direction(self):
        if self.position == "P1":
            return RIGHT
        return LEFT

    def get_actions(self) -> list[Button]:
        if len(self.queue) < 10:
            actions = self.plan_actions()
            self.queue += actions

        actions = self.queue[:10]
        self.queue = self.queue[10:]
        return actions

    def plan_actions(self):
        fireball = [DOWN, DOWN ^ self.get_direction(), self.get_direction() ^ X]  + [NOTHING] * 2
        balayette = [DOWN ^ R] + [NOTHING] * 4
        drill = [UP] +  [NOTHING] * 10 + [DOWN ^ R] * 1 + [NOTHING] * 10
        return fireball * 36 + drill * 4 + balayette * 18

class PQuestPlayer(Player):

    def __init__(self):
        super(Player, self).__init__()

    def select_player(self):
        # Let's select MAX
        self.frame(A)

    def plan_actions(self):
        fireball = [DOWN, DOWN ^ self.get_direction(), self.get_direction() ^ A]  + [NOTHING] * 2
        return fireball * 36

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # a simple page that says hello
    @app.post('/start')
    def start():
        try:
            data = request.json
            position = data.get("position", None)
            game = data.get("game", None)
            print(f"THE GAME IS {game}")
            print(data)
            global player
            if game == "pquest":
                player = PQuestPlayer()
            else:
                player = Player()
            if position in ["P1", "P2"]:
                print(f"Setting position {position}")
                player.set_position(position)
            game_id = data.get("game_id", None)
        except:
            return "blabla"
        return f"I start with position {position}, game is {game}, game id {game_id}"

    @app.post('/frame/<frameid>')
    def frame(frameid: int):
        frame_count = request.headers.get("X-Frame-Count", 0)
        player_clock = request.headers.get("X-Player-Clock", 0)
        player_timeout = request.headers.get("X-Player-Timeout", 0)

        actions = player.get_actions()
        str_actions = ", ".join([a.name for a in actions])
        print(f"ID: {frameid}, Count: {frame_count}, clock: {player_clock}, timeout: {player_timeout}, action: {str_actions}")

        return "".join(action.string for action in actions)

    return app