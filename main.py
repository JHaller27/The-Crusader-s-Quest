# Python Text RPG
# Authored by: Gaga Gievous
# Copyright February 2021

import yaml

from utils import get_map
from utils.configs import Player as PlayerConfig
from state import Context

from scenes import TitleScreen


def main():
    with open("./configs/map.yml", "r") as fp:
        map_config = yaml.safe_load(fp)
    map_data = get_map(map_config)

    with open("./configs/player_options.yml", "r") as fp:
        player_config = yaml.safe_load(fp)
    player_config = PlayerConfig(player_config)

    with open("./configs/enemies.yml", "r") as fp:
        enemy_config = yaml.safe_load(fp)

    global_context = Context(map_data, player_config, enemy_config)
    global_context.run(TitleScreen(global_context))


if __name__ == "__main__":
    main()
