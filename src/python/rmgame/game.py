from txtgamelib.game.game import Game
from txtgamelib.game.basic import say
from txtgamelib.player.player import BasicPlayer

from .gamedata import GameData
from .maingamescene import MainGameScene

game = Game()
game.player = BasicPlayer()
gameData = GameData()

@game.command('debug')
def debug(player):
    import pdb; pdb.set_trace() # Start debugger

@game.command('status')
def show_status(player):
    gameData.status()

@game.command('map info')
def show_map_info(player):
    gameData.show_map_info()

@game.command('gather RESOURCE PLACE NUMPEOPLE')
def gather(player, resource, place, numpeople):
    gameData.gather(resource, place, numpeople)

@game.command('stop gather RESOURCE PLACE NUMPEOPLE')
def stop_gather(player, resource, place, numpeople):
    gameData.stop_gather(resource, place, numpeople)

@game.command('show buildings')
def show_buildings(player):
    gameData.show_buildings()

@game.command('workers')
def show_workers(player):
    gameData.show_workers()

@game.command('build list')
def list_what_can_be_built(player):
    gameData.show_what_can_be_built()

@game.command('build BUILDING')
def create_building(player, building):
    gameData.create_building(building)

@game.command('fastforward MINUTES')
def gather(player, minutes):
    gameData.fast_forward(int(minutes))

@game.command('debug toggle')
def toggle_debug(player):
    gameData.toggle_debug()
    say('Debug mode is %s' %(gameData.debug_mode,))

say('Try to build a great empire')

gameData.add_workers()

game.scenes = [MainGameScene(gameData)]
game.start()
