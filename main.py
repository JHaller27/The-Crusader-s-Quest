# Python Text RPG
# Authored by: Gaga Gievous
# Copyright February 2021

from typing import Optional
import random
import yaml

from map import get_map
from ui import ui
from state import Context, State
from enemy import Enemy, get_enemy

from scenes import Traveller

with open("./data/player_options.yml", "r") as fp:
    player_options_config = yaml.safe_load(fp)
with open("./data/enemies.yml", "r") as fp:
    enemies_config = yaml.safe_load(fp)


# Information Menus #
def char_menu(ctx: Context):
    player = ctx.player

    ui.clear()
    ui.display_basic_player_info(player)
    ui.display_combat_stats(player)
    ui.display_resources(player)


def adventure_menu(ctx: Context):
    player = ctx.player

    ui.clear()
    ui.display_combat_stats(player)
    ui.display_resources(player)


# Title Screen #
class TitleScreen(State):
    def do(self) -> Optional[State]:
        ui.clear()
        ui.print("#####################################################################################################################")
        ui.print("#####################################################################################################################")
        ui.print("##     ## ## ##   ######   ##    ### ## ####  ##    ##  ####   ##    ### ####  #####    #### ## ##   ####  ##     ###")
        ui.print("#### #### ## ## ######## #### ##  ## ## ### #### ## ## # ### #### ##  ## ### ####### ## #### ## ## ##### ###### #####")
        ui.print("#### ####    ##   ###### ####   #### ## ###  ###    ## ## ##   ##   ########  ###### ## #### ## ##   ###  ##### #####")
        ui.print("#### #### ## ## ######## #### # #### ## #### ### ## ## # ### #### # ######### ###### ## #### ## ## ###### ##### #####")
        ui.print("#### #### ## ##   ######   ## ##  ##    ##  #### ## ##  ####   ## ##  #####  #######      ##    ##   ##  ###### #####")
        ui.print("#####################################################################################################################")
        ui.print("#####################################################################################################################")
        ui.print("The Crusader's Quest: Survival Text RPG.\n")
        ui.wait("play")

        return Introduction(self.ctx)


class Introduction(State):
    def do(self) -> Optional[State]:
        ui.clear()
        ui.print("The Antipope is defiling the holiest religious site in the world. You are a warrior monk from the Freemasons, and it is up to you to destroy the Antipope.\n")
        ui.print("You begin your journey in Goodshire, one of the many towns you hope to pass through.\n")

        return SetName(self.ctx)


# Character Creation #
class SetName(State):
    def do(self) -> Optional[State]:
        ui.print("What is your name?\n")
        self.ctx.player.name = ui.input_text()

        return SetRace(self.ctx)


class SetRace(State):
    def do(self) -> Optional[State]:
        player = self.ctx.player

        ui.clear()
        ui.print("What is your race?\n")

        races = player_options_config.get("races")

        selection = ui.choose([r.get("name") for r in races]) - 1
        selected_race = races[selection]

        player.race = selected_race.get("name")
        player.max_hp = selected_race.get("hp")
        player.hp = selected_race.get("hp")
        player.martial_prowess = selected_race.get("martial_prowess")
        player.consumption_rate = selected_race.get("consumption_rate")
        player.endurance = selected_race.get("endurance")
        player.max_gold = selected_race.get("gold")
        player.gold = selected_race.get("gold")
        player.luck = selected_race.get("luck")
        player.speed = selected_race.get("speed")

        return SetOccupation(self.ctx)


class SetOccupation(State):
    def do(self) -> Optional[State]:
        player = self.ctx.player

        ui.clear()
        ui.print("What is your occupation?\n")

        occupations = player_options_config.get("occupations")

        selection = ui.choose([o.get("name") for o in occupations]) - 1
        selected_occupation = occupations[selection]

        player.occupation = selected_occupation.get("name")
        player.max_hp += selected_occupation.get("hp")
        player.hp += selected_occupation.get("hp")
        player.max_food += selected_occupation.get("food").get("max")
        player.food += selected_occupation.get("food").get("curr")
        player.max_arrows += selected_occupation.get("arrows").get("max")
        player.arrows += selected_occupation.get("arrows").get("curr")
        player.max_gold += selected_occupation.get("gold").get("max")
        player.gold += selected_occupation.get("gold").get("curr")
        player.martial_prowess += selected_occupation.get("martial_prowess")

        return SetWeapon(self.ctx)


