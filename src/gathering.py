
class Gathering:
    def __init__(self, mapping, population):
        self.map = mapping
        self.population = population

    def can_gather(self, resource, place, num_people):
        place = int(place)
        num_people = int(num_people)

        place_exists = place >= 0 and place < len(self.map.map_elements)
        resource_exists = resource in self.map.map_elements[place]

        if not place_exists or not resource_exists:
            return False

        people_available = self.population.has_available(num_people)
        resource_space_available = (self.map.map_elements[place][resource]['max_people'] - \
                len(self.map.map_elements[place][resource]['current_people'])) >= num_people

        return people_available and resource_space_available

    def assign_people(self, resource, place, num_people):
        people = self.population.get_available_people(num_people)

        current_people = self.map.map_elements[place][resource]['current_people']
        for p in people:
            p.state = 'gathering'
            p.busy = True
            current_people.append(p)
        self.map.map_elements[place][resource]['current_people'] = current_people