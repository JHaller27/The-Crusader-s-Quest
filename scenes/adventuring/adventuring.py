from typing import Optional
import random

from state import State
from utils.ui import Singleton

import scenes.adventuring.random_events as random_events
import scenes.introduction
import scenes.town
import scenes.finalBattle

ui = Singleton()


# Hunt #
class Hunt(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        arrows_shot = min(random.randint(1, 10), self.ctx.player.arrows)
        food_found = random.randint(1, 25)

        if ctx.player.arrows == 0:
            ui.print("You do not have any arrows to hunt with.")

        else:
            ctx.player.arrows -= arrows_shot
            ctx.player.food += food_found

            ui.clear()
            self.ctx.adventure_menu()

            ui.print(f"You shot {arrows_shot} arrows, and gained {food_found} food.")

        ui.wait()

        return Adventuring(self.ctx)


# Rest #
class Rest(State):
    def do(self) -> Optional[State]:
        if self.ctx.player.is_full_health():
            ui.print("You rest for one day. Your HP is already maxed out.")

        else:
            restored_hp = random.randint(15, 25)

            self.ctx.player.hp += restored_hp
            ui.print(f"You rest for one day, gaining {restored_hp} HP.")

        ui.wait()

        return Adventuring(self.ctx)


class Adventuring(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        if not ctx.player.is_alive():
            return Death(self.ctx)

        if ctx.counter == 0:
            return EndAdventure(self.ctx)

        self.ctx.adventure_menu()
        selection = ui.choose(["Continue", "Hunt", "Rest", "Map"])

        if selection == 1:
            ctx.counter -= 1

            return random_events.RandomEvent(self.ctx)

        elif selection == 2:
            return Hunt(self.ctx)

        elif selection == 3:
            return Rest(self.ctx)

        elif selection == 4:
            return TheMap(self.ctx)


class EndAdventure(State):
    def do(self) -> Optional[State]:
        ui.clear()
        self.ctx.adventure_menu()

        ui.print("You have survived the trip.")
        ui.wait()

        return LocationChanger(self.ctx)


# Death #
class Death(State):
    def do(self) -> Optional[State]:
        ui.clear()
        ui.print("You have died.\n")
        ui.wait()

        self.ctx.char_menu()
        ui.print()
        ui.wait("return to menu")

        return scenes.introduction.TitleScreen(self.ctx)


# Map #
class TheMap(State):
    def do(self) -> Optional[State]:
        ui.clear()
        ui.display_map(self.ctx.map)

        ui.print(f"You have {self.ctx.counter} days to go.")
        ui.wait()

        return Adventuring(self.ctx)


# Location Changer #
class LocationChanger(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        ctx.map.move()

        if ctx.map.at_end_location():
            return scenes.finalBattle.FinalBattle(self.ctx)

        return scenes.town.Town(self.ctx)
