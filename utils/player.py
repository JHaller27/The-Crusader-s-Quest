from utils import ui


def sanitize_value(val: int, lower_bound: int = None, upper_bound: int = None) -> int:
    if lower_bound is not None and val < lower_bound:
        return lower_bound
    if upper_bound is not None and val > upper_bound:
        return upper_bound
    return val


class Player:
    name = ""
    race = ""
    occupation = ""

    _hp = 0
    max_hp = 0

    _food = 0
    max_food = 0

    _arrows = 0
    max_arrows = 0

    _gold = 0
    max_gold = 0

    _endurance = 0

    martial_prowess = 0
    consumption_rate = 0
    luck = 0
    speed = 0
    illness = None

    weapon = ""

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, val: int):
        self._hp = sanitize_value(val, 0, self.max_hp)

    @property
    def food(self) -> int:
        return self._food

    @food.setter
    def food(self, val: int):
        self._food = sanitize_value(val, 0, self.max_food)
        if self._food == self.max_food:
            ui.print("You have maxed out your food supply.")

    @property
    def arrows(self) -> int:
        return self._arrows

    @arrows.setter
    def arrows(self, val: int):
        self._arrows = sanitize_value(val, 0, self.max_arrows)
        if self._arrows == self.max_arrows:
            ui.print("You have maxed out your arrow count.")

    @property
    def gold(self) -> int:
        return self._gold

    @gold.setter
    def gold(self, val: int):
        self._gold = sanitize_value(val, 0, self.max_gold)
        if self._gold == self.max_gold:
            ui.print("You have completely filled your coin purse.")

    @property
    def endurance(self) -> int:
        return self._endurance

    @endurance.setter
    def endurance(self, val: int):
        self._endurance = sanitize_value(val, 0)

    @property
    def description(self) -> str:
        return f"You are {self.name}, the {self.race} {self.occupation}. " \
               f"You wield a {self.weapon}."

    def is_alive(self) -> bool:
        return self.hp > 0 and self.endurance > 0

    def is_full_health(self) -> bool:
        return self.hp == self.max_hp

    def is_race(self, race: str) -> bool:
        return self.race.lower() == race.lower()

    def fill_hp(self):
        self._hp = self.max_hp

    def fill_food(self):
        self._food = self.max_food

    def fill_arrows(self):
        self._arrows = self.max_arrows

    def fill_gold(self):
        self._gold = self.max_gold
