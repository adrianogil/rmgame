import txtgamelib
from txtgamelib import when, say

from gamedata import GameData


gameData = GameData()


@when('debug')
def debug():
    import pdb; pdb.set_trace() # Start debugger

@when('status')
def show_status():
    gameData.status()

@when('map info')
def show_map_info():
    gameData.show_map_info()

@when('gather RESOURCE PLACE NUMPEOPLE')
def gather(resource, place, numpeople):
    gameData.gather(resource, place, numpeople)

@when('show buildings')
def show_buildings():
    gameData.show_buildings()

@when('workers')
def show_workers():
    gameData.show_workers()

@when('build list')
def list_what_can_be_built():
    gameData.show_what_can_be_built()

@when('build BUILDING')
def create_building(building):
    gameData.create_building(building)

@when('debug toggle')
def toggle_debug():
    gameData.toggle_debug()
    say('Debug mode is %s' %(gameData.debug_mode,))

say('Try to build a great empire')

gameData.add_workers()
gameData.start_update_loop()
txtgamelib.start()
