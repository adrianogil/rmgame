from txtgamelib import say

from dice import Dice

import random

import pyutils.logsystem as logsystem


class Person:
    def __init__(self):
        self.name = "Person"
        self.state = 'idle'
        self.busy = False
        self.current_activity = None

        self.resource_gathering_velocity = {
            "wood": 2,
            "gold": 3,
            "meat": 4,
            "fish": 10,
        }

    def get_resource_gathering_velocity(self, resource):
        """
            get_resource_gathering_velocity
        """
        return self.resource_gathering_velocity[resource]


class Population:
    def __init__(self):
        self.limit = 1
        self.current = 1
        self.people = []
        for p in range(0, self.current):
            self.people.append(Person())

    def show_status(self):
        say('Population: %s/%s' % (self.current, self.limit,))

    def add_new_people(self, total_new_people):
        if self.current + total_new_people <= self.limit:
            for p in range(0, total_new_people):
                new_person = Person()
                new_person.name = "Person_" + str(self.current + p + 1)
                self.people.append(new_person)
            self.current = self.current + total_new_people
            logsystem.log('New people just arrived: your population incremented in %s' % (total_new_people,) )

    def has_available(self, num_people):
        total_available_people = 0

        for p in self.people:
            if p.busy == False:
                total_available_people = total_available_people + 1
                if total_available_people >= num_people:
                    return True

        return False

    def get_available_people(self, num_people):
        available_people = []

        for p in self.people:
            if p.busy == False:
                available_people.append(p)

        return available_people[:num_people]

    def increase_limit(self, increment):
        self.limit = self.limit + increment
        say("Your population limit increased in %s units" % (increment,))

    def verify_new_people(self, game_data):
        is_space_available = self.limit > self.current
        # TODO: verify if city is attractive
        if is_space_available:
            prob = random.uniform(0, 1)
            if prob < 0.5:
                available_space = self.limit - self.current
                total_new_people = Dice.parse("1d" + str(available_space))
                self.add_new_people(total_new_people)

    def world_update(self, game_data):
        self.verify_new_people(game_data)

        total_meat_consumption_day = 0

        for p in self.people:
            # Activity
            if p.current_activity is not None:
                p.current_activity(p)

            # Consumption
            consumption_day = 0
            if p.state == 'idle':
                consumption_day = 0.1 * random.randint(5, 10)
            else:
                consumption_day = 0.15 * random.randint(5, 10)

            total_meat_consumption_day += consumption_day
            game_data.resources["meat"] -= consumption_day

        logsystem.log("people consumed %f meat today" % (total_meat_consumption_day,))
