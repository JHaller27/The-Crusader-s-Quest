import os
from typing import Optional

from .player import Player
from .map import Map, Location


class UserInterface:
    """
    This allows us to have multiple kinds of UIs, and to swap them out easily.
    E.g. switching from a terminal-based UI to an interface window is as easy as
    creating a new class inheriting from UserInterface, then creating that instead of an existing UI.
    """
    def clear(self):
        raise NotImplementedError

    def print(self, text=''):
        raise NotImplementedError

    def debug(self, text=''):
        pass

    def wait(self, do=None):
        raise NotImplementedError

    def choose(self, options: list[str]) -> int:
        raise NotImplementedError

    def input_text(self) -> str:
        raise NotImplementedError

    def display_map(self, map_obj: Map):
        raise NotImplementedError

    def display_basic_player_info(self, player: Player):
        raise NotImplementedError

    def display_combat_stats(self, player: Player):
        raise NotImplementedError

    def display_resources(self, player: Player):
        raise NotImplementedError


class ConsoleInterface(UserInterface):
    def __init__(self):
        self._last_printed_sep = False

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def print(self, text=''):
        print(text)
        self._last_printed_sep = False

    def wait(self, do=None):
        if do is None:
            do = 'continue'

        input(f"Press enter to {do}")

    def choose(self, options: list[str]) -> int:
        for i, opt in enumerate(options):
            print(f"{i + 1} {opt}")

        have_valid_value = False
        while not have_valid_value:
            selection = self.input_text()
            try:
                selection = int(selection)
            except ValueError:
                self.print(f"'{selection}' is not a valid choice")
                selection = -1
            finally:
                have_valid_value = 1 <= selection <= len(options)

        # noinspection PyUnboundLocalVariable
        return selection

    def input_text(self) -> str:
        return input(">: ")

    def display_map(self, map_obj: Map):
        def opt_loc_to_chr(loc: Optional[Location]):
            if loc is None:
                return ' '
            if not loc.visited:
                return 'X'
            return loc.name[0]

        for r_idx, r in enumerate(map_obj.grid):
            if r_idx == 0:
                print("╔" + "═══╤" * (map_obj.width - 1) + "═══╗")
            else:
                print("╟" + "───┼" * (map_obj.width - 1) + "───╢")
            print(f"║ " + " │ ".join(map(opt_loc_to_chr, r)) + " ║")
        print("╚" + "═══╧" * (map_obj.width - 1) + "═══╝")

    def _print_sep(self):
        if not self._last_printed_sep:
            self.print('######################')
            self._last_printed_sep = True

    def display_basic_player_info(self, player: Player):
        self._print_sep()
        self.print(f"Name: {player.name}")
        self.print(f"Race: {player.race}")
        self.print(f"Occupation: {player.occupation}")
        self._print_sep()

    def display_combat_stats(self, player: Player):
        self._print_sep()
        self.print(f"HP: {player.hp} / {player.max_hp}")
        self.print(f"Martial Prowess: {player.martial_prowess}")
        self.print(f"Weapon: {player.weapon}")
        self._print_sep()

    def display_resources(self, player: Player):
        self._print_sep()
        self.print(f"Consumption Rate:{player.consumption_rate}")
        self.print(f"Food:{player.food}/{player.max_food}")
        self.print(f"Endurance:{player.endurance}")
        self.print(f"Arrows:{player.arrows}/{player.max_arrows}")
        self.print(f"Gold:{player.gold}/{player.max_gold}")
        self._print_sep()


class InterfaceDecorator(UserInterface):
    def __init__(self, base: UserInterface):
        self._base = base

    @property
    def base(self) -> UserInterface:
        return self._base

    def clear(self):
        return self.base.clear()

    def print(self, text=''):
        return self.base.print(text)

    def debug(self, text=''):
        return self.base.debug(text)

    def wait(self, do=None):
        return self.base.wait(do)

    def choose(self, options: list[str]) -> int:
        return self.base.choose(options)

    def input_text(self) -> str:
        return self.base.input_text()

    def display_map(self, map_obj: Map):
        return self.base.display_map(map_obj)

    def display_basic_player_info(self, player: Player):
        return self.base.display_basic_player_info(player)

    def display_combat_stats(self, player: Player):
        return self.base.display_combat_stats(player)

    def display_resources(self, player: Player):
        return self.base.display_resources(player)


class DebugInterfaceDecorator(InterfaceDecorator):
    """
    This will mostly pass through to _base. This way, all possible UserInterfaces
    can be decorated with this class for debugging.

    For example:
    ui = ConsoleInterface()  # Create the base
    ui = DebugInterfaceDecorator(ui)  # Optionally, allow debugging
    """

    def __init__(self, base):
        super().__init__(base)

    @staticmethod
    def _debug(text):
        print(f"~~~~~~~~~~  {text}")

    def clear(self):
        self._debug("clear screen")

    def debug(self, text=''):
        self._debug(text)


ui = ConsoleInterface()
ui = DebugInterfaceDecorator(ui)
