import yaml
import random


with open('./data/enemies.yml', 'r') as fp:
    config = yaml.safe_load(fp)


class Enemy:
    _adjective = ''
    _type = ''
    battle_score = 0
    gold = 0
    arrows = 0
    food = 0

    def __init__(self, adj: str, name: str):
        self._adjective = adj
        self._type = name

    def randomize_loot(self):
        self.food += random.randrange(10) + 1
        self.arrows += random.randrange(5) + 1
        self.gold += random.randrange(10) + 1

    @property
    def name(self) -> str:
        return f"{self._adjective} {self._type}"

    def is_type(self, enemy_type: str) -> bool:
        return self._type.lower() == enemy_type.lower()


def get_enemy(type_id: int) -> Enemy:
    enemy_type = config.get("types")[type_id - 1]

    adj = random.choice(config.get("adjectives"))

    enemy = Enemy(adj.get("name"), enemy_type.get("name"))
    enemy.battle_score = adj.get("battle_score") + enemy_type.get("battle_score")
    enemy.food = enemy_type.get("food")
    enemy.arrows = enemy_type.get("arrows")
    enemy.gold = enemy_type.get("gold")

    enemy.randomize_loot()

    return enemy
