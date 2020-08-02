# rmgame
Text-based resource management game in python3

Based on code from https://github.com/lordmauve/adventurelib

## Installation

Add the following lines to your bashrc:
```
export RMGAME_DIR=/<path-to>/rmgame/
source ${RMGAME_DIR}/bashrc.sh
```

You can also use [gil-install][https://github.com/adrianogil/gil-tools/blob/master/src/python/gil_install.py]:
```
cd <rmgame-path>/src/
gil-install -i
```

## Requirements

- [txtgamelib](https://github.com/adrianogil/txtgamelib)
- [pytools](https://github.com/adrianogil/pytools)


## Features
- Build a House
- Update-based world time
- Show Population limit/stats
- Population growth
- Resources
- Use resources when creating buildings
- Resource gathering

## Planned features
- Fix bug where is possible to gather a starved resource place
- See building description
- building level
- See description of map element
- List people activities
- Remove people from gathering activity
- People starving
- in-progress House (It should take at least few days to build it)
- Limits for storing resource
- Build Warehouse
- Build Farm
- Farm Wheat
- Farm Grapes
- Build Temple
- Build Tavern
- Build Marketplace
- Implement system to sell/buy items
- Implement weather
- People skill can progress according to their activities
