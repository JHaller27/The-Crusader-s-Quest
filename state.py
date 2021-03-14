from typing import Optional, Type

from ui import UserInterface
from map import Map, Location
from player import Player
from enemy import Enemy


class State:
    def __init__(self, ctx: 'Context'):
        self._ctx = ctx

    @property
    def ctx(self) -> 'Context':
        return self._ctx

    def do(self) -> Optional['State']:
        raise NotImplementedError


class TransientState(State):
    def __init__(self, ctx: 'Context', default: Optional[Type[State]]):
        super().__init__(ctx)
        self._default = default

    @property
    def default(self) -> Optional[Type[State]]:
        return self._default

    def _do(self) -> Optional[State]:
        raise NotImplementedError

    def do(self) -> Optional['State']:
        if next_state := self._do():
            return next_state

        return self._default(self.ctx)


class Context:
    counter = 0
    counter_set = 0

    days_to_go = 0
    adventure_state = False

    player: Player
    enemy: Enemy

    _state: State

    def __init__(self, ui: UserInterface, map_obj: Map):
        self.ui = ui
        self.map = map_obj
        self.player = Player()

    def _run_once(self):
        self.ui.debug(f"Running state '{type(self._state).__name__}'")
        self._state = self._state.do()

    def run(self, init: Optional[State]):
        self._state = init

        while self._state is not None:
            self._run_once()

    @property
    def location(self) -> str:
        return self.map.current.name

    @property
    def blacksmith_price(self) -> int:
        return self.map.current.blacksmith_price

    def get_location(self) -> Location:
        return self.map.get(self.location)

    def set_location(self, loc: str):
        self.map.set_location(loc)

    def combat_damage(self) -> int:
        assert self.enemy is not None, "No enemy set, combat failed"

        return max(self.enemy.battle_score - self.player.martial_prowess, 0)

    def char_menu(self):
        self.ui.print('######################')
        self.ui.print('Name: ' + self.player.name + '')
        self.ui.print('Race: ' + self.player.race + '')
        self.ui.print('Occupation: ' + self.player.occupation + '')
        self.ui.print('######################')
        self.ui.print('HP: ' + str(self.player.hp) + '/' + str(self.player.max_hp) + '')
        self.ui.print('Martial Prowess: ' + str(self.player.martial_prowess) + '')
        self.ui.print('Weapon: ' + self.player.weapon + '')
        self.ui.print('######################')
        self.ui.print('Consumption Rate: ' + str(self.player.consumption_rate) + '')
        self.ui.print('Food: ' + str(self.player.food) + '/' + str(self.player.max_food) + '')
        self.ui.print('Endurance: ' + str(self.player.endurance) + '')
        self.ui.print('Arrows: ' + str(self.player.arrows) + '/' + str(self.player.max_arrows) + '')
        self.ui.print('Gold: ' + str(self.player.gold) + '/' + str(self.player.max_gold) + '')
        self.ui.print('######################')
        # self.ui.print('Luck: ' + str(self.player.luck) + '')
        # self.ui.print('Speed: ' + str(self.player.speed) + '\n')
        # self.ui.print('Illness: ' + self.player.illness + '')
        # self.ui.print('######################\n')
        input('Press enter to continue')

    def adventure_menu(self):
        self.ui.print('######################')
        self.ui.print('HP: ' + str(self.player.hp) + '/' + str(self.player.max_hp) + '')
        self.ui.print('Food: ' + str(self.player.food) + '/' + str(self.player.max_food) + '')
        self.ui.print('Arrows: ' + str(self.player.arrows) + '/' + str(self.player.max_arrows) + '')
        self.ui.print('Gold: ' + str(self.player.gold) + '/' + str(self.player.max_gold) + '')
        self.ui.print('Endurance: ' + str(self.player.endurance) + '')
        self.ui.print('######################')
        self.ui.print('Martial Prowess: ' + str(self.player.martial_prowess) + '')
        self.ui.print('Weapon: ' + self.player.weapon + '')
        self.ui.print('Consumption Rate: ' + str(self.player.consumption_rate) + '')
        self.ui.print('######################\n')

    def town_description(self):
        if self.location == 'Goodshire':
            self.ui.print('The sun shines brightly on the lazy Halfling natives.')
        elif self.location == 'Rodez':
            self.ui.print('The sky is overcast, and your feet squelch in the mud from a recent rain.')
        elif self.location == 'Oristano':
            self.ui.print('The surrounding trees loom over the town like giants, and block the sun\'s rays.')
        elif self.location == 'Thasos':
            self.ui.print('A hot, dry wind blows clouds across the yellow sun, and you feel hot.')
        elif self.location == 'Karabuk':
            self.ui.print('There is a foul stench in the air, and the ground is covered bubbling puddles of unknown origin.')

    def display_map(self):
        self.ui.display_map(self.map)

    def at_end_location(self) -> bool:
        return self.location == self.map.end.name
