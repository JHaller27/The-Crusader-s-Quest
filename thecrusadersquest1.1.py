# Python Text RPG
# Authored by: Gaga Gievous
# Copyright February 2021

from typing import Optional
import random
import yaml

from map import get_map
from ui import ui
from state import Context, State, TransientState
from enemy import Enemy, get_enemy

with open('./data/player_options.yml', 'r') as fp:
    player_options_config = yaml.safe_load(fp)
with open('./data/enemies.yml', 'r') as fp:
    enemies_config = yaml.safe_load(fp)


# Title Screen #
class TitleScreen(State):
    def do(self) -> Optional[State]:
        ui.clear()
        ui.print(
            "#####################################################################################################################")
        ui.print(
            "#####################################################################################################################")
        ui.print(
            "##     ## ## ##   ######   ##    ### ## ####  ##    ##  ####   ##    ### ####  #####    #### ## ##   ####  ##     ###")
        ui.print(
            "#### #### ## ## ######## #### ##  ## ## ### #### ## ## # ### #### ##  ## ### ####### ## #### ## ## ##### ###### #####")
        ui.print(
            "#### ####    ##   ###### ####   #### ## ###  ###    ## ## ##   ##   ########  ###### ## #### ## ##   ###  ##### #####")
        ui.print(
            "#### #### ## ## ######## #### # #### ## #### ### ## ## # ### #### # ######### ###### ## #### ## ## ###### ##### #####")
        ui.print(
            "#### #### ## ##   ######   ## ##  ##    ##  #### ## ##  ####   ## ##  #####  #######      ##    ##   ##  ###### #####")
        ui.print(
            "#####################################################################################################################")
        ui.print(
            "#####################################################################################################################")
        ui.print("The Crusader's Quest: Survival Text RPG.\n")
        ui.wait("play")

        return SetupGame(self.ctx)


# Character Creation #

