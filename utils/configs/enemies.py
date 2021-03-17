import utils.configs.config_base as config_base


class EnemyType(config_base.ConfigBase):
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

    def __str__(self) -> str:
        return self.name


class Adjective(config_base.ConfigBase):
    @property
    def name(self) -> str:
        return self._get("name")

    @property
    def battle_score(self) -> int:
        return self._get("battle_score")

    def __str__(self) -> str:
        return self.name


class Enemies(config_base.ConfigBase):
    @property
    def types(self) -> list[EnemyType]:
        return [EnemyType(type_config) for type_config in self._get("types")]

    @property
    def adjectives(self) -> list[Adjective]:
        return [Adjective(adj_config) for adj_config in self._get("adjectives")]

    @property
    def final(self) -> EnemyType:
        return self._get("final")
