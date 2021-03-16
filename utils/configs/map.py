from typing import Optional

from .config_base import ConfigBase


class Location(ConfigBase):
    def __init__(self, config_dict: dict, name: str):
        super().__init__(config_dict)
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._get("description")

    @property
    def row(self) -> int:
        return self._get("row")

    @property
    def col(self) -> int:
        return self._get("col")

    @property
    def position(self) -> (int, int):
        return self.row, self.col

    @property
    def blacksmith_price(self) -> Optional[int]:
        return self._get("blacksmith_price")

    @property
    def enemy_exclude(self) -> Optional[list[int]]:
        return self._get("enemy_exclude")

    @property
    def destination(self) -> Optional[str]:
        return self._get("travel", "destination")

    @property
    def distance(self):
        return self._get("travel", "distance")


class Map(ConfigBase):
    @property
    def width(self) -> int:
        return self._get("width")

    @property
    def height(self) -> int:
        return self._get("height")

    @property
    def start(self) -> str:
        return self._get("start")

    @property
    def end(self) -> str:
        return self._get("end")

    @property
    def locations(self):
        return [Location(v, k) for k, v in self._get("locations").items()]
