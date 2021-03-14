from typing import Optional, Type

from ui import UserInterface
from map import Map, Location


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

    name = ''
    hp = 0
    max_hp = 0

    martial_prowess = 0
    consumption_rate = 10
    endurance = 10
    food = 0
    max_food = 0
    race = ''
    luck = 0
    arrows = 0
    max_arrows = 0
    speed = 0
    occupation = ''
    illness = 'None'
    gold = 100
    max_gold = 0

    blacksmith_price = 500

    weapon = 'Sword'
    weapon_type = 'sword'

    days_to_go = 0
    adventure_state = False

    enemy_adjective = ''
    enemy_type = ''
    enemy_locator = ''
    enemy_number = ''
    enemy_exclude = 0
    enemy_battle_score = 0
    enemy_gold = 0
    enemy_arrows = 0
    enemy_food = 0
    enemy_specific_gold = 0
    enemy_specific_arrows = 0
    enemy_specific_food = 0
    damage_taken = 0

    _state = None

    def __init__(self, ui: UserInterface, map_obj: Map):
        self.ui = ui
        self.map = map_obj

        self.location = self.map.start.name

    def _run_once(self):
        self.ui.debug(f"Running state '{type(self._state).__name__}'")
        self._state = self._state.do()

    def run(self, init: Optional[State]):
        self._state = init

        while self._state is not None:
            self._run_once()

    def get_location(self) -> Location:
        return self.map.get(self.location)

    def set_location(self, loc: str):
        self.location = loc
        loc_obj = self.map.get(loc)
        loc_obj.visit()

    def char_menu(self):
        self.ui.print('######################')
        self.ui.print('Name: ' + self.name + '')
        self.ui.print('Race: ' + self.race + '')
        self.ui.print('Occupation: ' + self.occupation + '')
        self.ui.print('######################')
        self.ui.print('HP: ' + str(self.hp) + '/' + str(self.max_hp) + '')
        self.ui.print('Martial Prowess: ' + str(self.martial_prowess) + '')
        self.ui.print('Weapon: ' + self.weapon + '')
        self.ui.print('######################')
        self.ui.print('Consumption Rate: ' + str(self.consumption_rate) + '')
        self.ui.print('Food: ' + str(self.food) + '/' + str(self.max_food) + '')
        self.ui.print('Endurance: ' + str(self.endurance) + '')
        self.ui.print('Arrows: ' + str(self.arrows) + '/' + str(self.max_arrows) + '')
        self.ui.print('######################')
        # self.ui.print('Luck: ' + str(self.luck) + '')
        # self.ui.print('Speed: ' + str(self.speed) + '\n')
        # self.ui.print('Illness: ' + self.illness + '')
        self.ui.print('Gold: ' + str(self.gold) + '/' + str(self.max_gold) + '')
        self.ui.print('######################\n')
        input('Press enter to continue')

    def adventure_menu(self):
        self.ui.print('######################')
        self.ui.print('HP: ' + str(self.hp) + '/' + str(self.max_hp) + '')
        self.ui.print('Food: ' + str(self.food) + '/' + str(self.max_food) + '')
        self.ui.print('Arrows: ' + str(self.arrows) + '/' + str(self.max_arrows) + '')
        self.ui.print('Gold: ' + str(self.gold) + '/' + str(self.max_gold) + '')
        self.ui.print('Endurance: ' + str(self.endurance) + '')
        self.ui.print('######################')
        self.ui.print('Martial Prowess: ' + str(self.martial_prowess) + '')
        self.ui.print('Weapon: ' + self.weapon + '')
        self.ui.print('Consumption Rate: ' + str(self.consumption_rate) + '')
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

    def hp_mechanic(self, death: Type[State]):
        if self.hp > self.max_hp:
            self.hp = self.max_hp
            self.ui.print('You have max HP.')
        if self.hp < 1:
            self.hp = 0
            self._state = death(self)

    def food_endurance_mechanic(self, death: Type[State]):
        if self.consumption_rate > self.food > 0:
            self.food = 0
        elif self.food > 1:
            self.food = self.food - self.consumption_rate
        elif self.food < 1:
            self.food = 0
            self.endurance = self.endurance - self.consumption_rate
            if self.endurance < 1:
                self.endurance = 0
                self._state = death(self)
        # need to work on restoring endurance#

    def display_map(self):
        self.ui.display_map(self.map)

    def at_end_location(self) -> bool:
        return self.location == self.map.end.name
