from txtgamelib import say

from building import House

class GameData:

    def __init__(self):
        self.total_gold = 100
        self.total_builders = 0
        self.available_buildings = [House()]
        self.buildings = []

        self.population_limit = 1
        self.population = 1
        self.available_worker = 1

        self.debug_mode = False

    def toggle_debug(self):
        self.debug_mode = not self.debug_mode

    def status(self):
        say('Population: %s/%s' % (self.population, self.population_limit,) )

    def add_builders(self):
        self.total_builders = self.total_builders + 1

    def show_builders(self):
        say('Builders: %s' % (self.total_builders,))

    def show_what_can_be_built(self):
        index = 0
        for b in self.available_buildings:
            say('%s - %s' % (index, b.name))
            index = index + 1

    def show_buildings(self):
        index = 0
        if len(self.buildings) == 0:
            say('There is not a single building. Let\'s create a new one')
        for b in self.buildings:
            say('%s - %s' % (index, b.name))
            index = index + 1

    def create_building(self, building_name):

        print('debug: create_building - ' + building_name)

        for b in self.available_buildings:
            if b.name.lower() == building_name.lower():
                self.dprint('create_building - lets create a ' + building_name)
                self.buildings.append(b.create_new(self))

    def dprint(self, text):
        if self.debug_mode:
            print('debug: ' + text)