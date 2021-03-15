from typing import Optional
import random

from state import State, Context
from ui import ui
from enemy import get_enemy

from scenes import Adventuring


class Fight(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        ctx.enemy = get_enemy(enemy_locator_generator(ctx))
        ui.print(f"You see a {ctx.enemy.name} approaching.")

        if ctx.enemy.is_type("Doppelganger"):
            ui.print(f"The doppelganger is wielding a {ctx.player.weapon} exactly like yours.")

        selection = ui.choose(["Fight", "Flee"])
        if selection == 1:
            return FightSimulation(ctx)

        return FleeFight(ctx)


# Fight Simulation #
class FightSimulation(State):
    def do(self) -> Optional[State]:
        damage_taken = self.ctx.combat_damage()
        self.ctx.player.hp -= damage_taken

        if damage_taken < 1:
            ui.print("The enemy was slain, and you took no damage.")
        else:
            ui.print(f"The enemy was slain, but you took {damage_taken} damage.")

        return EndFight(self.ctx)


class EndFight(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        ctx.player.food += ctx.enemy.food
        ctx.player.arrows += ctx.enemy.arrows
        ctx.player.gold += ctx.enemy.gold

        ui.print(f"You found {ctx.enemy.food} food, "
                 f"{ctx.enemy.arrows} arrows, and"
                 f"{ctx.enemy.gold} gold on the corpse.")

        ctx.enemy = None

        ui.wait()
        return Adventuring(self.ctx)


# Flee Fight #
class FleeFight(State):
    def do(self) -> Optional[State]:
        n = random.randint(1, 2)
        if n == 2:
            ui.print("You failed to flee the fight.")

            ui.wait()
            return FightSimulation(self.ctx)

        ui.print("You escaped the fight.")

        ui.wait()
        return Adventuring(self.ctx)


# Enemy Locator and Excluder Generator #
def enemy_locator_generator(ctx: Context) -> int:
    location = ctx.get_location()

    enemy_number = random.randint(1, 5)
    while enemy_number in location.enemy_exclude:
        enemy_number = random.randint(1, 5)

    return enemy_number
