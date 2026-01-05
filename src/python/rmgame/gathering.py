import pyutils.logsystem as logsystem

from txtgamelib.game.basic import say


class Gathering:
    def __init__(self, mapping, population):
        self.map = mapping
        self.population = population

    def can_gather(self, resource, place, num_people, game_data):
        place = int(place)
        num_people = int(num_people)

        place_exists = place >= 0 and place < len(self.map.map_elements)
        resource_exists = resource in self.map.map_elements[place]['resources_to_gather']

        logsystem.log("place_exists - %s" % (place_exists,))
        logsystem.log("resource_exists - %s" % (resource_exists,))

        if not place_exists:
            say("The place does not exist")
            return False

        if not resource_exists:
            say("The resource does not exist")
            return False

        people_available = self.population.has_available(num_people)
        resource_space_available = (self.map.map_elements[place]['resources_to_gather'][resource]['max_people'] - \
                len(self.map.map_elements[place]['resources_to_gather'][resource]['current_people'])) >= num_people

        logsystem.log("people_available - %s" % (people_available,))
        logsystem.log("resource_space_available - %s" % (resource_space_available,))

        if not people_available:
            say("There are not enough people available")

        if not resource_space_available:
            say("There are not enough space available for the people to gather the resource")

        return people_available and resource_space_available

    def assign_people(self, resource, place, num_people, game_data):
        logsystem.log("%s people is going to gather %s at %s" % (
                num_people, resource, place
            ))
        place = int(place)
        num_people = int(num_people)

        people = self.population.get_available_people(num_people)

        def gather_activity(person):
            gathering_velocity = game_data.day_percentage_per_update * person.get_resource_gathering_velocity(resource)
            logsystem.log("Person %s is gathering %s at %s with velocity %s" %
                (person.name, resource, place, gathering_velocity))
            self.map.map_elements[place]['resources_to_gather'][resource]["current"] -= \
                gathering_velocity
            game_data.resources[resource] += gathering_velocity

        current_people = self.map.map_elements[place]['resources_to_gather'][resource]['current_people']
        for p in people:
            p.state = 'gathering'
            p.busy = True
            p.current_activity = gather_activity
            current_people.append(p)
        self.map.map_elements[place]['resources_to_gather'][resource]['current_people'] = current_people

    def stop_gathering(self, resource, place, num_people, game_data):
        logsystem.log("%s people is going to stop gathering %s at %s" % (
                num_people, resource, place
            ))
        place = int(place)
        num_people = int(num_people)

        place_exists = place >= 0 and place < len(self.map.map_elements)
        resource_exists = place_exists and resource in self.map.map_elements[place]['resources_to_gather']

        if not place_exists:
            say("The place does not exist")
            return False

        if not resource_exists:
            say("The resource does not exist")
            return False

        current_people = self.map.map_elements[place]['resources_to_gather'][resource]['current_people']

        if len(current_people) < num_people:
            say("There are not enough people gathering this resource")
            return False

        people_to_stop = current_people[:num_people]
        remaining_people = current_people[num_people:]

        for p in people_to_stop:
            p.state = 'idle'
            p.busy = False
            p.current_activity = None

        self.map.map_elements[place]['resources_to_gather'][resource]['current_people'] = remaining_people
        return True

    def world_update(self, game_data):
        pass
