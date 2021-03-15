# Python Text RPG
# Authored by: Gaga Gievous
# Copyright February 2021

from map import get_map
from state import Context

from scenes import TitleScreen


def main():
    map_data = get_map("./data/map.yml")

    global_context = Context(map_data)
    global_context.run(TitleScreen(global_context))


if __name__ == "__main__":
    main()
