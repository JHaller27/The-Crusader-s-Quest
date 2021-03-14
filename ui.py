import os


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


class ConsoleInterface(UserInterface):
    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def print(self, text=''):
        print(text)

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


class DebugInterfaceDecorator(UserInterface):
    """
    This will mostly pass through to _base. This way, all possible UserInterfaces
    can be decorated with this class for debugging.

    For example:
    ui = ConsoleInterface()  # Create the base
    ui = DebugInterfaceDecorator(ui)  # Optionally, allow debugging
    """

    def __init__(self, base):
        self._base = base

    @staticmethod
    def _debug(text):
        print(f"~~~~~~~~~~  {text}")

    def clear(self):
        self._debug("clear screen")

    def debug(self, text=''):
        self._debug(text)

    def print(self, text=''):
        self._base.print(text)

    def choose(self, options: list[str]) -> int:
        return self._base.choose(options)

    def wait(self, do=None):
        self._base.wait(do)

    def input_text(self) -> str:
        return self._base.input_text()