class SetWeapon(State):
    def do(self) -> Optional[State]:
        player = self.ctx.player

        ui.clear()
        ui.print("What kind of weapon do you want to use? (ie. sword, poleaxe, etc.)")

        player.weapon = ui.input_text()

        return BeginAdventure(self.ctx)


class BeginAdventure(State):
    def do(self) -> Optional[State]:
        ui.clear()
        ui.print(self.ctx.player.description)

        selection = ui.choose(["Begin Adventure", "Restart"])
        if selection == 1:
            return StartGame(self.ctx)

        return TitleScreen(self.ctx)


# Death #
class Death(State):
    def do(self) -> Optional[State]:
        ui.clear()
        ui.print("You have died.\n")
        ui.wait()

        char_menu(self.ctx)
        ui.print()
        ui.wait("return to menu")

        return TitleScreen(self.ctx)


# Map #
class TheMap(State):
    def do(self) -> Optional[State]:
        self.ctx.display_map()

        ui.print(f"You have {self.ctx.counter} days to go.")
        ui.wait()

        return Adventuring(self.ctx)

# Treasure Generator #
# def treasure_generator():
# v = random.randint(0, 3)
# ui.print(f'You found {v} treasures on this leg of the journey.')


# Location Changer #
class LocationChanger(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        ctx.map.move()

        if ctx.map.at_end_location():
            return FinalBattle(self.ctx)

        return Town(self.ctx)


# Start Game #
class StartGame(State):
    def do(self) -> Optional[State]:
        return Town(self.ctx)


# Town #
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
            char_menu(self.ctx)
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


# Adventuring #
class Adventuring(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        if not ctx.player.is_alive():
            return Death(self.ctx)

        if ctx.counter == 0:
            return EndAdventure(self.ctx)

        adventure_menu(self.ctx)
        selection = ui.choose(["Continue", "Hunt", "Rest", "Map"])

        if selection == 1:
            ctx.counter -= 1

            return RandomEvent(self.ctx)

        elif selection == 2:
            return Hunt(self.ctx)

        elif selection == 3:
            return Rest(self.ctx)

        elif selection == 4:
            return TheMap(self.ctx)


class EndAdventure(State):
    def do(self) -> Optional[State]:
        ui.clear()
        adventure_menu(self.ctx)

        ui.print("You have survived the trip.")
        ui.wait()

        return LocationChanger(self.ctx)


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
            adventure_menu(self.ctx)

            ui.print(f"You shot {arrows_shot} arrows, and gained {food_found} food.")

        ui.wait()

        return Adventuring(self.ctx)


#
# Random Events #
#
class RandomEvent(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        ui.clear()
        adventure_menu(ctx)

        n = random.randint(1, 20)
        if n == 1:
            return Chest(ctx)
        if n == 2:
            return Fight(ctx)
        if n == 3:
            return Robbed(ctx)
        if n == 4:
            return Traveller(ctx)
        if n == 5:
            return Damaged(ctx)
        if n == 6:
            return Miracle(ctx)
        if n == 7:
            return Mushroom(ctx)
        if n == 8:
            return NoEvent(ctx)
        if n == 9:
            return Fight(ctx)
        if n == 10:
            return Fight(ctx)
        if n == 11:
            return Chest(ctx)
        if n == 12:
            return Fight(ctx)
        if n == 13:
            return Robbed(ctx)
        if n == 14:
            return Traveller(ctx)
        if n == 15:
            return Damaged(ctx)
        if n == 16:
            return Mystic(ctx)
        if n == 17:
            return BiggerBag(ctx)
        if n == 18:
            return LoseDay(ctx)
        if n == 19:
            return Fight(ctx)
        if n == 20:
            return Fight(ctx)


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
                        return Death(self.ctx)

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
                    return Death(self.ctx)

        else:
            ui.print("You leave the mushroom.")

        ui.wait()
        return Adventuring(self.ctx)


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
        return Adventuring(self.ctx)


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
        return Adventuring(self.ctx)


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

        return Adventuring(self.ctx)


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
        return Adventuring(self.ctx)


# Nothing #
class NoEvent(State):
    def do(self) -> Optional[State]:
        ui.print("Nothing notable happens.")
        ui.wait()

        return Adventuring(self.ctx)


# Damaged (Random Event) #
class Damaged(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        # adventure_menu()
        v = random.randint(1, 20)
        n = random.randint(1, 3)
        ctx.player.hp -= v

        if not ctx.player.is_alive():
            return Death(self.ctx)

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
        return Adventuring(self.ctx)


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
        return Adventuring(self.ctx)


# Fight #
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
                ui.wait()
                adventure_menu(self.ctx)
            if a == 2:
                damage = 20
                ui.print(f"It was booby trapped. A dart flies out and hits you for {damage} damage.")
                ctx.player.hp -= damage
                ui.wait()

                if not ctx.player.is_alive():
                    return Death(self.ctx)

                adventure_menu(self.ctx)
            # if a == 2 and ctx.luck > 0:
            # ui.print('It was booby trapped. A dart flies out and hits you for 20 damage.')
            # chest_loot()

        ui.print()

        return Adventuring(self.ctx)


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
        return adventure_menu(self.ctx)


# Final Battle #
class FinalBattle(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        ctx.display_map()
        ui.print("Salem\n")
        ui.wait()
        ui.clear()

        ui.print("You enter the ancient city of Salem, now blackened with fire and as silent as a graveyard, and see a man who looks like a commoner lounging upon a throne of skeletons in the courtyard.")
        ui.print('"Ah, ' + ctx.player.name + '", I was expecting you."\n')
        ui.print("Type 'who are you?'")
        ui.input_text()

        ui.clear()
        ui.print('"I am the called by your order the Antipope or the Prince of Darkness, but my birth name is Chernobog."')
        ui.print('"As you can see, I have already razed Salem. Your sacred temples and artifacts are totally destroyed. You have failed."')
        ui.print('"But I admire your willpower and resourcefulness to make it all the way here from Goodshire."')
        ui.print('"I want to make you an offer. Join me, and become my champion. Together, we will forge a New Dawn."')
        ui.print('"Your old ways are gone. You have failed your order, and they will no longer accept you."')
        ui.print('"If you decline, I won\'t kill you, but I will beat you within an inch of your life and enslave you for eternity."\n')
        ui.print('"The choice is yours, ' + ctx.player.name + '."\n')
        selection = ui.choose(["Accept offer", "Decline offer"])
        ui.clear()

        if selection == 1:
            char_menu(ctx)
            ui.print("You join the forces of Chernobog, the Prince of Darkness, and forsake your old way of life. You both combine your powers and forge a New Dawn.")
            ui.print()
            ui.wait("end game")

        else:
            ui.print('"Very well, then." Chernobog stands up.')
            ui.wait("fight")

            ctx.enemy = Enemy("", "Chernobog", 170)
            damage_taken = ctx.combat_damage()
            ctx.player.hp -= damage_taken

            if ctx.player.is_alive():
                ui.print("You have slain the Antipope. His body magically lights on fire, and leaves ashes on the ground.")
                ui.print("Your surroundings shimmer, and the city of Salem transforms from its ruined state to its former glory. You have succeeded in every goal.")
                ui.wait()

                char_menu(ctx)
                ui.clear()
                ui.print("You win!")

                ui.print(f"Occupation: {ctx.player.occupation}")

            else:
                char_menu(ctx)
                ui.print()
                ui.print("You have lost the fight, letting Chernobog win. He enslaves you for all eternity, and he takes over the world.\n")

            ui.wait("end game")

        return TitleScreen(self.ctx)


def main():
    map_data = get_map("./data/map.yml")

    global_context = Context(map_data)
    global_context.run(TitleScreen(global_context))


if __name__ == "__main__":
    main()
