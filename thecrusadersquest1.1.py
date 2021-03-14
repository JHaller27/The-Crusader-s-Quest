# Python Text RPG
# Authored by: Gaga Gievous
# Copyright February 2021

from typing import Optional
import random
import yaml

from map import get_map
from ui import ConsoleInterface, DebugInterfaceDecorator
from state import Context, State, TransientState
from enemy import Enemy, get_enemy


with open('./data/player_options.yml', 'r') as fp:
    player_options_config = yaml.safe_load(fp)
with open('./data/enemies.yml', 'r') as fp:
    enemies_config = yaml.safe_load(fp)


# Title Screen #
class TitleScreen(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        ctx.ui.clear()
        ctx.ui.print(
            '#####################################################################################################################')
        ctx.ui.print(
            '#####################################################################################################################')
        ctx.ui.print(
            '##     ## ## ##   ######   ##    ### ## ####  ##    ##  ####   ##    ### ####  #####    #### ## ##   ####  ##     ###')
        ctx.ui.print(
            '#### #### ## ## ######## #### ##  ## ## ### #### ## ## # ### #### ##  ## ### ####### ## #### ## ## ##### ###### #####')
        ctx.ui.print(
            '#### ####    ##   ###### ####   #### ## ###  ###    ## ## ##   ##   ########  ###### ## #### ## ##   ###  ##### #####')
        ctx.ui.print(
            '#### #### ## ## ######## #### # #### ## #### ### ## ## # ### #### # ######### ###### ## #### ## ## ###### ##### #####')
        ctx.ui.print(
            '#### #### ## ##   ######   ## ##  ##    ##  #### ## ##  ####   ## ##  #####  #######      ##    ##   ##  ###### #####')
        ctx.ui.print(
            '#####################################################################################################################')
        ctx.ui.print(
            '#####################################################################################################################')
        ctx.ui.print('The Crusader\'s Quest: Survival Text RPG.\n')
        ctx.ui.wait('play')

        return SetupGame(self.ctx)


# Character Creation #

# Name #
class SetupGame(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        ctx.heal_item = 0
        ctx.adventure_state = False

        ctx.ui.clear()
        ctx.ui.print(
            'The Antipope is defiling the holiest religious site in the world. You are a warrior monk from the Freemasons, and it is up to you to destroy the Antipope.\n')
        ctx.ui.print('You begin your journey in Goodshire, one of the many towns you hope to pass through.\n')
        ctx.ui.print('What is your name?\n')

        ctx.player.name = ctx.ui.input_text()

        # Race #
        ctx.ui.clear()
        ctx.ui.print('What is your race?\n')

        races = player_options_config.get('races')

        selection = ctx.ui.choose([r['name'] for r in races]) - 1
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

        ctx.ui.clear()

        # Occupation #
        ctx.ui.print('What is your occupation?\n')

        occupations = player_options_config.get('occupations')

        selection = ctx.ui.choose([o['name'] for o in occupations]) - 1
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

        ctx.ui.clear()
        ctx.ui.print('What kind of weapon do you want to use? (ie. sword, poleaxe, etc.)')

        ctx.player.weapon = ctx.ui.input_text()
        gold_mechanic(self.ctx)

        ctx.ui.clear()
        ctx.ui.print(ctx.player.description)

        selection = ctx.ui.choose(["Begin Adventure", "Restart"])
        if selection == 1:
            return StartGame(self.ctx)
        else:
            return TitleScreen(self.ctx)


# Death #
class Death(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        ctx.ui.clear()
        ctx.ui.print('You have died.\n')
        ctx.ui.wait()
        char_menu(self.ctx)
        ctx.ui.print()
        ctx.ui.wait("return to menu")

        return TitleScreen(self.ctx)


def gold_mechanic(ctx: Context):
    if ctx.player.gold < 1:
        ctx.player.gold = 0
    if ctx.player.gold > ctx.player.max_gold:
        ctx.player.gold = ctx.player.max_gold
        ctx.ui.print('You have completely filled your coin purse.')
    if ctx.player.gold < 1:
        ctx.player.gold = 0


def food_mechanic(ctx: Context):
    if ctx.player.food > ctx.player.max_food:
        ctx.player.food = ctx.player.max_food
        ctx.ui.print('You have maxed out your food supply.')
    if ctx.player.food < 1:
        ctx.player.food = 0


def arrows_mechanic(ctx: Context):
    if ctx.player.arrows < 1:
        ctx.player.arrows = 0
    if ctx.player.arrows > ctx.player.max_arrows:
        ctx.player.arrows = ctx.player.max_arrows
        ctx.ui.print('You have maxed out your arrow count.')
    if ctx.player.arrows < 1:
        ctx.player.arrows = 0


# Character Menu #
def char_menu(ctx: Context):
    ctx.ui.clear()
    ctx.char_menu()


# Adventure Menu #
def adventure_menu(ctx: Context):
    ctx.ui.clear()
    ctx.adventure_menu()


# Map #
class TheMap(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        # ctx.ui.print('Key: T = Town; C = City; etc.)
        ctx.display_map()

        return DaysToGo(self.ctx, self.default)


# Days to Go #
class DaysToGo(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        if ctx.adventure_state:
            ctx.ui.print('You have ' + str(ctx.counter) + ' days to go.')
            ctx.ui.wait()

            return None

        location = ctx.get_location()
        distance = location.distance
        ctx.counter_set = ctx.counter = distance

        ctx.ui.print(f"You will brave the wilds for {distance} days.")
        selection = ctx.ui.choose(['Continue', 'Go back'])

        if selection == 1:
            ctx.ui.wait()
            return Adventuring(self.ctx)

        return Town(self.ctx)


# Treasure Generator #
# def treasure_generator():
# v = random.randint(0, 3)
# ctx.ui.print('You found ' + str(v) + ' treasures on this leg of the journey.')


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


# Town Description #
def town_description(ctx: Context):
    ctx.town_description()


# Start Game #
class StartGame(State):
    def do(self) -> Optional[State]:
        return Town(self.ctx)


# Town #
class Town(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        ctx.ui.clear()
        ctx.ui.print('You are in ' + ctx.location + '.')
        town_description(ctx)
        ctx.ui.print()
        selection = ctx.ui.choose(["Tavern", "Blacksmith", "Character", "Adventure"])
        if selection == 1:
            ctx.ui.clear()
            return Tavern(self.ctx)

        if selection == 4:
            ctx.ui.clear()
            ctx.counter = 0
            return TheMap(ctx, LeaveTown)

        if selection == 2:
            ctx.ui.clear()
            return Blacksmith(self.ctx)
        if selection == 3:
            ctx.ui.clear()
            char_menu(self.ctx)
        return Town(self.ctx)


class LeaveTown(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        ctx.ui.print('You will brave the wilds for 5 days.')
        ctx.ui.wait()
        return Adventuring(self.ctx)


# Tavern #
class Tavern(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        ctx.ui.clear()
        ctx.ui.print('######################')
        ctx.ui.print('Gold: ' + str(ctx.player.gold) + '/' + str(ctx.player.max_gold) + '')
        ctx.ui.print('HP: ' + str(ctx.player.hp) + '/' + str(ctx.player.max_hp) + '')
        ctx.ui.print('Food: ' + str(ctx.player.food) + '/' + str(ctx.player.max_food) + '')
        ctx.ui.print('######################\n')
        ctx.ui.print('"Welcome to the ' + ctx.location + ' Inn. How may I serve you?"\n')

        selection = ctx.ui.choose(['Rest (1 gold)', 'Buy Food (5 gold)', 'Sell Food (3 gold)', 'Speak with random patron', 'Back'])
        if selection == 1:
            if ctx.player.gold < 1:
                ctx.ui.print('You cannot afford a bed here.')
                ctx.ui.wait('continue.')
            else:
                ctx.ui.print('You slept like a rock.')
                ctx.player.fill_hp()
                ctx.player.gold -= 1
                ctx.ui.wait('continue')

        elif selection == 2:
            ctx.ui.print('How much food do you want to buy?')
            ctx.player.food_price = 5
            n = ctx.ui.input_text()
            n = int(n)

            if n == 0:
                return Tavern(self.ctx)

            total_cost = n * ctx.player.food_price

            if total_cost > ctx.player.gold:
                ctx.ui.print('You do not have enough gold to buy ' + str(n) + ' food.')
                ctx.ui.wait()

            elif total_cost <= ctx.player.gold:
                ctx.player.food = ctx.player.food + n
                food_mechanic(self.ctx)
                ctx.player.gold = ctx.player.gold - total_cost
                ctx.ui.print('You complete the transaction')
                ctx.ui.wait()

        elif selection == 3:
            ctx.ui.print('How much food do you want to sell?')
            food_sell = 3
            n = ctx.ui.input_text()

            if n == 0:
                return Tavern(self.ctx)

            n = int(n)
            total_sell = n * food_sell

            if ctx.player.food < n:
                ctx.ui.print('You do not have that much food.')
                ctx.ui.wait()

            if ctx.player.food >= n:
                ctx.player.food = ctx.player.food - n
                ctx.player.gold = ctx.player.gold + total_sell
                ctx.ui.print('You complete the transaction')
                gold_mechanic(self.ctx)
                ctx.ui.wait()
                ctx.ui.clear()

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
            ctx.ui.print('I don\'t take too kindly to travelers.')
        if dialogue == 2:
            ctx.ui.print('I\'m too scared to leave ' + ctx.location + '. I don\'t know how you survive out there.')
        if dialogue == 3:
            ctx.ui.print('The ' + ctx.location + ' Inn is the best tavern in the world. Not that I would know.')
        if dialogue == 4:
            ctx.ui.print('There\'s nasty things where you\'re headed.')
        if dialogue == 5:
            ctx.ui.print("Someone I know was killed looking inside a hollow tree. You wouldn't want that happening to you.")
        if dialogue == 6:
            ctx.ui.print('If you run out of food and arrows in the wilds, how will you survive? On pure endurance ?')
        if dialogue == 7:
            ctx.ui.print('If you want stronger equipment, I recommend going to the blacksmith.')
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
            ctx.ui.print('In the wilds, I got caught in a hunter\'s trap. That\'s how I lost my ' + part + '.')
        if dialogue == 9:
            ctx.ui.print('Tales of the beasts and Satanic denizens in the wilds have kept me inside the city walls.')
        if dialogue == 10:
            ctx.ui.print('The good thing about resting at ' + ctx.location + ' Inn is that you get a complimentary meal.')
        ctx.ui.wait()
        return Tavern(self.ctx)


# Blacksmith #
class Blacksmith(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        ctx.ui.clear()
        ctx.ui.print('######################')
        ctx.ui.print('Gold: ' + str(ctx.player.gold) + '/' + str(ctx.player.max_gold) + '')
        ctx.ui.print('Arrows: ' + str(ctx.player.arrows) + '/' + str(ctx.player.max_arrows) + '')
        ctx.ui.print('Martial Prowess: ' + str(ctx.martial_prowess) + '')
        ctx.ui.print('######################\n')
        ctx.ui.print('"What can I do for you, traveler?"')

        selection = ctx.ui.choose([
            f"Upgrade your {ctx.player.weapon} ({ctx.blacksmith_price} gold)",
            "Buy Arrows (5 gold)",
            "Sell Arrows (3 gold)",
            "Back",
        ])
        if selection == 1:
            if ctx.player.gold < ctx.blacksmith_price:
                ctx.ui.print('You do not have enough gold to upgrade your ' + ctx.player.weapon + '.')
                ctx.ui.wait()
            else:
                ctx.player.gold = ctx.player.gold - ctx.blacksmith_price
                gold_mechanic(self.ctx)
                v = random.randint(10, 30)
                ctx.martial_prowess = ctx.martial_prowess + v
                ctx.ui.print('Your martial prowess increases by ' + str(v) + '.')
                ctx.ui.wait()
            return Blacksmith(self.ctx)
        if selection == 2:
            ctx.ui.print('How many arrows do you want to buy?')
            arrow_price = 5
            n = ctx.ui.input_text()
            n = int(n)
            total_cost = n * arrow_price
            if total_cost > ctx.player.gold:
                ctx.ui.print('You do not have enough gold to buy ' + str(n) + ' arrows.')
                ctx.ui.wait()
                return Blacksmith(self.ctx)
            if total_cost <= ctx.player.gold:
                ctx.player.arrows = ctx.player.arrows + n
                arrows_mechanic(self.ctx)
                ctx.player.gold = ctx.player.gold - total_cost
                ctx.ui.print('You complete the transaction')
                ctx.ui.wait()
                return Blacksmith(self.ctx)
        if selection == 3:
            ctx.ui.print('How many arrows do you want to sell?')
            arrow_sell = 3
            n = ctx.ui.input_text()
            n = int(n)
            total_sell = n * arrow_sell
            if ctx.player.arrows < n:
                ctx.ui.print('You do not have that many arrows.')
                ctx.ui.wait()
                return Blacksmith(self.ctx)
            if ctx.player.arrows >= n:
                ctx.player.arrows = ctx.player.arrows - n
                ctx.player.gold = ctx.player.gold + total_sell
                ctx.ui.print('You complete the transaction')
                gold_mechanic(self.ctx)
                ctx.ui.wait()
                ctx.ui.clear()
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
            selection = ctx.ui.choose(["Continue", "Hunt", "Rest", "Map"])
            ctx.ui.clear()
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
        ctx.ui.clear()
        adventure_menu(self.ctx)
        ctx.ui.print('You have survived the trip.')
        ctx.adventure_state = False
        ctx.ui.wait()

        return LocationChanger(self.ctx)


# Rest #
class Rest(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        if not ctx.player.is_alive():
            return Death(self.ctx)

        if ctx.player.hp == ctx.player.max_hp:
            ctx.ui.print('You rest for one day. Your HP is already maxed out.')
            ctx.ui.wait()

            return Adventuring(self.ctx)

        x = random.randint(15, 25)

        ctx.player.hp += x
        ctx.ui.print('You rest for one day, gaining ' + str(x) + ' HP.')

        ctx.ui.wait()


# Hunt #
class Hunt(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        x = random.randint(1, 10)
        y = random.randint(1, 25)

        if ctx.player.arrows == 0:
            ctx.ui.print('You do not have any arrows to hunt with.')
            ctx.ui.wait()
            return Adventuring(self.ctx)

        elif ctx.player.arrows < x:
            adventure_menu(self.ctx)
            x = ctx.player.arrows
            ctx.player.arrows = ctx.player.arrows - x
            ctx.player.food = ctx.player.food + y
            arrows_mechanic(self.ctx)
            ctx.ui.print('You shot ' + str(x) + ' arrows, and gained ' + str(y) + ' food.')
            food_mechanic(self.ctx)

        else:
            adventure_menu(self.ctx)
            ctx.player.arrows = ctx.player.arrows - x
            ctx.player.food = ctx.player.food + y
            arrows_mechanic(self.ctx)
            food_mechanic(self.ctx)
            ctx.ui.print('You shot ' + str(x) + ' arrows, and gained ' + str(y) + ' food.')

        ctx.ui.wait()

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

        ctx.ui.print('You see a strange mushroom.')
        selection = ctx.ui.choose(["Consume", "Leave"])
        if selection == 1:
            x = random.randint(1, 4)
            if x == 1:
                if ctx.player.race == 'Satyr':
                    w = ctx.player.consumption_rate + ctx.player.consumption_rate + ctx.player.consumption_rate
                    ctx.player.consumption_rate = ctx.player.consumption_rate + w
                    ctx.ui.print('You eat the mushroom, and gain ' + str(w) + ' Endurance.')
                else:
                    ctx.ui.print('You eat the mushroom, and nothing happened.')
            if x == 2:
                if ctx.player.race == 'Satyr':
                    w = ctx.player.consumption_rate + ctx.player.consumption_rate + ctx.player.consumption_rate
                    ctx.player.consumption_rate = ctx.player.consumption_rate + w
                    ctx.ui.print('You eat the mushroom, and gain ' + str(w) + ' Endurance.')
                else:
                    ctx.ui.print('You eat the mushroom, and it causes you to vomit.')
                    if not ctx.player.is_alive():
                        return Death(self.ctx)

            if x == 3:
                w = ctx.player.consumption_rate + ctx.player.consumption_rate
                ctx.player.consumption_rate = ctx.player.consumption_rate + w
                ctx.ui.print('You eat the mushroom, and gain ' + str(w) + ' Endurance.')
            if x == 4:
                if ctx.player.race == 'Satyr':
                    w = ctx.player.consumption_rate + ctx.player.consumption_rate
                    ctx.player.consumption_rate = ctx.player.consumption_rate + w
                    ctx.ui.print('You eat the mushroom, and gain ' + str(w) + ' Endurance.')
                else:
                    ctx.player.hp = 0
                    ctx.endurance = 0
                    ctx.ui.print('You eat the mushroom, and then fall to the ground, foaming at the mouth.')
                    ctx.ui.wait()
                    return Death(self.ctx)

        elif selection == 2:
            ctx.ui.print('You leave the mushroom.')
        else:
            return Mushroom(self.ctx, self.default)
        ctx.ui.wait()


# Miracle #
class Miracle(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        if ctx.player.race == 'Halfling':
            ctx.ui.print('You see an old wizard, and the wizard beckons you over.')
            ctx.ui.print('"Ho, there, traveler!"')
            ctx.ui.print('"I did not expect to see a Halfing out in the wilderness."')
            ctx.ui.print('"This is delightful. Here, have a gift."')

            selection = ctx.ui.choose(["Fill Food", "Fill Arrows", "Fill Gold", "Fill HP"])
            if selection == 1:
                ctx.player.food = ctx.player.max_food
                food_mechanic(self.ctx)
            if selection == 2:
                ctx.player.arrows = ctx.player.max_arrows
                arrows_mechanic(self.ctx)
            if selection == 3:
                ctx.player.gold = ctx.player.max_gold
                gold_mechanic(self.ctx)
            if selection == 4:
                ctx.player.fill_hp()
            ctx.ui.wait()
        else:
            return Nothing(self.ctx, self.default)


# Bigger Bag #
class BiggerBag(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        y = random.randint(1, 3)
        if y == 1:
            ctx.player.max_food = ctx.player.max_food + 10
            ctx.ui.print(
                'You find an empty food storage container on the side of the path, and it holds more food than your current one.')
            ctx.ui.wait('take\n')
            ctx.ui.print('Max food increased by 10.')
        if y == 2:
            ctx.player.max_arrows = ctx.player.max_arrows + 10
            ctx.ui.print('You spot an empty quiver on the side of the path. It holds more arrows than your current one.')
            ctx.ui.wait('take\n')
            ctx.ui.print('Max arrows increased by 10.')
        if y == 3:
            ctx.player.max_gold = ctx.player.max_gold + 100
            ctx.ui.print('You discover an empty coin purse on the side of the path. It holds more gold than your current one.')
            ctx.ui.wait('take\n')
            ctx.ui.print('Max gold increased by 100.')
        ctx.ui.print()
        ctx.ui.wait()

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

        ctx.ui.print('You realize that you are lost. It will take you ' + str(v) + ' days to get back on the right path.')
        # if y == 2:
        # if ctx.location == 'Goodshire' or 'Rodez':
        # ctx.ui.print('You arrive at a bridge spanning a massive whitewater river that is guarded by a score of bandits. One bandit approaches you.')
        # elif ctx.location == 'Oristano' or 'Thasos' or 'Karabuk':
        # ctx.ui.print('You arrive at a bridge spanning an enormous chasm that is guarded by a score of bandits. One bandit approaches you.')
        # ctx.ui.print('"If you want to cross this bridge, you have to pay us, ' + str(k) 'ctx.player.gold.\n')
        #        ctx.ui.print('1 Pay ctx.player.gold\n2 Take a detour\n')
        #        selection = ctx.ui.input('>: ')
        #        if selection == 1:
        #            if k > ctx.player.gold:
        #            ctx.ui.print('"That is not enough to cross, but we will keep what you gave us, and you can find another way around. Have fun out there."')
        #            ctx.player.gold = 0
        #            else:
        #               ctx.player.gold = ctx.player.gold - k
        #               ctx.ui.print('You gave the bandit ' + str(k) + ' ctx.player.gold, and they let you cross the bridge.')
        #       elif selection == 2
        #       else:
        #           selection = ctx.ui.input('>: ')

        ctx.ui.wait()

        return None


# Mystic #
class Mystic(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        ctx.ui.print('You come upon a roaming mystic.')
        ctx.ui.print('The mystic offers you a blessing.\n')

        selection = ctx.ui.choose(["Increase Max HP", "Increase Endurance", "Increase Martial Prowess"])
        if selection == 1:
            ctx.player.max_hp = ctx.player.max_hp + 10
            ctx.player.hp = ctx.player.hp + 10
            ctx.ui.print('Your max HP increases by 10.')
            ctx.ui.wait()
        elif selection == 2:
            ctx.endurance = ctx.endurance + ctx.player.consumption_rate
            ctx.ui.print('Your endurance increases by ' + str(ctx.player.consumption_rate) + '.')
            ctx.ui.wait()
        elif selection == 3:
            ctx.martial_prowess = ctx.martial_prowess + 10
            ctx.ui.print('Your martial prowess increases by 10.')
            ctx.ui.wait()
        else:
            return Mystic(self.ctx, self.default)


# Nothing #
class Nothing(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        ctx.ui.print('Nothing notable happens.')
        ctx.ui.wait()

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
            ctx.ui.print('You sprain your ankle in a divot, taking ' + str(v) + ' damage.')
            ctx.ui.print('However, you find ' + str(g) + ' gold on the ground.')
            gold_mechanic(self.ctx)
        if n == 2:
            f = random.randint(1, 20)
            ctx.player.food = ctx.player.food + f
            ctx.ui.print('You are stung by a swarm of bees, taking ' + str(v) + ' damage.')
            ctx.ui.print('However, you manage to take ' + str(f) + ' honey before you flee.')
            food_mechanic(self.ctx)

        if n == 3:
            a = random.randint(1, 20)
            ctx.player.arrows = ctx.player.arrows + a
            ctx.ui.print('You walk into an hunter\'s trap, taking ' + str(v) + ' damage.')
            ctx.ui.print('However, you find ' + str(a) + ' arrows nearby.')
            arrows_mechanic(self.ctx)

        ctx.ui.wait()

        return None


# Traveller #
class Traveller(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        time_of_day = random.choice(['morning', 'evening', 'afternoon'])

        ctx.ui.print('A friendly adventurer approaches you and wants to trade.')
        ctx.ui.print(f'"Good {time_of_day}, traveler."\n')

        traveller_values(self.ctx)

        return None


# Traveller Values #
def traveller_values(ctx: Context):
    traveller_generation(ctx)
    ctx.ui.wait()


# Traveller Generation #
def traveller_generation(ctx: Context):
    x = random.randint(1, 50)  # how much trader wants
    v = random.randint(1, 100)  # how much trader is willing to give
    c = random.randint(1, 4)  # what trader wants

    if c == 1:
        ctx.ui.print('The trader wants ' + str(x) + ' food.')
        p = random.randint(1, 3)  # what trader is giving
        if p == 1:
            ctx.ui.print('The trader is willing to give ' + str(v) + ' arrows.')
            selection = ctx.ui.choose(["Accept", "Decline"])
            if selection == 1:
                if ctx.player.food < x:
                    ctx.ui.print('You cannot afford the trade.')
                else:
                    ctx.player.food = ctx.player.food - x
                    ctx.player.arrows = ctx.player.arrows + v
                    ctx.ui.print('You accept the trade.')
                    arrows_mechanic(ctx)

            else:
                ctx.ui.print('You decline the trade.')

        if p == 2:
            ctx.ui.print('The trader is willing to pay ' + str(v) + ' gold.')
            selection = ctx.ui.choose(["Accept", "Decline"])
            if selection == 1:
                if ctx.player.food < x:
                    ctx.ui.print('You cannot afford the trade.')
                else:
                    ctx.player.food = ctx.player.food - x
                    ctx.player.gold = ctx.player.gold + v
                    ctx.ui.print('You accept the trade.')
                    gold_mechanic(ctx)

            else:
                ctx.ui.print('You decline the trade.')

        if p == 3:
            ctx.ui.print('The trader is willing to heal you ' + str(v) + ' HP.')
            selection = ctx.ui.choose(["Accept", "Decline"])
            if selection == 1:
                if ctx.player.food < x:
                    ctx.ui.print('You cannot afford the trade.')
                else:
                    ctx.player.food = ctx.player.food - x
                    ctx.player.hp += v
                    ctx.ui.print('You accept the trade.')

            else:
                ctx.ui.print('You decline the trade.')
    if c == 2:
        ctx.ui.print('The trader wants ' + str(x) + ' arrows.')
        p = random.randint(1, 3)  # what trader is giving
        if p == 1:
            ctx.ui.print('The trader is willing to give ' + str(v) + ' food.')
            selection = ctx.ui.choose(["Accept", "Decline"])
            if selection == 1:
                if ctx.player.arrows < x:
                    ctx.ui.print('You cannot afford the trade.')
                else:
                    ctx.player.arrows = ctx.player.arrows - x
                    ctx.player.food = ctx.player.food + v
                    ctx.ui.print('You accept the trade.')
                    food_mechanic(ctx)

            else:
                ctx.ui.print('You decline the trade.')
        if p == 2:
            ctx.ui.print('The trader is willing to give ' + str(v) + ' gold.')
            selection = ctx.ui.choose(["Accept", "Decline"])
            if selection == 1:
                if ctx.player.arrows < x:
                    ctx.ui.print('You cannot afford the trade.')
                else:
                    ctx.player.arrows = ctx.player.arrows - x
                    ctx.player.gold = ctx.player.gold + v
                    ctx.ui.print('You accept the trade.')
                    gold_mechanic(ctx)

            else:
                ctx.ui.print('You decline the trade.')
        if p == 3:
            ctx.ui.print('The trader is willing to heal you for ' + str(v) + ' HP.')
            selection = ctx.ui.choose(["Accept", "Decline"])
            if selection == 1:
                if ctx.player.arrows < x:
                    ctx.ui.print('You cannot afford the trade.')
                else:
                    ctx.player.arrows -= x
                    ctx.player.hp += v
                    ctx.ui.print('You accept the trade.')

            else:
                ctx.ui.print('You decline the trade.')
    if c == 3:
        ctx.ui.print('The trader wants ' + str(x) + ' gold.')
        p = random.randint(1, 3)  # what trader is giving
        if p == 1:
            ctx.ui.print('The trader is willing to give ' + str(v) + ' food.')
            selection = ctx.ui.choose(["Accept", "Decline"])
            if selection == 1:
                if ctx.player.gold < x:
                    ctx.ui.print('You cannot afford the trade.')
                else:
                    ctx.player.gold = ctx.player.gold - x
                    ctx.player.food = ctx.player.food + v
                    ctx.ui.print('You accept the trade.')
                    food_mechanic(ctx)

            else:
                ctx.ui.print('You decline the trade.')
        if p == 2:
            ctx.ui.print('The trader is willing to give ' + str(v) + ' arrows.')
            selection = ctx.ui.choose(["Accept", "Decline"])
            if selection == 1:
                if ctx.player.gold < x:
                    ctx.ui.print('You cannot afford the trade.')
                else:
                    ctx.player.gold = ctx.player.gold - x
                    ctx.player.arrows = ctx.player.arrows + v
                    ctx.ui.print('You accept the trade.')
                    arrows_mechanic(ctx)

            else:
                ctx.ui.print('You decline the trade.')

        if p == 3:
            ctx.ui.print('The trader is willing to heal you ' + str(v) + ' HP.')
            selection = ctx.ui.choose(["Accept", "Decline"])
            if selection == 1:
                if ctx.player.gold < x:
                    ctx.ui.print('You cannot afford the trade.')
                else:
                    ctx.player.gold -= x
                    ctx.player.hp += v
                    ctx.ui.print('You accept the trade.')

            else:
                ctx.ui.print('You decline the trade.')
    if c == 4:
        ctx.ui.print('The trader wants your blood. Specifically, ' + str(x) + ' HP.')
        p = random.randint(1, 3)  # what trader is giving
        if p == 1:
            ctx.ui.print('The trader is willing to give ' + str(v) + ' food.')
            selection = ctx.ui.choose(["Accept", "Decline"])
            if selection == 1:
                if ctx.player.hp < x:
                    ctx.ui.print('You cannot afford the trade, but the trader is willing to let you slide, this time.')
                    ctx.player.hp = ctx.player.hp - x
                    ctx.player.food = ctx.player.food + v
                    food_mechanic(ctx)
                else:
                    ctx.player.hp = ctx.player.hp - x
                    ctx.player.food = ctx.player.food + v
                    ctx.ui.print('You accept the trade.')
                    food_mechanic(ctx)

            else:
                ctx.ui.print('You decline the trade.')
        if p == 2:
            ctx.ui.print('The trader is willing to give ' + str(v) + ' arrows.')
            selection = ctx.ui.choose(["Accept", "Decline"])
            if selection == 1:
                if ctx.player.hp < x:
                    ctx.ui.print('You cannot afford the trade, but the trader is willing to let you slide, this time.')
                    ctx.player.hp = ctx.player.hp - x
                    ctx.player.food = ctx.player.food + v
                    food_mechanic(ctx)
                else:
                    ctx.player.hp = ctx.player.hp - x
                    ctx.player.arrows = ctx.player.arrows + v
                    ctx.ui.print('You accept the trade.')
                    arrows_mechanic(ctx)

            else:
                ctx.ui.print('You decline the trade.')
        if p == 3:
            ctx.ui.print('The trader is willing to give ' + str(v) + ' gold.')
            selection = ctx.ui.choose(["Accept", "Decline"])
            if selection == 1:
                if ctx.player.hp < x:
                    ctx.ui.print('You cannot afford the trade, but the trader is willing to let you slide, this time.')
                    ctx.player.hp = ctx.player.hp - x
                    ctx.player.food = ctx.player.food + v
                    food_mechanic(ctx)
                else:
                    ctx.player.hp = ctx.player.hp - x
                    ctx.player.gold = ctx.player.gold + v
                    ctx.ui.print('You accept the trade.')
                    gold_mechanic(ctx)

            else:
                ctx.ui.print('You decline the trade.')


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
            food_mechanic(self.ctx)
            y = random.randint(1, 2)
            # adventure_menu()
            if y == 1:
                ctx.ui.print('During the night, a shadowy figure stole ' + str(v) + ' of your food.')
            elif y == 2:
                ctx.ui.print('You check your food supply and find that ' + str(v) + ' food is missing.')
        elif x == 2:
            v = random.randint(1, 50)
            if ctx.player.arrows < v:
                v = ctx.player.arrows
            ctx.player.arrows = ctx.player.arrows - v
            arrows_mechanic(self.ctx)
            y = random.randint(1, 2)
            # adventure_menu()
            if y == 1:
                ctx.ui.print('During the night, a shadowy figure stole ' + str(v) + ' of your arrows.')
            elif y == 2:
                ctx.ui.print('You check your arrow quill, and find that ' + str(v) + ' arrows are missing.')

        elif x == 3:
            v = random.randint(1, 50)
            if ctx.player.gold < v:
                v = ctx.player.gold
            ctx.player.gold = ctx.player.gold - v
            gold_mechanic(self.ctx)
            y = random.randint(1, 2)
            # adventure_menu()
            if y == 1:
                ctx.ui.print('During the night, a shadowy figure stole ' + str(v) + ' of your gold.')
            elif y == 2:
                ctx.ui.print('You check your coin purse, and find that ' + str(v) + ' gold is missing.')


# Fight #
class Fight(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        ctx.enemy = get_enemy(enemy_locator_generator(ctx))
        ctx.ui.print(f"You see a {ctx.enemy.name} approaching.")

        if ctx.enemy.is_type("Doppelganger"):
            ctx.ui.print(f"The doppelganger is wielding a {ctx.player.weapon} exactly like yours.")

        selection = ctx.ui.choose(["Fight", "Flee"])
        if selection == 1:
            return FightSimulation(ctx, self.default)

        return FleeFight(ctx, self.default)


# Fight Simulation #
class FightSimulation(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        your_damage_taken(ctx)
        enemy_loot(ctx)

        ctx.ui.wait()

        ctx.enemy = None

        return Adventuring(self.ctx)


# Enemy Loot #
def enemy_loot(ctx: Context):
    ctx.player.food += ctx.enemy.food
    ctx.player.arrows += ctx.enemy.arrows
    ctx.player.gold += ctx.enemy.gold

    ctx.ui.print(f"You found {ctx.enemy.food} food, "
                 f"{ctx.enemy.arrows} arrows, and"
                 f"{ctx.enemy.gold} gold on the corpse.")

    food_mechanic(ctx)
    arrows_mechanic(ctx)
    gold_mechanic(ctx)


# Your Damage Taken #
def your_damage_taken(ctx: Context):
    damage_taken = ctx.combat_damage()

    ctx.player.hp -= damage_taken

    if damage_taken < 1:
        ctx.ui.print("The enemy was slain, and you took no damage.")
    else:
        ctx.ui.print(f"The enemy was slain, but you took {damage_taken} damage.")


# Flee Fight #
class FleeFight(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        n = random.randint(1, 2)
        if n == 2:
            ctx.ui.print('You failed to flee the fight.')
            ctx.ui.wait()

            return FightSimulation(self.ctx, self.default)

        ctx.ui.print('You escaped the fight.')
        ctx.ui.wait()
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
            ctx.ui.print('You see a treasure chest.')
        if p == 2:
            ctx.ui.print('You see a large hollow tree.')
        selection = ctx.ui.choose(["Inspect", "Avoid"])
        if selection == 1:
            a = random.randint(1, 3)
            if a == 1:
                ctx.ui.print('It is empty. Nothing but cobwebs remain.')
                ctx.ui.wait()
                adventure_menu(self.ctx)
            if a == 2:
                ctx.ui.print('It was booby trapped. A dart flies out and hits you for 20 damage.')
                ctx.player.hp -= 20
                ctx.ui.wait()

                if not ctx.player.is_alive():
                    return Death(self.ctx)

                adventure_menu(self.ctx)
            # if a == 2 and ctx.luck > 0:
            # ctx.ui.print('It was booby trapped. A dart flies out and hits you for 20 damage.')
            # chest_loot()
            if a == 3:
                return ChestLoot(self.ctx)

        elif selection == 2:
            ctx.ui.print()

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
            ctx.ui.print('Inside, you found ' + str(v) + ' food.')
            food_mechanic(ctx)
        if x == 2:
            v = random.randint(50, 100)
            ctx.player.arrows = ctx.player.arrows + v
            ctx.ui.print('Inside, you found ' + str(v) + ' arrows.')
            arrows_mechanic(ctx)
        if x == 3:
            v = random.randint(50, 100)
            ctx.player.gold = ctx.player.gold + v
            ctx.ui.print('Inside, you found ' + str(v) + ' gold.')
            gold_mechanic(ctx)

        ctx.ui.wait()
        return adventure_menu(self.ctx)


# Salem #
class Salem(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        ctx.display_map()
        ctx.ui.print('Salem\n')
        ctx.ui.wait()
        ctx.ui.clear()

        ctx.ui.print(
            'You enter the ancient city of Salem, now blackened with fire and as silent as a graveyard, and see a man who looks like a commoner lounging upon a throne of skeletons in the courtyard.')
        ctx.ui.print('"Ah, ' + ctx.player.name + '", I was expecting you."\n')
        ctx.ui.print('Type \'who are you?\'')
        ctx.ui.input_text()

        ctx.ui.clear()
        ctx.ui.print('"I am the called by your order the Antipope or the Prince of Darkness, but my birth name is Chernobog."')
        ctx.ui.print(
            '"As you can see, I have already razed Salem. Your sacred temples and artifacts are totally destroyed. You have failed."')
        ctx.ui.print('"But I admire your willpower and resourcefulness to make it all the way here from Goodshire."')
        ctx.ui.print('"I want to make you an offer. Join me, and become my champion. Together, we will forge a New Dawn."')
        ctx.ui.print('"Your old ways are gone. You have failed your order, and they will no longer accept you."')
        ctx.ui.print(
            '"If you decline, I won\'t kill you, but I will beat you within an inch of your life and enslave you for eternity."\n')
        ctx.ui.print('"The choice is yours, ' + ctx.player.name + '."\n')
        selection = ctx.ui.choose(["Accept offer", "Decline offer"])
        ctx.ui.clear()

        if selection == 1:
            char_menu(ctx)
            ctx.ui.print(
                'You join the forces of Chernobog, the Prince of Darkness, and forsake your old way of life. You both combine your powers and forge a New Dawn.')
            ctx.ui.print()
            ctx.ui.wait('end game')

        elif selection == 2:
            ctx.ui.print('"Very well, then." Chernobog stands up.')
            ctx.ui.wait('fight')

            ctx.enemy = Enemy('', 'Chernobog', 170)
            damage_taken = ctx.combat_damage()
            ctx.player.hp -= damage_taken

            if ctx.player.hp > 0:
                ctx.ui.print('You have slain the Antipope. His body magically lights on fire, and leaves ashes on the ground.')
                ctx.ui.print(
                    'Your surroundings shimmer, and the city of Salem transforms from its ruined state to its former glory. You have succeeded in every goal.')
                ctx.ui.wait()
                char_menu(ctx)
                ctx.ui.clear()
                ctx.ui.print('You win!')

                ctx.ui.print('Occupation: ' + ctx.player.occupation + '')
                ctx.ui.wait('end game')

            else:
                ctx.player.hp = 0.1
                char_menu(ctx)
                ctx.ui.print()
                ctx.ui.print('You have lost the fight, letting Chernobog win. He enslaves you for all eternity, and he takes over the world.\n')
                ctx.ui.wait('end game')

        else:
            raise RuntimeError("Invalid selection (this should never happen)")

        return TitleScreen(self.ctx)


def main():
    ui = ConsoleInterface()
    ui = DebugInterfaceDecorator(ui)

    map_data = get_map('./data/map.yml')

    global_context = Context(ui, map_data)
    global_context.run(TitleScreen(global_context))


if __name__ == "__main__":
    main()
