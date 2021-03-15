from .config_base import ConfigBase


class Race(ConfigBase):
    @property
    def name(self) -> str:
        return self._get("name")

    @property
    def hp(self) -> int:
        return self._get("hp")

    @property
    def martial_prowess(self) -> int:
        return self._get("martial_prowess")

    @property
    def consumption_rate(self) -> int:
        return self._get("consumption_rate")

    @property
    def endurance(self) -> int:
        return self._get("endurance")

    @property
    def gold(self) -> int:
        return self._get("gold")

    @property
    def luck(self) -> int:
        return self._get("luck")

    @property
    def speed(self) -> int:
        return self._get("speed")


class Occupation(ConfigBase):
    @property
    def name(self) -> str:
        return self._get("name")

    @property
    def hp(self) -> int:
        return self._get("hp")

    @property
    def food(self) -> int:
        return self._get("food", "curr")

    @property
    def max_food(self) -> int:
        return self._get("food", "max")

    @property
    def arrows(self) -> int:
        return self._get("arrows", "curr")

    @property
    def max_arrows(self) -> int:
        return self._get("arrows", "max")

    @property
    def gold(self) -> int:
        return self._get("gold", "curr")

    @property
    def max_gold(self) -> int:
        return self._get("gold", "max")

    @property
    def martial_prowess(self) -> int:
        return self._get("martial_prowess")


class Player(ConfigBase):
    @property
    def races(self) -> list[Race]:
        return [Race(race_dict) for race_dict in self._get("races")]

    @property
    def occupations(self) -> list[Occupation]:
        return [Occupation(occ_dict) for occ_dict in self._get("occupations")]
