from typing import Optional
import yaml


class Location:
    def __init__(self, name: str, description: str, pos: (int, int), blacksmith_price: int,
                 enemy_exclude: list[int], destination: str, distance: int):
        self.name = name
        self.description = description
        self.row, self.col = pos
        self.blacksmith_price = blacksmith_price
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

    def visit(self):
        self.visited = True


class Map:
    _grid: list[list[Optional[Location]]]

    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height

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

    def add_location(self, loc: Location):
        self._locations[loc.name] = loc
        self._grid[loc.row][loc.col] = loc

    def get(self, name: str) -> Optional[Location]:
        return self._locations.get(name)


def get_map(data_path: str) -> (Map, dict):
    with open(data_path, 'r') as fp:
        map_config = yaml.safe_load(fp)

    map_obj = Map(map_config.get("width"), map_config.get("height"))
    for name, loc in map_config.get("locations").items():
        loc_obj = Location.from_yaml(name, loc)
        map_obj.add_location(loc_obj)

    map_obj.get(map_config.get("start")).visit()

    return map_obj, map_config
