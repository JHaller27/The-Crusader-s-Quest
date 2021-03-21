from typing import Optional
import random

from state import State
from utils.ui import Singleton

import scenes.adventuring.adventuring as adventuring

ui = Singleton()


class Mushroom(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        ui.print("You see a strange mushroom.")
        selection = ui.choose(["Consume", "Leave"])
        if selection == 2:
            ui.print("You leave the mushroom.")

        elif ctx.player.is_race("Satyr"):
            extra_endurance = 3 * ctx.player.consumption_rate
            ctx.player.endurance += extra_endurance
            ui.print(f"You eat the mushroom, and gain {extra_endurance} Endurance.")

        else:
            event = random.randint(1, 4)

            if event == 1:
                ui.print("You eat the mushroom, and nothing happens.")

            elif event == 2:
                ui.print("You eat the mushroom, and it causes you to vomit.")

            elif event == 3:
                extra_endurance = 2 * ctx.player.consumption_rate
                ctx.player.consumption_rate += extra_endurance
                ui.print(f"You eat the mushroom, and gain {extra_endurance} Endurance.")

            else:
                ctx.player.hp = 0
                ctx.endurance = 0

                ui.print("You eat the mushroom, and then fall to the ground, foaming at the mouth.")

        ui.wait()
        return adventuring.Adventuring(self.ctx)