# Name #
class SetupGame(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        ctx.heal_item = 0
        ctx.adventure_state = False

        ui.clear()
        ui.print(
            'The Antipope is defiling the holiest religious site in the world. You are a warrior monk from the Freemasons, and it is up to you to destroy the Antipope.\n')
        ui.print('You begin your journey in Goodshire, one of the many towns you hope to pass through.\n')
        ui.print('What is your name?\n')

        ctx.player.name = ui.input_text()

        # Race #
        ui.clear()
        ui.print('What is your race?\n')

        races = player_options_config.get('races')

        selection = ui.choose([r['name'] for r in races]) - 1
        selected_race = races[selection]

        ctx.player.race = selected_race.get('name')
        ctx.player.max_hp = selected_race.get('hp')
        ctx.player.hp = selected_race.get('hp')
        ctx.player.martial_prowess = selected_race.get('martial_prowess')
        ctx.player.consumption_rate = selected_race.get('consumption_rate')
        ctx.player.endurance = selected_race.get('endurance')
        ctx.player.max_gold = selected_race.get('gold')
        ctx.player.gold = selected_race.get('gold')
        ctx.player.luck = selected_race.get('luck')
        ctx.player.speed = selected_race.get('speed')

        ui.clear()

        # Occupation #
        ui.print('What is your occupation?\n')

        occupations = player_options_config.get('occupations')

        selection = ui.choose([o['name'] for o in occupations]) - 1
        selected_occupation = occupations[selection]

        ctx.player.occupation = selected_occupation.get('name')
        ctx.player.max_hp += selected_occupation.get('hp')
        ctx.player.hp += selected_occupation.get('hp')
        ctx.player.max_food += selected_occupation.get('food').get('max')
        ctx.player.food += selected_occupation.get('food').get('curr')
        ctx.player.max_arrows += selected_occupation.get('arrows').get('max')
        ctx.player.arrows += selected_occupation.get('arrows').get('curr')
        ctx.player.max_gold += selected_occupation.get('gold').get('max')
        ctx.player.gold += selected_occupation.get('gold').get('curr')
        ctx.player.martial_prowess += selected_occupation.get('martial_prowess')

        ui.clear()
        ui.print('What kind of weapon do you want to use? (ie. sword, poleaxe, etc.)')

        ctx.player.weapon = ui.input_text()

        ui.clear()
        ui.print(ctx.player.description)

        selection = ui.choose(["Begin Adventure", "Restart"])
        if selection == 1:
            return StartGame(self.ctx)
        else:
            return TitleScreen(self.ctx)


# Death #
class Death(State):
    def do(self) -> Optional[State]:
        ui.clear()
        ui.print('You have died.\n')
        ui.wait()
        char_menu(self.ctx)
        ui.print()
        ui.wait("return to menu")

        return TitleScreen(self.ctx)


# Character Menu #
def char_menu(ctx: Context):
    ui.clear()
    ctx.char_menu()


# Adventure Menu #
def adventure_menu(ctx: Context):
    ui.clear()
    ctx.adventure_menu()


# Map #
class TheMap(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        # ui.print('Key: T = Town; C = City; etc.)
        ctx.display_map()

        return DaysToGo(self.ctx, self.default)


# Days to Go #
class DaysToGo(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        if ctx.adventure_state:
            ui.print(f'You have {ctx.counter} days to go.')
            ui.wait()

            return None

        location = ctx.get_location()
        distance = location.distance
        ctx.counter_set = ctx.counter = distance

        ui.print(f"You will brave the wilds for {distance} days.")
        selection = ui.choose(['Continue', 'Go back'])

        if selection == 1:
            ui.wait()
            return Adventuring(self.ctx)

        return Town(self.ctx)


# Treasure Generator #
# def treasure_generator():
# v = random.randint(0, 3)
# ui.print(f'You found {v} treasures on this leg of the journey.')


# Location Changer #
class LocationChanger(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        ctx.adventure_state = False

        location = ctx.get_location()
        ctx.set_location(location.destination)

        if ctx.at_end_location():
            return Salem(self.ctx)

        return Town(self.ctx)


# Start Game #
class StartGame(State):
    def do(self) -> Optional[State]:
        return Town(self.ctx)


# Town #
class Town(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        ui.clear()
        ui.print('You are in ' + ctx.location + '.')
        ui.print(ctx.get_location().description)
        ui.print()
        selection = ui.choose(["Tavern", "Blacksmith", "Character", "Adventure"])
        if selection == 1:
            ui.clear()
            return Tavern(self.ctx)

        if selection == 4:
            ui.clear()
            ctx.counter = 0
            return TheMap(ctx, LeaveTown)

        if selection == 2:
            ui.clear()
            return Blacksmith(self.ctx)
        if selection == 3:
            ui.clear()
            char_menu(self.ctx)
            ui.wait()
        return Town(self.ctx)


class LeaveTown(State):
    def do(self) -> Optional[State]:
        ui.print('You will brave the wilds for 5 days.')
        ui.wait()
        return Adventuring(self.ctx)


# Tavern #
class Tavern(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        ui.clear()
        ui.print('######################')
        ui.print(f'Gold: {ctx.player.gold}/{ctx.player.max_gold}')
        ui.print(f'HP: {ctx.player.hp}/{ctx.player.max_hp}')
        ui.print(f'Food: {ctx.player.food}/{ctx.player.max_food}')
        ui.print('######################\n')
        ui.print('"Welcome to the ' + ctx.location + ' Inn. How may I serve you?"\n')

        selection = ui.choose(
            ['Rest (1 gold)', 'Buy Food (5 gold)', 'Sell Food (3 gold)', 'Speak with random patron', 'Back'])
        if selection == 1:
            if ctx.player.gold < 1:
                ui.print('You cannot afford a bed here.')
                ui.wait('continue.')
            else:
                ui.print('You slept like a rock.')
                ctx.player.fill_hp()
                ctx.player.gold -= 1
                ui.wait('continue')

        elif selection == 2:
            ui.print('How much food do you want to buy?')
            ctx.player.food_price = 5
            n = ui.input_text()
            n = int(n)

            if n == 0:
                return Tavern(self.ctx)

            total_cost = n * ctx.player.food_price

            if total_cost > ctx.player.gold:
                ui.print(f'You do not have enough gold to buy {n} food.')
                ui.wait()

            elif total_cost <= ctx.player.gold:
                ctx.player.food = ctx.player.food + n
                ctx.player.gold = ctx.player.gold - total_cost
                ui.print('You complete the transaction')
                ui.wait()

        elif selection == 3:
            ui.print('How much food do you want to sell?')
            food_sell = 3
            n = ui.input_text()

            if n == 0:
                return Tavern(self.ctx)

            n = int(n)
            total_sell = n * food_sell

            if ctx.player.food < n:
                ui.print('You do not have that much food.')
                ui.wait()

            if ctx.player.food >= n:
                ctx.player.food = ctx.player.food - n
                ctx.player.gold = ctx.player.gold + total_sell
                ui.print('You complete the transaction')
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
        part = ''
        if dialogue == 1:
            ui.print('I don\'t take too kindly to travelers.')
        if dialogue == 2:
            ui.print('I\'m too scared to leave ' + ctx.location + '. I don\'t know how you survive out there.')
        if dialogue == 3:
            ui.print('The ' + ctx.location + ' Inn is the best tavern in the world. Not that I would know.')
        if dialogue == 4:
            ui.print('There\'s nasty things where you\'re headed.')
        if dialogue == 5:
            ui.print("Someone I know was killed looking inside a hollow tree. You wouldn't want that happening to you.")
        if dialogue == 6:
            ui.print('If you run out of food and arrows in the wilds, how will you survive? On pure endurance ?')
        if dialogue == 7:
            ui.print('If you want stronger equipment, I recommend going to the blacksmith.')
        if dialogue == 8:
            n = random.randint(1, 8)
            if n == 1:
                part = 'arm'
            if n == 2:
                part = 'leg'
            if n == 3:
                part = 'hand'
            if n == 4:
                part = 'foot'
            if n == 5:
                part = 'eye'
            if n == 6:
                part = 'ear'
            if n == 7:
                part = 'finger'
            if n == 8:
                part = 'toe'
            ui.print('In the wilds, I got caught in a hunter\'s trap. That\'s how I lost my ' + part + '.')
        if dialogue == 9:
            ui.print('Tales of the beasts and Satanic denizens in the wilds have kept me inside the city walls.')
        if dialogue == 10:
            ui.print('The good thing about resting at ' + ctx.location + ' Inn is that you get a complimentary meal.')
        ui.wait()
        return Tavern(self.ctx)


# Blacksmith #
class Blacksmith(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        ui.clear()
        ui.print('######################')
        ui.print(f'Gold: {ctx.player.gold}/{ctx.player.max_gold}')
        ui.print(f'Arrows: {ctx.player.arrows}/{ctx.player.max_arrows}')
        ui.print(f'Martial Prowess: {ctx.martial_prowess}')
        ui.print('######################\n')
        ui.print('"What can I do for you, traveler?"')

        selection = ui.choose([
            f"Upgrade your {ctx.player.weapon} ({ctx.blacksmith_price} gold)",
            "Buy Arrows (5 gold)",
            "Sell Arrows (3 gold)",
            "Back",
        ])
        if selection == 1:
            if ctx.player.gold < ctx.blacksmith_price:
                ui.print('You do not have enough gold to upgrade your ' + ctx.player.weapon + '.')
                ui.wait()
            else:
                ctx.player.gold = ctx.player.gold - ctx.blacksmith_price
                v = random.randint(10, 30)
                ctx.martial_prowess = ctx.martial_prowess + v
                ui.print(f'Your martial prowess increases by {v}.')
                ui.wait()
            return Blacksmith(self.ctx)
        if selection == 2:
            ui.print('How many arrows do you want to buy?')
            arrow_price = 5
            n = ui.input_text()
            n = int(n)
            total_cost = n * arrow_price
            if total_cost > ctx.player.gold:
                ui.print(f'You do not have enough gold to buy {n} arrows.')
                ui.wait()
                return Blacksmith(self.ctx)
            if total_cost <= ctx.player.gold:
                ctx.player.arrows = ctx.player.arrows + n
                ctx.player.gold = ctx.player.gold - total_cost
                ui.print('You complete the transaction')
                ui.wait()
                return Blacksmith(self.ctx)
        if selection == 3:
            ui.print('How many arrows do you want to sell?')
            arrow_sell = 3
            n = ui.input_text()
            n = int(n)
            total_sell = n * arrow_sell
            if ctx.player.arrows < n:
                ui.print('You do not have that many arrows.')
                ui.wait()
                return Blacksmith(self.ctx)
            if ctx.player.arrows >= n:
                ctx.player.arrows = ctx.player.arrows - n
                ctx.player.gold = ctx.player.gold + total_sell
                ui.print('You complete the transaction')
                ui.wait()
                ui.clear()
                return Blacksmith(self.ctx)

        if selection == 4:
            return Town(self.ctx)
        else:
            return Blacksmith(self.ctx)


# Adventuring #
class Adventuring(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        if ctx.counter == 0:
            return EndAdventure(self.ctx)

        ctx.adventure_state = True
        if ctx.player.hp > 0:
            adventure_menu(self.ctx)
            selection = ui.choose(["Continue", "Hunt", "Rest", "Map"])
            ui.clear()
            if selection == 1:
                ctx.counter -= 1

                if not ctx.player.is_alive():
                    return Death(self.ctx)

                adventure_menu(ctx)

                return RandomEvent(ctx, Adventuring)
            if selection == 2:
                return Hunt(self.ctx, Adventuring)
            if selection == 3:
                return Rest(self.ctx, Adventuring)
            if selection == 4:
                return TheMap(self.ctx, Adventuring)
            else:
                return Adventuring(self.ctx)
        else:
            return Death(self.ctx)


class EndAdventure(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        ctx.counter = 0
        ui.clear()
        adventure_menu(self.ctx)
        ui.print('You have survived the trip.')
        ctx.adventure_state = False
        ui.wait()

        return LocationChanger(self.ctx)


# Rest #
class Rest(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        if not ctx.player.is_alive():
            return Death(self.ctx)

        if ctx.player.hp == ctx.player.max_hp:
            ui.print('You rest for one day. Your HP is already maxed out.')
            ui.wait()

            return Adventuring(self.ctx)

        x = random.randint(15, 25)

        ctx.player.hp += x
        ui.print(f'You rest for one day, gaining {x} HP.')

        ui.wait()


# Hunt #
class Hunt(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        x = random.randint(1, 10)
        y = random.randint(1, 25)

        if ctx.player.arrows == 0:
            ui.print('You do not have any arrows to hunt with.')
            ui.wait()
            return Adventuring(self.ctx)

        elif ctx.player.arrows < x:
            adventure_menu(self.ctx)
            x = ctx.player.arrows
            ctx.player.arrows = ctx.player.arrows - x
            ctx.player.food = ctx.player.food + y
            ui.print(f'You shot {x} arrows, and gained {y} food.')

        else:
            adventure_menu(self.ctx)
            ctx.player.arrows = ctx.player.arrows - x
            ctx.player.food = ctx.player.food + y
            ui.print(f'You shot {x} arrows, and gained {y} food.')

        ui.wait()

        return None


#
# Random Events #
#
class RandomEvent(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        n = random.randint(1, 20)
        if n == 1:
            return Chest(ctx, self.default)
        if n == 2:
            return Fight(ctx, self.default)
        if n == 3:
            return Robbed(ctx, self.default)
        if n == 4:
            return Traveller(ctx, self.default)
        if n == 5:
            return Damaged(ctx, self.default)
        if n == 6:
            return Miracle(ctx, self.default)
        if n == 7:
            return Mushroom(ctx, self.default)
        if n == 8:
            return Nothing(ctx, self.default)
        if n == 9:
            return Fight(ctx, self.default)
        if n == 10:
            return Fight(ctx, self.default)
        if n == 11:
            return Chest(ctx, self.default)
        if n == 12:
            return Fight(ctx, self.default)
        if n == 13:
            return Robbed(ctx, self.default)
        if n == 14:
            return Traveller(ctx, self.default)
        if n == 15:
            return Damaged(ctx, self.default)
        if n == 16:
            return Mystic(ctx, self.default)
        if n == 17:
            return BiggerBag(ctx, self.default)
        if n == 18:
            return LoseDay(ctx, self.default)
        if n == 19:
            return Fight(ctx, self.default)
        if n == 20:
            return Fight(ctx, self.default)


# Mushroom #
class Mushroom(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        ui.print('You see a strange mushroom.')
        selection = ui.choose(["Consume", "Leave"])
        if selection == 1:
            x = random.randint(1, 4)
            if x == 1:
                if ctx.player.race == 'Satyr':
                    w = ctx.player.consumption_rate + ctx.player.consumption_rate + ctx.player.consumption_rate
                    ctx.player.consumption_rate = ctx.player.consumption_rate + w
                    ui.print(f'You eat the mushroom, and gain {w} Endurance.')
                else:
                    ui.print('You eat the mushroom, and nothing happened.')
            if x == 2:
                if ctx.player.race == 'Satyr':
                    w = ctx.player.consumption_rate + ctx.player.consumption_rate + ctx.player.consumption_rate
                    ctx.player.consumption_rate = ctx.player.consumption_rate + w
                    ui.print(f'You eat the mushroom, and gain {w} Endurance.')
                else:
                    ui.print('You eat the mushroom, and it causes you to vomit.')
                    if not ctx.player.is_alive():
                        return Death(self.ctx)

            if x == 3:
                w = ctx.player.consumption_rate + ctx.player.consumption_rate
                ctx.player.consumption_rate = ctx.player.consumption_rate + w
                ui.print(f'You eat the mushroom, and gain {w} Endurance.')
            if x == 4:
                if ctx.player.race == 'Satyr':
                    w = ctx.player.consumption_rate + ctx.player.consumption_rate
                    ctx.player.consumption_rate = ctx.player.consumption_rate + w
                    ui.print(f'You eat the mushroom, and gain {w} Endurance.')
                else:
                    ctx.player.hp = 0
                    ctx.endurance = 0
                    ui.print('You eat the mushroom, and then fall to the ground, foaming at the mouth.')
                    ui.wait()
                    return Death(self.ctx)

        elif selection == 2:
            ui.print('You leave the mushroom.')
        else:
            return Mushroom(self.ctx, self.default)
        ui.wait()


# Miracle #
class Miracle(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        if ctx.player.race == 'Halfling':
            ui.print('You see an old wizard, and the wizard beckons you over.')
            ui.print('"Ho, there, traveler!"')
            ui.print('"I did not expect to see a Halfing out in the wilderness."')
            ui.print('"This is delightful. Here, have a gift."')

            selection = ui.choose(["Fill Food", "Fill Arrows", "Fill Gold", "Fill HP"])
            if selection == 1:
                ctx.player.food = ctx.player.max_food
            if selection == 2:
                ctx.player.arrows = ctx.player.max_arrows
            if selection == 3:
                ctx.player.gold = ctx.player.max_gold
            if selection == 4:
                ctx.player.fill_hp()
            ui.wait()
        else:
            return Nothing(self.ctx, self.default)


# Bigger Bag #
class BiggerBag(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        y = random.randint(1, 3)
        if y == 1:
            ctx.player.max_food = ctx.player.max_food + 10
            ui.print(
                'You find an empty food storage container on the side of the path, and it holds more food than your current one.')
            ui.wait('take\n')
            ui.print('Max food increased by 10.')
        if y == 2:
            ctx.player.max_arrows = ctx.player.max_arrows + 10
            ui.print('You spot an empty quiver on the side of the path. It holds more arrows than your current one.')
            ui.wait('take\n')
            ui.print('Max arrows increased by 10.')
        if y == 3:
            ctx.player.max_gold = ctx.player.max_gold + 100
            ui.print(
                'You discover an empty coin purse on the side of the path. It holds more gold than your current one.')
            ui.wait('take\n')
            ui.print('Max gold increased by 100.')
        ui.print()
        ui.wait()

        return None


# Lose a Day #
class LoseDay(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        v = random.randint(1, 3)
        # y = random.randint(1, 2)
        # k = random.randint(1, 100)
        ctx.counter = ctx.counter + v
        # if y == 1:

        ui.print(f'You realize that you are lost. It will take you {v} days to get back on the right path.')
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

        return None


# Mystic #
class Mystic(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        ui.print('You come upon a roaming mystic.')
        ui.print('The mystic offers you a blessing.\n')

        selection = ui.choose(["Increase Max HP", "Increase Endurance", "Increase Martial Prowess"])
        if selection == 1:
            ctx.player.max_hp = ctx.player.max_hp + 10
            ctx.player.hp = ctx.player.hp + 10
            ui.print('Your max HP increases by 10.')
            ui.wait()
        elif selection == 2:
            ctx.endurance = ctx.endurance + ctx.player.consumption_rate
            ui.print(f'Your endurance increases by {ctx.player.consumption_rate}.')
            ui.wait()
        elif selection == 3:
            ctx.martial_prowess = ctx.martial_prowess + 10
            ui.print('Your martial prowess increases by 10.')
            ui.wait()
        else:
            return Mystic(self.ctx, self.default)


# Nothing #
class Nothing(TransientState):
    def _do(self) -> Optional[State]:
        ui.print('Nothing notable happens.')
        ui.wait()

        return None


# Damaged (Random Event) #
class Damaged(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        # adventure_menu()
        v = random.randint(1, 20)
        n = random.randint(1, 3)
        ctx.player.hp -= v

        if not ctx.player.is_alive():
            return Death(self.ctx)

        if n == 1:
            g = random.randint(1, 20)
            ctx.player.gold = ctx.player.gold + g
            ui.print(f'You sprain your ankle in a divot, taking {v} damage.')
            ui.print(f'However, you find {g} gold on the ground.')
        if n == 2:
            f = random.randint(1, 20)
            ctx.player.food = ctx.player.food + f
            ui.print(f'You are stung by a swarm of bees, taking {v} damage.')
            ui.print(f'However, you manage to take {f} honey before you flee.')

        if n == 3:
            a = random.randint(1, 20)
            ctx.player.arrows = ctx.player.arrows + a
            ui.print(f"You walk into an hunter's trap, taking {v} damage.")
            ui.print(f"However, you find {a} arrows nearby.")

        ui.wait()

        return None


# Traveller #
class Traveller(TransientState):
    def _do(self) -> Optional[State]:
        time_of_day = random.choice(['morning', 'evening', 'afternoon'])

        ui.print('A friendly adventurer approaches you and wants to trade.')
        ui.print(f'"Good {time_of_day}, traveler."\n')

        traveller_values(self.ctx)

        return None


# Traveller Values #
def traveller_values(ctx: Context):
    traveller_generation(ctx)
    ui.wait()


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


# Robbed #
class Robbed(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        x = random.randint(1, 3)
        if ctx.player.food == 0 and ctx.player.arrows == 0 and ctx.player.gold == 0:
            return Nothing(self.ctx, self.default)
        elif x == 1:
            v = random.randint(1, 50)
            if ctx.player.food < v:
                v = ctx.player.food

            ctx.player.food = ctx.player.food - v
            y = random.randint(1, 2)
            # adventure_menu()
            if y == 1:
                ui.print(f'During the night, a shadowy figure stole {v} of your food.')
            elif y == 2:
                ui.print(f'You check your food supply and find that {v} food is missing.')
        elif x == 2:
            v = random.randint(1, 50)
            if ctx.player.arrows < v:
                v = ctx.player.arrows
            ctx.player.arrows = ctx.player.arrows - v
            y = random.randint(1, 2)
            # adventure_menu()
            if y == 1:
                ui.print(f'During the night, a shadowy figure stole {v} of your arrows.')
            elif y == 2:
                ui.print(f'You check your arrow quill, and find that {v} arrows are missing.')

        elif x == 3:
            v = random.randint(1, 50)
            if ctx.player.gold < v:
                v = ctx.player.gold
            ctx.player.gold = ctx.player.gold - v
            y = random.randint(1, 2)
            # adventure_menu()
            if y == 1:
                ui.print(f'During the night, a shadowy figure stole {v} of your gold.')
            elif y == 2:
                ui.print(f'You check your coin purse, and find that {v} gold is missing.')


# Fight #
class Fight(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        ctx.enemy = get_enemy(enemy_locator_generator(ctx))
        ui.print(f"You see a {ctx.enemy.name} approaching.")

        if ctx.enemy.is_type("Doppelganger"):
            ui.print(f"The doppelganger is wielding a {ctx.player.weapon} exactly like yours.")

        selection = ui.choose(["Fight", "Flee"])
        if selection == 1:
            return FightSimulation(ctx, self.default)

        return FleeFight(ctx, self.default)


# Fight Simulation #
class FightSimulation(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        your_damage_taken(ctx)
        enemy_loot(ctx)

        ui.wait()

        ctx.enemy = None

        return Adventuring(self.ctx)


# Enemy Loot #
def enemy_loot(ctx: Context):
    ctx.player.food += ctx.enemy.food
    ctx.player.arrows += ctx.enemy.arrows
    ctx.player.gold += ctx.enemy.gold

    ui.print(f"You found {ctx.enemy.food} food, "
             f"{ctx.enemy.arrows} arrows, and"
             f"{ctx.enemy.gold} gold on the corpse.")


# Your Damage Taken #
def your_damage_taken(ctx: Context):
    damage_taken = ctx.combat_damage()

    ctx.player.hp -= damage_taken

    if damage_taken < 1:
        ui.print("The enemy was slain, and you took no damage.")
    else:
        ui.print(f"The enemy was slain, but you took {damage_taken} damage.")


# Flee Fight #
class FleeFight(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        n = random.randint(1, 2)
        if n == 2:
            ui.print('You failed to flee the fight.')
            ui.wait()

            return FightSimulation(self.ctx, self.default)

        ui.print('You escaped the fight.')
        ui.wait()
        adventure_menu(ctx)

        return Adventuring(self.ctx)


# Enemy Locator and Excluder Generator #
def enemy_locator_generator(ctx: Context) -> int:
    location = ctx.get_location()

    enemy_number = random.randint(1, 5)
    while enemy_number in location.enemy_exclude:
        enemy_number = random.randint(1, 5)

    return enemy_number


# Chest #
class Chest(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        p = random.randint(1, 2)
        if p == 1:
            ui.print('You see a treasure chest.')
        if p == 2:
            ui.print('You see a large hollow tree.')
        selection = ui.choose(["Inspect", "Avoid"])
        if selection == 1:
            a = random.randint(1, 3)
            if a == 1:
                ui.print('It is empty. Nothing but cobwebs remain.')
                ui.wait()
                adventure_menu(self.ctx)
            if a == 2:
                ui.print('It was booby trapped. A dart flies out and hits you for 20 damage.')
                ctx.player.hp -= 20
                ui.wait()

                if not ctx.player.is_alive():
                    return Death(self.ctx)

                adventure_menu(self.ctx)
            # if a == 2 and ctx.luck > 0:
            # ui.print('It was booby trapped. A dart flies out and hits you for 20 damage.')
            # chest_loot()
            if a == 3:
                return ChestLoot(self.ctx)

        elif selection == 2:
            ui.print()

        else:
            return Chest(self.ctx, self.default)


# Chest Loot #
class ChestLoot(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        x = random.randint(1, 3)
        if x == 1:
            v = random.randint(50, 100)
            ctx.player.food = ctx.player.food + v
            ui.print(f'Inside, you found {v} food.')
        if x == 2:
            v = random.randint(50, 100)
            ctx.player.arrows = ctx.player.arrows + v
            ui.print(f'Inside, you found {v} arrows.')
        if x == 3:
            v = random.randint(50, 100)
            ctx.player.gold = ctx.player.gold + v
            ui.print(f'Inside, you found {v} gold.')

        ui.wait()
        return adventure_menu(self.ctx)


# Salem #
class Salem(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        ctx.display_map()
        ui.print('Salem\n')
        ui.wait()
        ui.clear()

        ui.print(
            'You enter the ancient city of Salem, now blackened with fire and as silent as a graveyard, and see a man who looks like a commoner lounging upon a throne of skeletons in the courtyard.')
        ui.print('"Ah, ' + ctx.player.name + '", I was expecting you."\n')
        ui.print('Type \'who are you?\'')
        ui.input_text()

        ui.clear()
        ui.print(
            '"I am the called by your order the Antipope or the Prince of Darkness, but my birth name is Chernobog."')
        ui.print(
            '"As you can see, I have already razed Salem. Your sacred temples and artifacts are totally destroyed. You have failed."')
        ui.print('"But I admire your willpower and resourcefulness to make it all the way here from Goodshire."')
        ui.print('"I want to make you an offer. Join me, and become my champion. Together, we will forge a New Dawn."')
        ui.print('"Your old ways are gone. You have failed your order, and they will no longer accept you."')
        ui.print(
            '"If you decline, I won\'t kill you, but I will beat you within an inch of your life and enslave you for eternity."\n')
        ui.print('"The choice is yours, ' + ctx.player.name + '."\n')
        selection = ui.choose(["Accept offer", "Decline offer"])
        ui.clear()

        if selection == 1:
            char_menu(ctx)
            ui.print(
                'You join the forces of Chernobog, the Prince of Darkness, and forsake your old way of life. You both combine your powers and forge a New Dawn.')
            ui.print()
            ui.wait('end game')

        elif selection == 2:
            ui.print('"Very well, then." Chernobog stands up.')
            ui.wait('fight')

            ctx.enemy = Enemy('', 'Chernobog', 170)
            damage_taken = ctx.combat_damage()
            ctx.player.hp -= damage_taken

            if ctx.player.is_alive():
                ui.print(
                    'You have slain the Antipope. His body magically lights on fire, and leaves ashes on the ground.')
                ui.print(
                    'Your surroundings shimmer, and the city of Salem transforms from its ruined state to its former glory. You have succeeded in every goal.')
                ui.wait()
                char_menu(ctx)
                ui.clear()
                ui.print('You win!')

                ui.print('Occupation: ' + ctx.player.occupation + '')
                ui.wait('end game')

            else:
                char_menu(ctx)
                ui.print()
                ui.print(
                    'You have lost the fight, letting Chernobog win. He enslaves you for all eternity, and he takes over the world.\n')
                ui.wait('end game')

        else:
            raise RuntimeError("Invalid selection (this should never happen)")

        return TitleScreen(self.ctx)


def main():
    map_data = get_map('./data/map.yml')

    global_context = Context(map_data)
    global_context.run(TitleScreen(global_context))


if __name__ == "__main__":
    main()
