from .config_base import ConfigBase


class EnemyType(ConfigBase):
    @property
    def name(self) -> str:
        return self._get("name")

    @property
    def battle_score(self) -> int:
        return self._get("battle_score")

    @property
    def food(self) -> int:
        return self._get("food")

    @property
    def arrows(self) -> int:
        return self._get("arrows")

    @property
    def gold(self) -> int:
        return self._get("gold")


class Adjective(ConfigBase):
    @property
    def name(self) -> str:
        return self._get("name")

    @property
    def battle_score(self) -> int:
        return self._get("battle_score")


class Enemies(ConfigBase):
    @property
    def types(self) -> list[EnemyType]:
        return [EnemyType(type_config) for type_config in self._get("types")]

    @property
    def adjectives(self) -> list[Adjective]:
        return [Adjective(adj_config) for adj_config in self._get("adjectives")]

    @property
    def final(self) -> EnemyType:
        return self._get("final")
