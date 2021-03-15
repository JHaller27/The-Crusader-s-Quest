import random
from typing import Optional

from state import State
from utils import ui


class Town(State):
    def do(self) -> Optional[State]:

        ui.clear()
        ui.print(f"You are in {self.ctx.location}.")
        ui.print(self.ctx.get_location().description)
        ui.print()

        selection = ui.choose(["Tavern", "Blacksmith", "Character", "Adventure"])
        if selection == 1:
            return Tavern(self.ctx)

        elif selection == 2:
            return Blacksmith(self.ctx)

        elif selection == 3:
            ui.clear()
            self.ctx.char_menu()
            ui.wait()

        elif selection == 4:
            return LeaveTown(self.ctx)

        return Town(self.ctx)


class LeaveTown(State):
    def do(self) -> Optional[State]:
        self.ctx.counter = 0

        location = self.ctx.get_location()
        self.ctx.counter = location.distance

        ui.print(f"You will brave the wilds for {self.ctx.counter} days.")
        selection = ui.choose(["Continue", "Go back"])

        if selection == 1:
            return TheMap(self.ctx)

        return Town(self.ctx)


# Tavern #
class Tavern(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        ui.clear()
        ui.print("######################")
        ui.print(f"Gold: {ctx.player.gold}/{ctx.player.max_gold}")
        ui.print(f"HP: {ctx.player.hp}/{ctx.player.max_hp}")
        ui.print(f"Food: {ctx.player.food}/{ctx.player.max_food}")
        ui.print("######################\n")
        ui.print(f'"Welcome to the {ctx.location} Inn. How may I serve you?"\n')

        selection = ui.choose(["Rest (1 gold)", "Buy Food (5 gold)", "Sell Food (3 gold)", "Speak with random patron", "Back"])
        if selection == 1:
            if ctx.player.gold < 1:
                ui.print("You cannot afford a bed here.")
                ui.wait("continue.")
            else:
                ui.print("You slept like a rock.")
                ctx.player.fill_hp()
                ctx.player.gold -= 1
                ui.wait("continue")

        elif selection == 2:
            ui.print("How much food do you want to buy?")
            ctx.player.food_price = 5
            n = ui.input_text()
            n = int(n)

            if n == 0:
                return Tavern(self.ctx)

            total_cost = n * ctx.player.food_price

            if total_cost > ctx.player.gold:
                ui.print(f"You do not have enough gold to buy {n} food.")
                ui.wait()

            elif total_cost <= ctx.player.gold:
                ctx.player.food = ctx.player.food + n
                ctx.player.gold = ctx.player.gold - total_cost
                ui.print("You complete the transaction")
                ui.wait()

        elif selection == 3:
            ui.print("How much food do you want to sell?")
            food_sell = 3
            n = ui.input_text()

            if n == 0:
                return Tavern(self.ctx)

            n = int(n)
            total_sell = n * food_sell

            if ctx.player.food < n:
                ui.print("You do not have that much food.")
                ui.wait()

            if ctx.player.food >= n:
                ctx.player.food = ctx.player.food - n
                ctx.player.gold = ctx.player.gold + total_sell
                ui.print("You complete the transaction")
                ui.wait()
                ui.clear()

        elif selection == 4:
            return Talk(self.ctx)

        elif selection == 5:
            return Town(self.ctx)

        return Tavern(self.ctx)


# Talk #
class Talk(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        dialogue = random.randint(1, 10)
        part = ""
        if dialogue == 1:
            ui.print("I don't take too kindly to travelers.")
        if dialogue == 2:
            ui.print("I'm too scared to leave " + ctx.location + ". I don't know how you survive out there.")
        if dialogue == 3:
            ui.print("The " + ctx.location + " Inn is the best tavern in the world. Not that I would know.")
        if dialogue == 4:
            ui.print("There's nasty things where you're headed.")
        if dialogue == 5:
            ui.print("Someone I know was killed looking inside a hollow tree. You wouldn't want that happening to you.")
        if dialogue == 6:
            ui.print("If you run out of food and arrows in the wilds, how will you survive? On pure endurance ?")
        if dialogue == 7:
            ui.print("If you want stronger equipment, I recommend going to the blacksmith.")
        if dialogue == 8:
            n = random.randint(1, 8)
            if n == 1:
                part = "arm"
            if n == 2:
                part = "leg"
            if n == 3:
                part = "hand"
            if n == 4:
                part = "foot"
            if n == 5:
                part = "eye"
            if n == 6:
                part = "ear"
            if n == 7:
                part = "finger"
            if n == 8:
                part = "toe"
            ui.print(f"In the wilds, I got caught in a hunter's trap. That's how I lost my {part}.")
        if dialogue == 9:
            ui.print("Tales of the beasts and Satanic denizens in the wilds have kept me inside the city walls.")
        if dialogue == 10:
            ui.print(f"The good thing about resting at {ctx.location} Inn is that you get a complimentary meal.")
        ui.wait()
        return Tavern(self.ctx)


# Blacksmith #
class Blacksmith(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        ui.clear()
        ui.print("######################")
        ui.print(f"Gold: {ctx.player.gold}/{ctx.player.max_gold}")
        ui.print(f"Arrows: {ctx.player.arrows}/{ctx.player.max_arrows}")
        ui.print(f"Martial Prowess: {ctx.martial_prowess}")
        ui.print("######################\n")
        ui.print('"What can I do for you, traveler?"')

        selection = ui.choose([
            f"Upgrade your {ctx.player.weapon} ({ctx.blacksmith_price} gold)",
            "Buy Arrows (5 gold)",
            "Sell Arrows (3 gold)",
            "Back",
        ])

        if selection == 4:
            return Town(self.ctx)

        if selection == 1:
            if ctx.player.gold < ctx.blacksmith_price:
                ui.print("You do not have enough gold to upgrade your " + ctx.player.weapon + ".")
                ui.wait()
            else:
                ctx.player.gold = ctx.player.gold - ctx.blacksmith_price
                v = random.randint(10, 30)
                ctx.martial_prowess = ctx.martial_prowess + v
                ui.print(f"Your martial prowess increases by {v}.")
                ui.wait()

        elif selection == 2:
            ui.print("How many arrows do you want to buy?")
            arrow_price = 5
            n = ui.input_text()
            n = int(n)
            total_cost = n * arrow_price
            if total_cost > ctx.player.gold:
                ui.print(f"You do not have enough gold to buy {n} arrows.")
                ui.wait()
            if total_cost <= ctx.player.gold:
                ctx.player.arrows = ctx.player.arrows + n
                ctx.player.gold = ctx.player.gold - total_cost
                ui.print("You complete the transaction")
                ui.wait()

        elif selection == 3:
            ui.print("How many arrows do you want to sell?")
            arrow_sell = 3
            n = ui.input_text()
            n = int(n)
            total_sell = n * arrow_sell
            if ctx.player.arrows < n:
                ui.print("You do not have that many arrows.")
                ui.wait()
            if ctx.player.arrows >= n:
                ctx.player.arrows = ctx.player.arrows - n
                ctx.player.gold = ctx.player.gold + total_sell
                ui.print("You complete the transaction")
                ui.wait()
                ui.clear()

        return Blacksmith(self.ctx)
