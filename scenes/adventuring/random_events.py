from typing import Optional, Type
import random

from state import State
from utils.ui import Singleton

import scenes.adventuring.traveller as traveller
import scenes.adventuring.fight as fight
import scenes.adventuring.adventuring as adventuring

ui = Singleton()


class RandomEvent(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        ui.clear()
        ui.adventure_menu(self.ctx.player)

        next_state: State = random.choice([
            Chest,
            fight.Fight,
            Robbed,
            traveller.Traveller,
            Damaged,
            Miracle,
            Mushroom,
            NoEvent,
            fight.Fight,
            fight.Fight,
            Chest,
            fight.Fight,
            Robbed,
            traveller.Traveller,
            Damaged,
            Mystic,
            BiggerBag,
            LoseDay,
            fight.Fight,
            fight.Fight,
        ])[0](ctx)

        return next_state


# Mushroom #
class Mushroom(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        ui.print("You see a strange mushroom.")
        selection = ui.choose(["Consume", "Leave"])
        if selection == 1:
            x = random.randint(1, 4)
            if x == 1:
                if ctx.player.is_race("Satyr"):
                    w = ctx.player.consumption_rate + ctx.player.consumption_rate + ctx.player.consumption_rate
                    ctx.player.consumption_rate = ctx.player.consumption_rate + w
                    ui.print(f"You eat the mushroom, and gain {w} Endurance.")
                else:
                    ui.print("You eat the mushroom, and nothing happened.")

            elif x == 2:
                if ctx.player.race == "Satyr":
                    w = ctx.player.consumption_rate + ctx.player.consumption_rate + ctx.player.consumption_rate
                    ctx.player.consumption_rate = ctx.player.consumption_rate + w
                    ui.print(f"You eat the mushroom, and gain {w} Endurance.")
                else:
                    ui.print("You eat the mushroom, and it causes you to vomit.")
                    if not ctx.player.is_alive():
                        return adventuring.Death(self.ctx)

            elif x == 3:
                w = ctx.player.consumption_rate + ctx.player.consumption_rate
                ctx.player.consumption_rate = ctx.player.consumption_rate + w
                ui.print(f"You eat the mushroom, and gain {w} Endurance.")

            elif x == 4:
                if ctx.player.race == "Satyr":
                    w = ctx.player.consumption_rate + ctx.player.consumption_rate
                    ctx.player.consumption_rate = ctx.player.consumption_rate + w
                    ui.print(f"You eat the mushroom, and gain {w} Endurance.")
                else:
                    ctx.player.hp = 0
                    ctx.endurance = 0
                    ui.print("You eat the mushroom, and then fall to the ground, foaming at the mouth.")
                    ui.wait()
                    return adventuring.Death(self.ctx)

        else:
            ui.print("You leave the mushroom.")

        ui.wait()
        return adventuring.Adventuring(self.ctx)


# Miracle #
class Miracle(State):
    def do(self) -> Optional[State]:
        player = self.ctx.player

        if not player.is_race("Halfling"):
            return NoEvent(self.ctx)

        ui.print("You see an old wizard, and the wizard beckons you over.")
        ui.print('"Ho, there, traveler!"')
        ui.print(f'"I did not expect to see a {player.race} out in the wilderness."')
        ui.print('"This is delightful. Here, have a gift."')

        selection = ui.choose(["Fill Food", "Fill Arrows", "Fill Gold", "Fill HP"])
        if selection == 1:
            player.fill_food()
        if selection == 2:
            player.fill_arrows()
        if selection == 3:
            player.fill_gold()
        if selection == 4:
            player.fill_hp()

        ui.wait()
        return adventuring.Adventuring(self.ctx)


# Bigger Bag #
class BiggerBag(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        y = random.randint(1, 3)
        if y == 1:
            item_name = "food storage container"
            resource_name = "food"
            resource_amount = 10
            ctx.player.max_food += resource_amount

        elif y == 2:
            item_name = "quiver"
            resource_name = "arrows"
            resource_amount = 10
            ctx.player.max_arrows += resource_amount

        else:
            item_name = "coin purse"
            resource_name = "gold"
            resource_amount = 100
            ctx.player.max_gold += resource_amount

        ui.print(f"You find an empty {item_name} on the side of the path. It holds more {resource_name} than your current one.")
        ui.wait("take\n")
        ui.print(f"Max {resource_name} increased by {resource_amount}.")
        ui.print()

        ui.wait()
        return adventuring.Adventuring(self.ctx)


# Lose a Day #
class LoseDay(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        v = random.randint(1, 3)
        # y = random.randint(1, 2)
        # k = random.randint(1, 100)
        ctx.counter += v
        # if y == 1:

        ui.print(f"You realize that you are lost. It will take you {v} days to get back on the right path.")
        # if y == 2:
        # if ctx.location == 'Goodshire' or 'Rodez':
        # ui.print('You arrive at a bridge spanning a massive whitewater river that is guarded by a score of bandits. One bandit approaches you.')
        # elif ctx.location == 'Oristano' or 'Thasos' or 'Karabuk':
        # ui.print('You arrive at a bridge spanning an enormous chasm that is guarded by a score of bandits. One bandit approaches you.')
        # ui.print('"If you want to cross this bridge, you have to pay us, ' + str(k) 'ctx.player.gold.\n')
        #        ui.print('1 Pay ctx.player.gold\n2 Take a detour\n')
        #        selection = ui.input('>: ')
        #        if selection == 1:
        #            if k > ctx.player.gold:
        #            ui.print('"That is not enough to cross, but we will keep what you gave us, and you can find another way around. Have fun out there."')
        #            ctx.player.gold = 0
        #            else:
        #               ctx.player.gold = ctx.player.gold - k
        #               ui.print(f'You gave the bandit {k} ctx.player.gold, and they let you cross the bridge.')
        #       elif selection == 2
        #       else:
        #           selection = ui.input('>: ')

        ui.wait()

        return adventuring.Adventuring(self.ctx)


# Mystic #
class Mystic(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        ui.print("You come upon a roaming mystic.")
        ui.print("The mystic offers you a blessing.\n")

        selection = ui.choose(["Increase Max HP", "Increase Endurance", "Increase Martial Prowess"])
        if selection == 1:
            increase = 10
            resource_name = "max HP"
            ctx.player.max_hp += increase
            ctx.player.hp += increase

        elif selection == 2:
            increase = ctx.player.consumption_rate
            resource_name = "endurance"
            ctx.player.endurance += increase

        else:
            increase = 10
            resource_name = "martial prowess"
            ctx.player.martial_prowess += increase

        ui.print(f"Your {resource_name} increases by {increase}.")

        ui.wait()
        return adventuring.Adventuring(self.ctx)


# Nothing #
class NoEvent(State):
    def do(self) -> Optional[State]:
        ui.print("Nothing notable happens.")
        ui.wait()

        return adventuring.Adventuring(self.ctx)


# Damaged (Random Event) #
class Damaged(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        # adventure_menu()
        v = random.randint(1, 20)
        n = random.randint(1, 3)
        ctx.player.hp -= v

        if not ctx.player.is_alive():
            return adventuring.Death(self.ctx)

        if n == 1:
            g = random.randint(1, 20)
            ctx.player.gold += g
            ui.print(f"You sprain your ankle in a divot, taking {v} damage.")
            ui.print(f"However, you find {g} gold on the ground.")

        elif n == 2:
            f = random.randint(1, 20)
            ctx.player.food += f
            ui.print(f"You are stung by a swarm of bees, taking {v} damage.")
            ui.print(f"However, you manage to take {f} honey before you flee.")

        else:
            a = random.randint(1, 20)
            ctx.player.arrows += a
            ui.print(f"You walk into an hunter's trap, taking {v} damage.")
            ui.print(f"However, you find {a} arrows nearby.")

        ui.wait()
        return adventuring.Adventuring(self.ctx)


# Robbed #
class Robbed(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        if ctx.player.food == 0 and ctx.player.arrows == 0 and ctx.player.gold == 0:
            return NoEvent(self.ctx)

        x = random.randint(1, 3)
        if x == 1:
            v = random.randint(1, 50)
            ctx.player.food -= v

            y = random.randint(1, 2)
            if y == 1:
                ui.print(f"During the night, a shadowy figure stole {v} of your food.")
            else:
                ui.print(f"You check your food supply and find that {v} food is missing.")

        elif x == 2:
            v = random.randint(1, 50)
            ctx.player.arrows -= v

            y = random.randint(1, 2)
            if y == 1:
                ui.print(f"During the night, a shadowy figure stole {v} of your arrows.")
            elif y == 2:
                ui.print(f"You check your arrow quill, and find that {v} arrows are missing.")

        elif x == 3:
            v = random.randint(1, 50)
            ctx.player.gold -= v

            y = random.randint(1, 2)
            if y == 1:
                ui.print(f"During the night, a shadowy figure stole {v} of your gold.")
            elif y == 2:
                ui.print(f"You check your coin purse, and find that {v} gold is missing.")

        ui.wait()
        return adventuring.Adventuring(self.ctx)


# Chest #
class Chest(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        chest_name = random.choice(["treasure chest", "large hollow tree"])
        ui.print(f"You see a {chest_name}.")

        selection = ui.choose(["Inspect", "Avoid"])
        if selection == 1:
            a = random.randint(1, 3)
            if a == 1:
                ui.print("It is empty. Nothing but cobwebs remain.")
            if a == 2:
                damage = 20
                ui.print(f"It was booby trapped. A dart flies out and hits you for {damage} damage.")
                ctx.player.hp -= damage

                if not ctx.player.is_alive():
                    return adventuring.Death(self.ctx)

            # if a == 2 and ctx.luck > 0:
            # ui.print('It was booby trapped. A dart flies out and hits you for 20 damage.')
            # chest_loot()

        ui.print()

        ui.wait()
        return adventuring.Adventuring(self.ctx)


# Chest Loot #
class ChestLoot(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        x = random.randint(1, 3)
        if x == 1:
            resource_name = "food"
            amount = random.randint(50, 100)
            ctx.player.food += amount

        elif x == 2:
            resource_name = "arrows"
            amount = random.randint(50, 100)
            ctx.player.arrows += amount

        else:
            resource_name = "gold"
            amount = random.randint(50, 100)
            ctx.player.gold += amount

        ui.print(f"Inside, you found {amount} {resource_name}.")

        ui.wait()
        return adventuring.Adventuring(self.ctx)
