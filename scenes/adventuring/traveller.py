import random
from typing import Optional

from state import State, Context
from utils.ui import Singleton

import scenes.adventuring.adventuring as adventuring

ui = Singleton()


class _Choice:
    def __init__(self, ctx: Context,
                 want_fmt: str, want_amt: int,
                 give_fmt: str, give_amt: int,
                 cant_afford: str):
        self._ctx = ctx
        self._want_fmt = want_fmt
        self._want_amt = want_amt
        self._give_fmt = give_fmt
        self._give_amt = give_amt
        self._cant_afford = cant_afford

    @property
    def ctx(self) -> Context:
        return self._ctx

    @property
    def want_text(self) -> str:
        return self._want_fmt.format(self._want_amt)

    @property
    def give_text(self) -> str:
        return self._give_fmt.format(self._give_amt)

    @property
    def _resource(self) -> int:
        raise NotImplementedError

    @_resource.setter
    def _resource(self, val: int):
        raise NotImplementedError

    def pay(self) -> bool:
        if self._resource < self._want_amt:
            ui.print(self._cant_afford)
            return False

        self._resource -= self._want_amt
        return True

    def give(self):
        self._resource += self._give_amt


class _Arrows(_Choice):
    def __init__(self, ctx: Context, want_amt: int, give_amt: int):
        super().__init__(ctx,
                         "The trader wants {0} arrows.", want_amt,
                         "The trader is willing to give {0} arrows.", give_amt,
                         "You cannot afford the trade.")

    @property
    def _resource(self) -> int:
        return self.ctx.player.arrows

    @_resource.setter
    def _resource(self, val: int):
        self.ctx.player.arrows = val


class _Food(_Choice):
    def __init__(self, ctx: Context, want_amt: int, give_amt: int):
        super().__init__(ctx,
                         "The trader wants {0} food.", want_amt,
                         "The trader is willing to give {0} food.", give_amt,
                         "You cannot afford the trade.")

    @property
    def _resource(self) -> int:
        return self.ctx.player.food

    @_resource.setter
    def _resource(self, val: int):
        self.ctx.player.food = val


class _Gold(_Choice):
    def __init__(self, ctx: Context, want_amt: int, give_amt: int):
        super().__init__(ctx,
                         "The trader wants {0} gold.", want_amt,
                         "The trader is willing to give {0} gold.", give_amt,
                         "You cannot afford the trade.")

    @property
    def _resource(self) -> int:
        return self.ctx.player.gold

    @_resource.setter
    def _resource(self, val: int):
        self.ctx.player.gold = val


class _Health(_Choice):
    def __init__(self, ctx: Context, want_amt: int, give_amt: int):
        super().__init__(ctx,
                         "The trader wants your blood. Specifically, {0} HP.", want_amt,
                         "The trader is willing to heal you for {0} HP.", give_amt,
                         "You cannot afford the trade, but the trader is willing to let you slide, this time.")

    @property
    def _resource(self) -> int:
        return self.ctx.player.hp

    @_resource.setter
    def _resource(self, val: int):
        self.ctx.player.hp = val

    def pay(self) -> bool:
        super().pay()
        return True


class Traveller(State):
    def do(self) -> Optional[State]:
        time_of_day = random.choice(["morning", "evening", "afternoon"])

        ui.print("A friendly adventurer approaches you and wants to trade.")
        ui.print(f'"Good {time_of_day}, traveler."\n')

        want_amt = random.randint(1, 50)  # how much trader wants
        give_amt = random.randint(1, 100)  # how much trader is willing to give

        choices: list[_Choice] = [
            _Arrows(self.ctx, want_amt, give_amt),
            _Food(self.ctx, want_amt, give_amt),
            _Gold(self.ctx, want_amt, give_amt),
            _Health(self.ctx, want_amt, give_amt),
        ]
        random.shuffle(choices)

        want_choice = choices.pop()
        give_choice = choices.pop()

        ui.print(want_choice.want_text)
        ui.print(give_choice.give_text)

        selection = ui.choose(["Accept", "Decline"])
        if selection == 1:
            if want_choice.pay():
                ui.print("You accept the trade.")
                give_choice.give()
        else:
            ui.print("You decline the trade.")

        ui.wait()

        return adventuring.Adventuring(self.ctx)
