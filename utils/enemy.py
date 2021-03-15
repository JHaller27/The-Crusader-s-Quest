import random


class Enemy:
    _adjective = ''
    _type = ''
    _battle_score = 0
    gold = 0
    arrows = 0
    food = 0

    def __init__(self, adj: str, name: str, battle_score: int):
        self._adjective = adj
        self._type = name
        self._battle_score = battle_score

    def randomize_loot(self):
        self.food += random.randrange(10) + 1
        self.arrows += random.randrange(5) + 1
        self.gold += random.randrange(10) + 1

    @property
    def name(self) -> str:
        return f"{self._adjective} {self._type}"

    @property
    def battle_score(self) -> int:
        return self._battle_score

    def is_type(self, enemy_type: str) -> bool:
        return self._type.lower() == enemy_type.lower()


def get_enemy(type_id: int, config: dict) -> Enemy:
    enemy_type = config.get("types")[type_id - 1]
    type_name = enemy_type.get("name")

    adj = random.choice(config.get("adjectives"))
    adj_name = adj.get("name")

    battle_score = adj.get("battle_score") + enemy_type.get("battle_score")

    enemy = Enemy(adj_name, type_name, battle_score)

    enemy.food = enemy_type.get("food")
    enemy.arrows = enemy_type.get("arrows")
    enemy.gold = enemy_type.get("gold")

    enemy.randomize_loot()

    return enemy
