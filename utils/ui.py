import os
from typing import Optional

import utils.player as player_utils
import utils.map as map_utils


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

    def display_map(self, map_obj: map_utils.Map):
        raise NotImplementedError

    def adventure_menu(self, player: player_utils.Player):
        raise NotImplementedError

    def char_menu(self, player: player_utils.Player):
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

    def display_map(self, map_obj: map_utils.Map):
        def opt_loc_to_chr(loc: Optional[map_utils.Location]):
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

    def _display_basic_player_info(self, player: player_utils.Player):
        self._print_sep()
        self.print(f"Name: {player.name}")
        self.print(f"Race: {player.race}")
        self.print(f"Occupation: {player.occupation}")
        self._print_sep()

    def _display_combat_stats(self, player: player_utils.Player):
        self._print_sep()
        self.print(f"HP: {player.hp} / {player.max_hp}")
        self.print(f"Martial Prowess: {player.martial_prowess}")
        self.print(f"Weapon: {player.weapon}")
        self._print_sep()

    def _display_resources(self, player: player_utils.Player):
        self._print_sep()
        self.print(f"Consumption Rate:{player.consumption_rate}")
        self.print(f"Food:{player.food}/{player.max_food}")
        self.print(f"Endurance:{player.endurance}")
        self.print(f"Arrows:{player.arrows}/{player.max_arrows}")
        self.print(f"Gold:{player.gold}/{player.max_gold}")
        self._print_sep()

    def adventure_menu(self, player: player_utils.Player):
        self._display_combat_stats(player)
        self._display_resources(player)

    def char_menu(self, player: player_utils.Player):
        self._display_basic_player_info(player)
        self._display_combat_stats(player)
        self._display_resources(player)


class InterfaceDecorator(UserInterface):
    def __init__(self, base: UserInterface):
        self._base = base

    @property
    def base(self) -> UserInterface:
        return self._base

    @base.setter
    def base(self, val: UserInterface):
        self._base = val

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

    def display_map(self, map_obj: map_utils.Map):
        return self.base.display_map(map_obj)

    def adventure_menu(self, player: player_utils.Player):
        return self.base.adventure_menu(player)

    def char_menu(self, player: player_utils.Player):
        return self.base.char_menu(player)


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


class FilePlayer(InterfaceDecorator):
    def __init__(self, base: UserInterface, data: list[str]):
        super().__init__(base)
        self._data_iter = iter(data)

    def _read(self):
        data = next(self._data_iter)
        print(f"<<< {data}")

        return data

    def choose(self, options: list[str]) -> int:
        try:
            return int(self._read())
        except StopIteration:
            return self.base.choose(options)

    def input_text(self) -> str:
        try:
            return self._read()
        except StopIteration:
            return self.base.input_text()


# To be honest, this Singleton implementation is mostly black magic pulled from
# refactoring.guru/design-patterns/singleton/python/example
class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instance = None

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls._instance is None:
            instance = super().__call__(*args, **kwargs)
            cls._instance = instance
        return cls._instance


class Singleton(InterfaceDecorator, metaclass=SingletonMeta):
    def __init__(self, base: UserInterface = None):
        super().__init__(base)

    def decorate(self, decorator: InterfaceDecorator):
        self.base = decorator


Singleton(ConsoleInterface())
