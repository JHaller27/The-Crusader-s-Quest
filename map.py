from typing import Optional, Union
import random
import yaml


class Location:
    def __init__(self, name: str, description: str, pos: (int, int), blacksmith_price: int,
                 enemy_exclude: list[int], destination: str, distance: int):
        self.name = name
        self.description = description
        self.row, self.col = pos
        self._blacksmith_mod = blacksmith_price
        self._blacksmith_base = 0
        self.enemy_exclude = enemy_exclude
        self.destination = destination
        self.distance = distance
        self.visited = False

    @classmethod
    def from_yaml(cls, name: str, source: dict):
        travel = source.get("travel")
        dest = None if travel is None else travel.get("destination")
        dist = None if travel is None else travel.get("distance")

        return cls(
            name=name,
            description=source.get("description"),
            pos=(source.get("row"), source.get("col")),
            blacksmith_price=source.get("blacksmith_price"),
            enemy_exclude=source.get("enemy_exclude"),
            destination=dest,
            distance=dist,
        )

    @property
    def blacksmith_price(self) -> int:
        return self._blacksmith_base + self._blacksmith_base

    def randomize_blacksmith_price(self):
        self._blacksmith_base = random.randint(51, 75)

    def visit(self):
        self.visited = True


class Map:
    _grid: list[list[Optional[Location]]]

    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height

        self._start = None
        self._end = None
        self._current = None

        self._locations = dict()
        self._grid = [[None for _ in range(self._width)] for _ in range(self._height)]

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

    def set_location(self, val: Union[Location, str]):
        if isinstance(val, str):
            val = self.get(val)

        self._current = val
        self._current.visit()

    def add_location(self, loc: Location):
        self._locations[loc.name] = loc
        self._grid[loc.row][loc.col] = loc

    def set_start(self, name: str):
        self._start = self._locations.get(name)

        if self._current is None:
            self._current = self._start

    def set_end(self, name: str):
        self._end = self._locations.get(name)

    def get(self, name: str) -> Optional[Location]:
        return self._locations.get(name)


def get_map(data_path: str) -> Map:
    with open(data_path, 'r') as fp:
        map_config = yaml.safe_load(fp)

    map_obj = Map(map_config.get("width"), map_config.get("height"))
    for name, loc in map_config.get("locations").items():
        loc_obj = Location.from_yaml(name, loc)
        loc_obj.randomize_blacksmith_price()

        map_obj.add_location(loc_obj)

    map_obj.set_start(map_config.get("start"))
    map_obj.start.visit()

    map_obj.set_end(map_config.get("end"))

    return map_obj
