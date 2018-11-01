from txtgamelib import say

from dice import Dice

import random

class Population:
    def __init__(self):
        self.limit = 1
        self.current = 1

    def show_status(self):
        say('Population: %s/%s' % (self.current, self.limit,) )

    def add_new_people(self, total_new_people):
        if self.current + total_new_people <= self.limit:
            self.current = self.current + total_new_people
            say('New people just arrived: your population incremented in %s' % (total_new_people,) )

    def increase_limit(self, increment):
        self.limit = self.limit + increment
        say("Your population limit increased in %s units" % (increment,))

    def verify_new_people(self, game_data):
        is_space_available = self.limit > self.current
        # TODO: verify if city is attractive
        if is_space_available:
            prob = random.uniform(0, 1)
            if prob < 0.05:
                available_space = self.limit - self.current
                total_new_people = Dice.parse("1d" + str(available_space))
                self.add_new_people(total_new_people)

    def world_update(self, game_data):
        self.verify_new_people(game_data)