from txtgamelib.game.basic import say

from .population import Population
from .building import House
from .map import Map


from .gathering import Gathering
from . import utils

import threading
import time

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
            "wood": 20000.0,
            "meat": 1000.0,
            "fish": 0.0,
        }

        self.population = Population()
        self.map = Map()

        self.gathering = Gathering(self.map, self.population)

        self.debug_mode = True
        self.game_is_running = True
        self.daytime_in_irl = 10

        self.current_total_minutes = 0

        self.minutes_per_update = 5

        self.minutes_per_day = 24 * 60
        self.minutes_per_year = 365 * self.minutes_per_day

        self.day_percentage_per_update = self.minutes_per_update / self.minutes_per_day


    def toggle_debug(self):
        self.debug_mode = not self.debug_mode

    def show_current_time(self):
        # Total time in minutes
        total_time = self.current_total_minutes

        days = total_time // (24 * 60)
        total_time -= (24 * 60) * days
        hours = total_time // 60
        total_time -= 60 * hours
        minutes = total_time

        say("Current day: %dd%02dh%02dm" % (days, hours, minutes))

    def status(self):
        self.population.show_status()

        print("Resources:")
        for r in self.resources:
            say('\t%s: %s' % (r.capitalize(), self.resources[r]))


        self.show_current_time()

    def gather(self, resource, place, num_people):
        logsystem.log("gather resource %s at %s with %s people" % (
                resource, place, num_people
            ))

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
            cost_parts = []
            for resource, amount in b.cost.items():
                cost_parts.append('%s %s' % (amount, resource))
            cost_display = ', '.join(cost_parts)
            description = getattr(b, 'description', '')
            if description:
                say('%s - %s: %s (Cost: %s)' % (index, b.name, description, cost_display))
            else:
                say('%s - %s (Cost: %s)' % (index, b.name, cost_display))
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

        self.current_total_minutes += self.minutes_per_update

    def fast_forward(self, minutes):
        updates_to_fast_forward = minutes // self.minutes_per_update

        for _ in range(updates_to_fast_forward):
            self.world_update()
