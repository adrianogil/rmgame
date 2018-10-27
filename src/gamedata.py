from txtgamelib import say

from building import House

import utils

class GameData:

    def __init__(self):
        self.total_gold = 100
        self.total_workers = 0
        self.available_buildings = [House()]
        self.buildings = []

        self.current_gold = 50000

        self.population_limit = 1
        self.population = 1
        self.available_worker = 1

        self.debug_mode = False

    def toggle_debug(self):
        self.debug_mode = not self.debug_mode

    def status(self):
        say('Population: %s/%s' % (self.population, self.population_limit,) )
        say('Gold: %s' % (self.current_gold))

    def add_workers(self):
        self.total_workers = self.total_workers + 1

    def show_workers(self):
        say('workers: %s' % (self.total_workers,))

    def show_what_can_be_built(self):
        say('You can build:')
        index = 0
        for b in self.available_buildings:
            say('%s - %s' % (index, b.name))
            index = index + 1

    def show_buildings(self):
        
        if len(self.buildings) == 0:
            say('There is not a single building. Let\'s create a new one')
        buildings_to_show = {}
        for b in self.available_buildings:
            buildings_to_show[b.type] = 0
        for b in self.buildings:
            buildings_to_show[b.type] = buildings_to_show[b.type] + 1

        for b in buildings_to_show:
            if buildings_to_show[b] == 1:
                say('%s (only %s building)' % (b, buildings_to_show[b]))
            elif buildings_to_show[b] > 1:
                say('%s (%s buildings)' % (b, buildings_to_show[b]))


    def create_building(self, building_name):
        self.dprint('debug: create_building - ' + building_name)

        if utils.is_int(building_name):
            b =  self.available_buildings[int(building_name)]
            self.build(b)

        for b in self.available_buildings:
            if b.name.lower() == building_name.lower():
                self.build(b)
                

    def build(self, building_obj):
        b = building_obj
        if b.cost['gold'] < self.current_gold:
            say('You spend %s gold' % (b.cost['gold']))
            self.current_gold = self.current_gold - b.cost['gold']

            self.dprint('create_building - lets create a ' + b.name)
            new_building = b.create_new(self)
            self.buildings.append(new_building)
            say('You %s building is ready!' % (new_building.type))
        else:
            say("You don't have %s gold" % (b.cost['gold']))

    def dprint(self, text):
        if self.debug_mode:
            print('debug: ' + text)