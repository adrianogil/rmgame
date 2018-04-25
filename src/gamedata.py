from txtgamelib import say


class GameData:

    def __init__(self):
        self.total_gold = 100
        self.total_builders = 0
        self.available_buildings = ['House']
        self.buildings = []

    def add_builders(self):
        self.total_builders = self.total_builders + 1

    def show_builders(self):
        say('Builders: %s' % (self.total_builders,))

    def show_what_can_be_built(self):
        index = 0
        for b in self.available_buildings:
            say('%s - %s' % (index, b))
            index = index + 1

    def show_buildings(self):
        index = 0
        if len(self.buildings) == 0:
            say('There is not a single building. Let\'s create a new one')
        for b in self.buildings:
            say('%s - %s' % (index, b))
            index = index + 1