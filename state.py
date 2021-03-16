from typing import Optional

from utils.map import Map, Location
from utils.player import Player
from utils.enemy import Enemy
from utils.ui import Singleton
from utils.configs.player import Player as PlayerConfig
from utils.configs.enemies import Enemies as EnemiesConfig


class State:
    def __init__(self, ctx: 'Context'):
        self._ctx = ctx

    @property
    def ctx(self) -> 'Context':
        return self._ctx

    def do(self) -> Optional['State']:
        raise NotImplementedError


class Context:
    counter = 0

    days_to_go = 0

    player: Player
    enemy: Enemy

    _state: State

    def __init__(self, map_obj: Map, player_config: PlayerConfig, enemy_config: EnemiesConfig):
        self.map = map_obj
        self.player_config = player_config
        self.enemy_config = enemy_config

        self.player = Player()

    def _run_once(self):
        Singleton().debug(f"Running state '{type(self._state).__name__}'")
        self._state = self._state.do()

    def run(self, init: Optional[State]):
        self._state = init

        while self._state is not None:
            self._run_once()

    @property
    def location(self) -> Location:
        return self.map.current

    @property
    def blacksmith_price(self) -> int:
        return self.map.current.blacksmith_price

    def combat_damage(self) -> int:
        assert self.enemy is not None, "No enemy set, combat failed"

        return max(self.enemy.battle_score - self.player.martial_prowess, 0)
