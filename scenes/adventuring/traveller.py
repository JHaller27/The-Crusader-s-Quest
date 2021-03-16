import random
from typing import Optional

from state import State, Context
from utils.ui import Singleton

import scenes.adventuring.adventuring as adventuring

ui = Singleton()


class Traveller(State):
    def do(self) -> Optional[State]:
        time_of_day = random.choice(["morning", "evening", "afternoon"])

        ui.print("A friendly adventurer approaches you and wants to trade.")
        ui.print(f'"Good {time_of_day}, traveler."\n')

        traveller_generation(self.ctx)
        ui.wait()

        return adventuring.Adventuring(self.ctx)


# Traveller Generation #
def traveller_generation(ctx: Context):
    x = random.randint(1, 50)  # how much trader wants
    v = random.randint(1, 100)  # how much trader is willing to give
    c = random.randint(1, 4)  # what trader wants

    if c == 1:
        ui.print(f'The trader wants {x} food.')
        p = random.randint(1, 3)  # what trader is giving
        if p == 1:
            ui.print(f'The trader is willing to give {v} arrows.')
            selection = ui.choose(["Accept", "Decline"])
            if selection == 1:
                if ctx.player.food < x:
                    ui.print('You cannot afford the trade.')
                else:
                    ctx.player.food = ctx.player.food - x
                    ctx.player.arrows = ctx.player.arrows + v
                    ui.print('You accept the trade.')

            else:
                ui.print('You decline the trade.')

        if p == 2:
            ui.print(f'The trader is willing to pay {v} gold.')
            selection = ui.choose(["Accept", "Decline"])
            if selection == 1:
                if ctx.player.food < x:
                    ui.print('You cannot afford the trade.')
                else:
                    ctx.player.food = ctx.player.food - x
                    ctx.player.gold = ctx.player.gold + v
                    ui.print('You accept the trade.')

            else:
                ui.print('You decline the trade.')

        if p == 3:
            ui.print(f'The trader is willing to heal you {v} HP.')
            selection = ui.choose(["Accept", "Decline"])
            if selection == 1:
                if ctx.player.food < x:
                    ui.print('You cannot afford the trade.')
                else:
                    ctx.player.food = ctx.player.food - x
                    ctx.player.hp += v
                    ui.print('You accept the trade.')

            else:
                ui.print('You decline the trade.')
    if c == 2:
        ui.print(f'The trader wants {x} arrows.')
        p = random.randint(1, 3)  # what trader is giving
        if p == 1:
            ui.print(f'The trader is willing to give {v} food.')
            selection = ui.choose(["Accept", "Decline"])
            if selection == 1:
                if ctx.player.arrows < x:
                    ui.print('You cannot afford the trade.')
                else:
                    ctx.player.arrows = ctx.player.arrows - x
                    ctx.player.food = ctx.player.food + v
                    ui.print('You accept the trade.')

            else:
                ui.print('You decline the trade.')
        if p == 2:
            ui.print(f'The trader is willing to give {v} gold.')
            selection = ui.choose(["Accept", "Decline"])
            if selection == 1:
                if ctx.player.arrows < x:
                    ui.print('You cannot afford the trade.')
                else:
                    ctx.player.arrows = ctx.player.arrows - x
                    ctx.player.gold = ctx.player.gold + v
                    ui.print('You accept the trade.')

            else:
                ui.print('You decline the trade.')
        if p == 3:
            ui.print(f'The trader is willing to heal you for {v} HP.')
            selection = ui.choose(["Accept", "Decline"])
            if selection == 1:
                if ctx.player.arrows < x:
                    ui.print('You cannot afford the trade.')
                else:
                    ctx.player.arrows -= x
                    ctx.player.hp += v
                    ui.print('You accept the trade.')

            else:
                ui.print('You decline the trade.')
    if c == 3:
        ui.print(f'The trader wants {x} gold.')
        p = random.randint(1, 3)  # what trader is giving
        if p == 1:
            ui.print(f'The trader is willing to give {v} food.')
            selection = ui.choose(["Accept", "Decline"])
            if selection == 1:
                if ctx.player.gold < x:
                    ui.print('You cannot afford the trade.')
                else:
                    ctx.player.gold = ctx.player.gold - x
                    ctx.player.food = ctx.player.food + v
                    ui.print('You accept the trade.')

            else:
                ui.print('You decline the trade.')
        if p == 2:
            ui.print(f'The trader is willing to give {v} arrows.')
            selection = ui.choose(["Accept", "Decline"])
            if selection == 1:
                if ctx.player.gold < x:
                    ui.print('You cannot afford the trade.')
                else:
                    ctx.player.gold = ctx.player.gold - x
                    ctx.player.arrows = ctx.player.arrows + v
                    ui.print('You accept the trade.')

            else:
                ui.print('You decline the trade.')

        if p == 3:
            ui.print(f'The trader is willing to heal you {v} HP.')
            selection = ui.choose(["Accept", "Decline"])
            if selection == 1:
                if ctx.player.gold < x:
                    ui.print('You cannot afford the trade.')
                else:
                    ctx.player.gold -= x
                    ctx.player.hp += v
                    ui.print('You accept the trade.')

            else:
                ui.print('You decline the trade.')
    if c == 4:
        ui.print(f'The trader wants your blood. Specifically, {x} HP.')
        p = random.randint(1, 3)  # what trader is giving
        if p == 1:
            ui.print(f'The trader is willing to give {v} food.')
            selection = ui.choose(["Accept", "Decline"])
            if selection == 1:
                if ctx.player.hp < x:
                    ui.print('You cannot afford the trade, but the trader is willing to let you slide, this time.')
                    ctx.player.hp = ctx.player.hp - x
                    ctx.player.food = ctx.player.food + v
                else:
                    ctx.player.hp = ctx.player.hp - x
                    ctx.player.food = ctx.player.food + v
                    ui.print('You accept the trade.')

            else:
                ui.print('You decline the trade.')
        if p == 2:
            ui.print(f'The trader is willing to give {v} arrows.')
            selection = ui.choose(["Accept", "Decline"])
            if selection == 1:
                if ctx.player.hp < x:
                    ui.print('You cannot afford the trade, but the trader is willing to let you slide, this time.')
                    ctx.player.hp = ctx.player.hp - x
                    ctx.player.food = ctx.player.food + v
                else:
                    ctx.player.hp = ctx.player.hp - x
                    ctx.player.arrows = ctx.player.arrows + v
                    ui.print('You accept the trade.')

            else:
                ui.print('You decline the trade.')
        if p == 3:
            ui.print(f'The trader is willing to give {v} gold.')
            selection = ui.choose(["Accept", "Decline"])
            if selection == 1:
                if ctx.player.hp < x:
                    ui.print('You cannot afford the trade, but the trader is willing to let you slide, this time.')
                    ctx.player.hp = ctx.player.hp - x
                    ctx.player.food = ctx.player.food + v
                else:
                    ctx.player.hp = ctx.player.hp - x
                    ctx.player.gold = ctx.player.gold + v
                    ui.print('You accept the trade.')

            else:
                ui.print('You decline the trade.')
