from dice import Dice

import utils

import copy

class Map:
    def __init__(self):
        self.map_elements_types = [
            {
                'name' : 'Florest',
                'distance' : 0,
                'resources_to_gather' : {
                    'wood': {
                        'current': 1000,
                        'auto-renewable': True,
                        'renewable-velocity': 100, # per minute
                        'max_people': 5,
                        'current_people': []
                    },
                    "meat" : {
                        'current': 1000,
                        'auto-renewable': True,
                        'renewable-velocity': 100, # per minute
                        'max_people': 5,
                        'current_people': []
                    },
                }
            },
            {
                'name' : 'Big Florest',
                'distance' : 0,
                'resources_to_gather' : {
                    'wood': {
                        'current': 10000,
                        'auto-renewable': True,
                        'renewable-velocity': 1000, # per minute
                        'current_people': [],
                        'max_people': 10
                    },
                    "meat" : {
                        'current': 10000,
                        'auto-renewable': True,
                        'renewable-velocity': 1000, # per minute
                        'current_people': [],
                        'max_people': 10
                    },
                }
            },
            {
                'name' : 'Lake',
                'distance' : 0,
                'resources_to_gather' : {
                    "fish" : {
                        'current': 100,
                        'auto-renewable': True,
                        'renewable-velocity': 1, # per minute
                        'max_people': 5,
                        'current_people': [],
                    },
                }
            },
            {
                'name' : 'Big Lake',
                'distance' : 0,
                'resources_to_gather' : {
                    "fish" : {
                        'current': 1000,
                        'auto-renewable': True,
                        'renewable-velocity': 10, # per minute
                        'max_people': 5,
                        'current_people': []
                    },
                }
            }

        ]
        self.generate_initial_map()

    def generate_initial_map(self):
        self.map_elements = []

        initial_elements_size = Dice.parse('3d6')

        for e in range(0, initial_elements_size):
            new_element = copy.deepcopy(utils.get_random(self.map_elements_types))
            new_element['distance'] = Dice.parse('10*10d10')
            self.map_elements.append(new_element)

        self.map_elements = sorted(self.map_elements, key=lambda x: x['distance'], reverse=False)

    def show_info(self):
        index = 0

        for e in self.map_elements:
            
            people_working = 0
            resource_str = "("
            if 'resources_to_gather' in e:
                for r in e['resources_to_gather']:
                    resource_str = resource_str + str(e['resources_to_gather'][r]['current']) + \
                            ' ' + r + ', '
                    people_working = people_working + len(e['resources_to_gather'][r]['current_people'])
            resource_str = resource_str + str(people_working) + ' people gathering )'

            data_to_show = (index,  e['name'], e['distance']/1000.0, resource_str)
            print('%s - %s at %.2f km %s' % data_to_show)
            index = index + 1