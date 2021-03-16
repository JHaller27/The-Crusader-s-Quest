# Python Text RPG
# Authored by: Gaga Gievous
# Copyright February 2021

import yaml

from utils.map import Map
from utils.configs.player import Player as PlayerConfig
from utils.configs.map import Map as MapConfig
from utils.configs.enemies import Enemies as EnemiesConfig
from state import Context

from scenes.introduction import TitleScreen
from utils.ui import DebugInterfaceDecorator, FilePlayer, Singleton

ui = Singleton()


def init_debug():
    with open("./data/dummy_player.txt", "r") as fp:
        file_data = [line.strip() for line in fp]

    ui.decorate(DebugInterfaceDecorator(ui.base))
    ui.decorate(FilePlayer(ui.base, file_data))


def main():
    with open("./configs/map.yml", "r") as fp:
        map_config = yaml.safe_load(fp)
    map_config = MapConfig(map_config)
    map_data = Map(map_config)

    with open("./configs/player_options.yml", "r") as fp:
        player_config = yaml.safe_load(fp)
    player_config = PlayerConfig(player_config)

    with open("./configs/enemies.yml", "r") as fp:
        enemy_config = yaml.safe_load(fp)
    enemy_config = EnemiesConfig(enemy_config)

    global_context = Context(map_data, player_config, enemy_config)
    global_context.run(TitleScreen(global_context))


if __name__ == "__main__":
    init_debug()
    main()
