import random

from utils.configs import EnemyType, EnemyAdjective


class Enemy:
    def __init__(self, enemy_type: EnemyType, adj: EnemyAdjective = None):
        self._adjective = adj
        self._type = enemy_type

        self._food = self._type.food if self._type.food is not None else 0
        self._arrows = self._type.arrows if self._type.arrows is not None else 0
        self._gold = self._type.gold if self._type.gold is not None else 0

    def randomize_loot(self):
        if self._food is not None:
            self._food += random.randrange(10) + 1

        if self._arrows is not None:
            self._arrows += random.randrange(5) + 1

        if self._gold is not None:
            self._gold += random.randrange(10) + 1

    @property
    def name(self) -> str:
        s = ""
        if self._adjective is not None:
            s += self._adjective.name + " "
        s += self._type.name

        return s

    @property
    def name(self) -> str:
        return f"{self._adjective} {self._type}"

    @property
    def battle_score(self) -> int:
        return self._type.battle_score + self._adjective.battle_score

    @property
    def food(self) -> int:
        return self._food if self._food is not None else 0

    @property
    def arrows(self) -> int:
        return self._arrows if self._arrows is not None else 0

    @property
    def gold(self) -> int:
        return self._gold if self._gold is not None else 0

    def is_type(self, enemy_type: str) -> bool:
        return self._type.name.lower() == enemy_type.lower()
