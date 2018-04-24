from txtgamelib import say


class GameData:

    def __init__(self):
        self.total_gold = 100
        self.total_builders = 0

    def add_builders(self):
        self.total_builders = self.total_builders + 1

    def show_builders(self):
        say('Builders: %s' % (self.total_builders,))