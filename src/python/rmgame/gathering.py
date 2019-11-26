import pyutils.logsystem as logsystem


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

        if not place_exists or not resource_exists:

            return False

        people_available = self.population.has_available(num_people)
        resource_space_available = (self.map.map_elements[place]['resources_to_gather'][resource]['max_people'] - \
                len(self.map.map_elements[place]['resources_to_gather'][resource]['current_people'])) >= num_people

        logsystem.log("people_available - %s" % (people_available,))
        logsystem.log("resource_space_available - %s" % (resource_space_available,))

        return people_available and resource_space_available

    def assign_people(self, resource, place, num_people, game_data):
        place = int(place)
        num_people = int(num_people)

        people = self.population.get_available_people(num_people)

        current_people = self.map.map_elements[place]['resources_to_gather'][resource]['current_people']
        for p in people:
            p.state = 'gathering'
            p.busy = True
            current_people.append(p)
        self.map.map_elements[place]['resources_to_gather'][resource]['current_people'] = current_people

    def world_update(self, game_data):
        pass
