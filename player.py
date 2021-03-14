def sanitize_value(val: int, lower_bound: int = None, upper_bound: int = None) -> int:
    if lower_bound is not None and val < lower_bound:
        return lower_bound
    if upper_bound is not None and val > upper_bound:
        return upper_bound
    return val


class Player:
    name: str
    race: str
    occupation: str

    _hp: int
    max_hp: int

    _food: int
    max_food: int

    _arrows: int
    max_arrows: int

    _gold: int
    max_gold: int

    _endurance: int

    martial_prowess: int
    consumption_rate: int
    luck: int
    speed: int
    illness = None

    weapon = 'Sword'

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

    @property
    def arrows(self) -> int:
        return self._arrows

    @arrows.setter
    def arrows(self, val: int):
        self._arrows = sanitize_value(val, 0, self.max_arrows)

    @property
    def gold(self) -> int:
        return self._gold

    @gold.setter
    def gold(self, val: int):
        self._gold = sanitize_value(val, 0, self.max_gold)

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

    def fill_hp(self):
        self._hp = self.max_hp
