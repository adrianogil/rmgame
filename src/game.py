import txtgamelib
from txtgamelib import when, say

from gamedata import GameData

gameData = GameData()

@when('test')
def test():
    # Method is handled before. So that line is not executed
    say("Test commands works!")

@when('show buildings')
def show_buildings():
    gameData.show_buildings()

@when('build list')
def list_what_can_be_built():
    gameData.show_what_can_be_built();

@when('builders')
def show_builders():
    gameData.show_builders()

@when('builders add')
def add_builders():
    gameData.add_builders()

say('Try to build a great empire')

txtgamelib.start()


