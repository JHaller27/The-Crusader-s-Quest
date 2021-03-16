from typing import Optional
import random

from utils.configs.map import Map as MapConfig, Location as LocationConfig


class Location:
    def __init__(self, config: LocationConfig):
        self.name = config.name
        self.description = config.description
        self.row, self.col = config.row, config.col
        self._blacksmith_mod = config.blacksmith_price
        self._blacksmith_base = 0
        self.enemy_exclude = config.enemy_exclude
        self.destination = config.destination
        self.distance = config.distance
        self.visited = False

    @property
    def blacksmith_price(self) -> int:
        return self._blacksmith_base + self._blacksmith_base

    def randomize_blacksmith_price(self):
        self._blacksmith_base = random.randint(51, 75)

    def visit(self):
        self.visited = True


class Map:
    _locations: dict[str, Location]
    _grid: list[list[Optional[Location]]]
    _current: Optional[Location]

    def __init__(self, config: MapConfig):
        self._width = config.width
        self._height = config.height

        self._grid = [[None for _ in range(self._width)] for _ in range(self._height)]

        self._locations = dict()
        for loc_config in config.locations:
            loc = Location(loc_config)
            self._locations[loc_config.name] = loc
            self._grid[loc_config.row][loc_config.col] = loc

        self._start = self._current = self.get(config.start)
        self._end = self.get(config.end)

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def grid(self) -> list[list[Optional[Location]]]:
        return self._grid

    @property
    def start(self) -> Location:
        assert self._start is not None, "Start not set yet"
        return self._start

    @property
    def end(self) -> Location:
        assert self._end is not None, "End not set yet"
        return self._end

    @property
    def current(self) -> Location:
        assert self._current is not None, "No current location"
        return self._current

    def randomize_blacksmith_prices(self):
        for loc in self._locations.values():
            loc.randomize_blacksmith_price()

    def get(self, name: str) -> Optional[Location]:
        return self._locations.get(name)

    def move(self):
        destination = self.get(self._current.destination)
        self._current = destination

    def at_end_location(self) -> bool:
        return self._current.name == self.end
