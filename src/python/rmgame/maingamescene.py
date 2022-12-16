from txtgamelib.game.scene import GameScene


class MainGameScene(GameScene): 
    def __init__(self, gameData):
        self.gameData = gameData

    def play(self, game):
        pass

    def update(self, game):
        self.gameData.world_update()
