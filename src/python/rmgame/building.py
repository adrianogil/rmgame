from txtgamelib.game.basic import say


class House:
    def __init__(self):
        self.name = 'House'
        self.type = 'House'
        self.cost = {
            'gold': 100,
            'wood': 50
        }
        self.population_limit_increment = 5

    def create_new(self, gameData):
        self.on_create(gameData)

        return House()

    def on_create(self, gameData):
        gameData.population.increase_limit(self.population_limit_increment)
