from typing import Optional
import random

from state import State, Context
from utils.ui import Singleton

import scenes.adventuring.random_events as random_events
import scenes.adventuring.adventuring as adventuring

ui = Singleton()


class _Choice:
    def __init__(self, ctx: Context, resource_name: str, container_name: str):
        self._ctx = ctx
        self._name = resource_name
        self._container = container_name

    @property
    def ctx(self) -> Context:
        return self._ctx

    @property
    def resource_name(self) -> str:
        return self._name

    @property
    def container_name(self) -> str:
        return self._container

    @property
    def _resource(self) -> int:
        raise NotImplementedError

    @_resource.setter
    def _resource(self, val: int):
        raise NotImplementedError

    def is_empty(self) -> bool:
        return self._resource == 0

    def reduce_resource(self, amt: int) -> int:
        old = self._resource
        amt = min(old, amt)
        self._resource -= amt

        return amt


class _Arrows(_Choice):
    def __init__(self, ctx: Context):
        super().__init__(ctx, "arrows", "quiver")

    @property
    def _resource(self) -> int:
        return self.ctx.player.arrows

    @_resource.setter
    def _resource(self, val: int):
        self.ctx.player.arrows = val


class _Food(_Choice):
    def __init__(self, ctx: Context):
        super().__init__(ctx, "food", "food supply")

    @property
    def _resource(self) -> int:
        return self.ctx.player.food

    @_resource.setter
    def _resource(self, val: int):
        self.ctx.player.food = val


class _Gold(_Choice):
    def __init__(self, ctx: Context):
        super().__init__(ctx, "gold", "coin purse")

    @property
    def _resource(self) -> int:
        return self.ctx.player.gold

    @_resource.setter
    def _resource(self, val: int):
        self.ctx.player.gold = val


class Robbed(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        choices = [_Arrows(ctx), _Food(ctx), _Gold(ctx)]
        choices = [c for c in choices if not c.is_empty()]

        if len(choices) == 0:
            return random_events.NoEvent(self.ctx)

        choice = random.choice(choices)

        amt = choice.reduce_resource(random.randint(1, 50))
        fmt = random.choice([
            "During the night, a shadowy figure stole {0} of your {1}.",
            "You check your {2} and find that {0} {1} is missing.",
        ])

        ui.print(fmt.format(amt, choice.resource_name, choice.container_name))
        ui.wait()

        return adventuring.Adventuring(self.ctx)
