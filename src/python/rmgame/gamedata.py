from txtgamelib import say

from population import Population
from building import House
from map import Map

from gathering import Gathering

import time
import utils
import threading

import pyutils.logsystem as logsystem

logsystem.log_function = logsystem.savelogfile

class GameData:

    def __init__(self):
        self.total_workers = 0
        self.available_buildings = [House()]
        self.buildings = []

        self.current_gold = 50000
        self.resources = {
            "gold": 50000,
            "wood": 20000,
            "meat": 1000,
        }

        self.population = Population()
        self.map = Map()

        self.gathering = Gathering(self.map, self.population)

        self.debug_mode = True
        self.game_is_running = True
        self.daytime_in_irl = 10

    def toggle_debug(self):
        self.debug_mode = not self.debug_mode

    def status(self):
        self.population.show_status()

        for r in self.resources:
            say('%s: %s' % (r.capitalize(), self.resources[r]))

    def gather(self, resource, place, num_people):
        if self.gathering.can_gather(resource, place, num_people, self):
            self.gathering.assign_people(resource, place, num_people, self)
            say('%s people starts to gather %s' % (num_people, resource))

    def show_map_info(self):
        self.map.show_info()

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
        logsystem.log('debug: create_building - ' + building_name)

        if utils.is_int(building_name):
            b =  self.available_buildings[int(building_name)]
            self.build(b)
            return

        for b in self.available_buildings:
            if b.name.lower() == building_name.lower():
                self.build(b)
                return

    def verify_cost(self, cost):
        for c in cost:
            if self.resources[c] < cost[c]:
                return False
        return True

    def pay_cost(self, cost):
        for c in cost:
            say('You spend %s %s' % (cost[c], c))
            self.resources[c] = self.resources[c] - cost[c]

    def build(self, building_obj):
        b = building_obj
        if self.verify_cost(b.cost):
            self.pay_cost(b.cost)

            logsystem.log('create_building - lets create a ' + b.name)
            new_building = b.create_new(self)
            self.buildings.append(new_building)
            say('You %s building is ready!' % (new_building.type))
        else:
            say("You don't have %s gold" % (b.cost['gold']))

    def world_update(self):
        self.population.world_update(self)
        self.gathering.world_update(self)
        logsystem.log('World Update!')

    def update_loop(self):
        while self.game_is_running:
            self.world_update()
            time.sleep(self.daytime_in_irl)

    def start_update_loop(self):
        t = threading.Thread(target=self.update_loop)
        t.daemon = True
        t.start()
