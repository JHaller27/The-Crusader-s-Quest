# Python Text RPG
# Authored by: Gaga Gievous
# Copyright February 2021

from typing import Optional
import random

from ui import ConsoleInterface, DebugInterfaceDecorator
from state import Context, State, TransientState

ui = ConsoleInterface()
# ui = DebugInterfaceDecorator(ui)

global_context = Context(ui)


def clear():
    global_context.ui.clear()


# Title Screen #
class title_screen_selections(State):
    def do(self) -> Optional[State]:
        option = input('>: ')

        if option.lower() == '1':
            return setup_game(self.ctx)
        elif option.lower() == '2':
            return help_menu(self.ctx)
        elif option.lower() == '0':
            return None
        while option.lower() not in ['1', '2', '0']:
            option = input('>: ')
            if option.lower() == '1':
                return setup_game(self.ctx)
            elif option.lower() == '2':
                return help_menu(self.ctx)
            elif option.lower() == '0':
                return None


class title_screen(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        clear()
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
        ctx.ui.print('  1 Play  ')
        ctx.ui.print('  2 Help  ')
        ctx.ui.print('  0 Quit  ')
        return title_screen_selections(self.ctx)


class help_menu(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        ctx.ui.print('Put in controls')
        ctx.ui.print('Etc.')
        return title_screen_selections(self.ctx)


# Character Creation #

# Name #
class setup_game(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        ctx.arrows = 0
        ctx.gold = 0
        ctx.food = 0
        ctx.max_arrows = 0
        ctx.max_gold = 0
        ctx.max_food = 0
        ctx.hp = 0
        ctx.max_hp = 0
        ctx.martial_prowess = 0
        ctx.heal_item = 0
        ctx.endurance = 10
        ctx.adventure_state = False
        clear()
        ctx.ui.print(
            'The Antipope is defiling the holiest religious site in the world. You are a warrior monk from the Freemasons, and it is up to you to destroy the Antipope.\n')
        ctx.ui.print('You begin your journey in Goodshire, one of the many towns you hope to pass through.\n')
        ctx.ui.print('What is your name?\n')

        ctx.name = input('>: ')

        # Race #
        clear()
        ctx.ui.print('What is your race?\n')
        ctx.ui.print('1 Human\n2 Dwarf\n3 Satyr\n4 Halfling\n5 Elf\n6 Tigerman\n7 Leprechaun\n')

        selection = input('>: ')
        if selection == '1':
            ctx.race = "Human"
            ctx.hp = 25
            ctx.max_hp = 25
            ctx.martial_prowess = 10
            ctx.consumption_rate = 10
            ctx.endurance = 30
            ctx.gold = 100
            ctx.luck = 0
            ctx.speed = 0

        elif selection == '2':
            ctx.race = "Dwarf"
            ctx.hp = 50
            ctx.max_hp = 50
            ctx.martial_prowess = 30
            ctx.consumption_rate = 20
            ctx.endurance = 200
            ctx.gold = 200
            ctx.luck = 0
            ctx.speed = 0

        elif selection == '3':
            ctx.race = "Satyr"
            ctx.hp = 100
            ctx.max_hp = 100
            ctx.martial_prowess = 0
            ctx.consumption_rate = 20
            ctx.endurance = 200
            ctx.gold = 0
            ctx.luck = 0
            ctx.speed = 0

        elif selection == '4':
            ctx.race = "Halfling"
            ctx.hp = 25
            ctx.max_hp = 25
            ctx.martial_prowess = 0
            ctx.consumption_rate = 20
            ctx.endurance = 200
            ctx.gold = 100
            ctx.luck = 0
            ctx.speed = 0

        elif selection == '5':
            ctx.race = "Elf"
            ctx.hp = 10
            ctx.max_hp = 10
            ctx.martial_prowess = 0
            ctx.consumption_rate = 10
            ctx.endurance = 1000
            ctx.gold = 100
            ctx.luck = 0
            ctx.speed = 0

        elif selection == '6':
            ctx.race = "Tigerman"
            ctx.hp = 25
            ctx.max_hp = 25
            ctx.martial_prowess = 50
            ctx.consumption_rate = 20
            ctx.endurance = 100
            ctx.gold = 0
            ctx.luck = 0
            ctx.speed = 0

        elif selection == '7':
            ctx.race = "Leprechaun"
            ctx.hp = 10
            ctx.max_hp = 10
            ctx.martial_prowess = 0
            ctx.consumption_rate = 10
            ctx.endurance = 10
            ctx.gold = 1000
            ctx.luck = 0
            ctx.speed = 0

        else:
            ctx.race = "Human"
            ctx.hp = 25
            ctx.max_hp = 25
            ctx.martial_prowess = 10
            ctx.consumption_rate = 10
            ctx.endurance = ctx.endurance + 30
            ctx.gold = 100
            ctx.luck = 0
            ctx.speed = 0

        clear()

        # Occupation #
        ctx.ui.print('What is your occupation?\n')
        ctx.ui.print('1 Hunter\n2 Knight\n3 Adventurer\n4 Assassin\n5 Glutton\n')

        selection = input('>: ')
        if selection == '1':
            ctx.occupation = 'Hunter'
            ctx.hp = ctx.hp + 0
            ctx.max_hp = ctx.max_hp + 0
            ctx.food = ctx.food + 50
            ctx.max_food = ctx.max_food + 150
            ctx.arrows = ctx.arrows + 75
            ctx.max_arrows = ctx.max_arrows + 100
            ctx.gold = ctx.gold + 0
            ctx.max_gold = ctx.max_gold + 800
            ctx.martial_prowess = ctx.martial_prowess + 0
        elif selection == '2':
            ctx.occupation = 'Knight'
            ctx.hp = ctx.hp + 100
            ctx.max_hp = ctx.max_hp + 100
            ctx.food = ctx.food + 25
            ctx.max_food = ctx.max_food + 100
            ctx.arrows = ctx.arrows + 8
            ctx.max_arrows = ctx.max_arrows + 10
            ctx.gold = ctx.gold + 400
            ctx.max_gold = ctx.max_gold + 1000
            ctx.martial_prowess = ctx.martial_prowess + 20
        elif selection == '3':
            ctx.occupation = 'Adventurer'
            ctx.hp = ctx.hp + 25
            ctx.max_hp = ctx.max_hp + 25
            ctx.food = ctx.food + 75
            ctx.max_food = ctx.max_food + 100
            ctx.arrows = ctx.arrows + 20
            ctx.max_arrows = ctx.max_arrows + 20
            ctx.gold = ctx.gold + 100
            ctx.max_gold = ctx.max_gold + 800
            ctx.martial_prowess = ctx.martial_prowess + 10
        elif selection == '4':
            ctx.occupation = 'Assassin'
            ctx.hp = ctx.hp + 0
            ctx.max_hp = ctx.max_hp + 0
            ctx.food = ctx.food + 25
            ctx.max_food = ctx.max_food + 100
            ctx.arrows = ctx.arrows + 8
            ctx.max_arrows = ctx.max_arrows + 10
            ctx.gold = ctx.gold + 100
            ctx.max_gold = ctx.max_gold + 1000
            ctx.martial_prowess = ctx.martial_prowess + 60
        elif selection == '5':
            ctx.occupation = 'Glutton'
            ctx.hp = ctx.hp + 25
            ctx.max_hp = ctx.max_hp + 25
            ctx.food = ctx.food + 500
            ctx.max_food = ctx.max_food + 500
            ctx.arrows = ctx.arrows + 0
            ctx.max_arrows = ctx.max_arrows + 1
            ctx.gold = ctx.gold + 0
            ctx.max_gold = ctx.max_gold + 1000
            ctx.martial_prowess = ctx.martial_prowess + 0
        else:
            ctx.occupation = 'Hunter'
            ctx.hp = ctx.hp + 25
            ctx.max_hp = ctx.max_hp + 25
            ctx.food = ctx.food + 50
            ctx.max_food = ctx.max_food + 150
            ctx.arrows = ctx.arrows + 75
            ctx.max_arrows = ctx.max_arrows + 100
            ctx.gold = ctx.gold + 0
            ctx.max_gold = ctx.max_gold + 300
            ctx.martial_prowess = ctx.martial_prowess + 0

        clear()

        ctx.ui.print('What kind of weapon do you want to use? (ie. sword, poleaxe, etc.)')

        ctx.weapon = input('>: ')
        gold_mechanic(self.ctx)

        clear()

        # ctx.ui.print('What is your ctx.weapon called? (ie. Thorn, Crusher, etc.)')

        # ctx.weapon = input('>: ')
        clear()

        ctx.ui.print('You are ' + ctx.name + ', the ' + ctx.race + ' ' + ctx.occupation + '. You wield a ' + ctx.weapon + '.\n')
        ctx.ui.print('1 Begin Adventure\n2 Restart')
        selection = input('>: ')
        if selection == '1':
            return start_game(self.ctx)
        else:
            return title_screen(self.ctx)


# Death #
class death(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        clear()
        ctx.ui.print('You have died.\n')
        input('Press enter enter to continue')
        char_menu(self.ctx)
        ctx.ui.print()
        ctx.ui.print('1 Menu\n')
        selection = input('>: ')
        if selection == '1':
            return title_screen(self.ctx)
        else:
            return title_screen(self.ctx)


# Food and Endurance Mechanic #

def food_endurance_mechanic(ctx: Context):
    ctx.food_endurance_mechanic(death)


# Resource Mechanics #

def hp_mechanic(ctx: Context):
    ctx.hp_mechanic(death)


def gold_mechanic(ctx: Context):
    if ctx.gold < 1:
        ctx.gold = 0
    if ctx.gold > ctx.max_gold:
        ctx.gold = ctx.max_gold
        ctx.ui.print('You have completely filled your coin purse.')
    if ctx.gold < 1:
        ctx.gold = 0


def food_mechanic(ctx: Context):
    if ctx.food > ctx.max_food:
        ctx.food = ctx.max_food
        ctx.ui.print('You have maxed out your food supply.')
    if ctx.food < 1:
        ctx.food = 0


def arrows_mechanic(ctx: Context):
    if ctx.arrows < 1:
        ctx.arrows = 0
    if ctx.arrows > ctx.max_arrows:
        ctx.arrows = ctx.max_arrows
        ctx.ui.print('You have maxed out your arrow count.')
    if ctx.arrows < 1:
        ctx.arrows = 0


# Character Menu #
def char_menu(ctx: Context):
    clear()
    ctx.char_menu()


# Adventure Menu #
def adventure_menu(ctx: Context):
    clear()
    ctx.adventure_menu()


# Map ###         Update this to turn X into another symbol when that ctx.location is active
class the_map(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        # ctx.ui.print('Key: T = Town; C = City; etc.)

        if ctx.location == 'Goodshire':
            ctx.ui.print('-----------------')
            ctx.ui.print('| G |   |   |   |')
            ctx.ui.print('+---+---+---+---+')
            ctx.ui.print('| X |   |   |   |')
            ctx.ui.print('+---+---+---+---+')
            ctx.ui.print('|   | X |   |   |')
            ctx.ui.print('+---+---+---+---+')
            ctx.ui.print('|   | X | X |   |')
            ctx.ui.print('+---+---+---+---+')
            ctx.ui.print('|   |   |   | X |')
            ctx.ui.print('+---------------+\n')

        if ctx.location == 'Rodez':
            ctx.ui.print('-----------------')
            ctx.ui.print('| G |   |   |   |')
            ctx.ui.print('+---+---+---+---+')
            ctx.ui.print('| R |   |   |   |')
            ctx.ui.print('+---+---+---+---+')
            ctx.ui.print('|   | X |   |   |')
            ctx.ui.print('+---+---+---+---+')
            ctx.ui.print('|   | X | X |   |')
            ctx.ui.print('+---+---+---+---+')
            ctx.ui.print('|   |   |   | X |')
            ctx.ui.print('+---------------+\n')

        if ctx.location == 'Oristano':
            ctx.ui.print('-----------------')
            ctx.ui.print('| G |   |   |   |')
            ctx.ui.print('+---+---+---+---+')
            ctx.ui.print('| R |   |   |   |')
            ctx.ui.print('+---+---+---+---+')
            ctx.ui.print('|   | O |   |   |')
            ctx.ui.print('+---+---+---+---+')
            ctx.ui.print('|   | X | X |   |')
            ctx.ui.print('+---+---+---+---+')
            ctx.ui.print('|   |   |   | X |')
            ctx.ui.print('+---------------+\n')

        if ctx.location == 'Thasos':
            ctx.ui.print('-----------------')
            ctx.ui.print('| G |   |   |   |')
            ctx.ui.print('+---+---+---+---+')
            ctx.ui.print('| R |   |   |   |')
            ctx.ui.print('+---+---+---+---+')
            ctx.ui.print('|   | O |   |   |')
            ctx.ui.print('+---+---+---+---+')
            ctx.ui.print('|   | T | X |   |')
            ctx.ui.print('+---+---+---+---+')
            ctx.ui.print('|   |   |   | X |')
            ctx.ui.print('+---------------+\n')

        if ctx.location == 'Karabuk':
            ctx.ui.print('-----------------')
            ctx.ui.print('| G |   |   |   |')
            ctx.ui.print('+---+---+---+---+')
            ctx.ui.print('| R |   |   |   |')
            ctx.ui.print('+---+---+---+---+')
            ctx.ui.print('|   | O |   |   |')
            ctx.ui.print('+---+---+---+---+')
            ctx.ui.print('|   | T | K |   |')
            ctx.ui.print('+---+---+---+---+')
            ctx.ui.print('|   |   |   | X |')
            ctx.ui.print('+---------------+\n')

        if ctx.location == 'Salem':
            ctx.ui.print('-----------------')
            ctx.ui.print('| G |   |   |   |')
            ctx.ui.print('+---+---+---+---+')
            ctx.ui.print('| R |   |   |   |')
            ctx.ui.print('+---+---+---+---+')
            ctx.ui.print('|   | O |   |   |')
            ctx.ui.print('+---+---+---+---+')
            ctx.ui.print('|   | T | K |   |')
            ctx.ui.print('+---+---+---+---+')
            ctx.ui.print('|   |   |   | S |')
            ctx.ui.print('+---------------+\n')

        return days_to_go(self.ctx, self.default)


# Days to Go #
class days_to_go(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        if ctx.location == 'Goodshire':
            if not ctx.adventure_state:
                ctx.counter_set = 7
                ctx.counter = 7
                ctx.ui.print('You will brave the wilds for ' + str(ctx.counter_set) + ' days.')
                ctx.ui.print('1 Continue\n2 Back')
                selection = input('>: ')
                if selection == '1':
                    input('Press enter to continue')
                    return adventuring(self.ctx)

                elif selection == '2':
                    return town(self.ctx)
                else:
                    return town(self.ctx)
            else:
                ctx.ui.print('You have ' + str(ctx.counter) + ' days to go.')
                input('Press enter to continue')

        if ctx.location == 'Rodez':
            if not ctx.adventure_state:
                ctx.counter_set = 11
                ctx.counter = 11
                ctx.ui.print('You will brave the wilds for ' + str(ctx.counter_set) + ' days.')
                ctx.ui.print('1 Continue\n2 Back')
                selection = input('>: ')
                if selection == '1':
                    input('Press enter to continue')
                    adventuring(self.ctx)

                if selection == '2':
                    return town(self.ctx)
                else:
                    return town(self.ctx)
            else:
                ctx.ui.print('You have ' + str(ctx.counter) + ' days to go.')
                input('Press enter to continue')
        if ctx.location == 'Oristano':
            if not ctx.adventure_state:
                ctx.counter_set = 15
                ctx.counter = 15
                ctx.ui.print('You will brave the wilds for ' + str(ctx.counter_set) + ' days.')
                ctx.ui.print('1 Continue\n2 Back')
                selection = input('>: ')
                if selection == '1':
                    input('Press enter to continue')
                    adventuring(self.ctx)

                if selection == '2':
                    return town(self.ctx)
                else:
                    return town(self.ctx)
            else:
                ctx.ui.print('You have ' + str(ctx.counter) + ' days to go.')
                input('Press enter to continue')
        if ctx.location == 'Thasos':
            if not ctx.adventure_state:
                ctx.counter_set = 19
                ctx.counter = 19
                ctx.ui.print('You will brave the wilds for ' + str(ctx.counter_set) + ' days.')
                ctx.ui.print('1 Continue\n2 Back')
                selection = input('>: ')
                if selection == '1':
                    input('Press enter to continue')
                    adventuring(self.ctx)

                if selection == '2':
                    return town(self.ctx)
                else:
                    return town(self.ctx)
            else:
                ctx.ui.print('You have ' + str(ctx.counter) + ' days to go.')
                input('Press enter to continue')
        if ctx.location == 'Karabuk':
            if not ctx.adventure_state:
                ctx.counter_set = 25
                ctx.counter = 25
                ctx.ui.print('You will brave the wilds for ' + str(ctx.counter_set) + ' days.')
                ctx.ui.print('1 Continue\n2 Back')
                selection = input('>: ')
                if selection == '1':
                    input('Press enter to continue')
                    adventuring(self.ctx)

                if selection == '2':
                    return town(self.ctx)
                else:
                    return town(self.ctx)
            else:
                ctx.ui.print('You have ' + str(ctx.counter) + ' days to go.')
                input('Press enter to continue')
        if ctx.location == 'Last Refuge':
            if not ctx.adventure_state:
                ctx.counter_set = 25
                ctx.counter = 25
                ctx.ui.print('You will brave the wilds for ' + str(ctx.counter_set) + ' days.')
                ctx.ui.print('1 Continue\n2 Back')
                selection = input('>: ')
                if selection == '1':
                    input('Press enter to continue')
                    adventuring(self.ctx)

                if selection == '2':
                    return town(self.ctx)
                else:
                    return town(self.ctx)
            else:
                ctx.ui.print('You have ' + str(ctx.counter) + ' days to go.')
                input('Press enter to continue')


# Treasure Generator #
# def treasure_generator():
# v = random.randint(0, 3)
# ctx.ui.print('You found ' + str(v) + ' treasures on this leg of the journey.')


# Location Changer #
class location_changer(State):
    def do(self) -> Optional['State']:
        ctx = self.ctx

        ctx.adventure_state = False

        if ctx.location == 'Goodshire':
            ctx.location = 'Rodez'
            blacksmith_price_generator(self.ctx)
            # treasure_generator()

        elif ctx.location == 'Rodez':
            ctx.location = 'Oristano'
            blacksmith_price_generator(self.ctx)

        elif ctx.location == 'Oristano':
            ctx.location = 'Thasos'
            blacksmith_price_generator(self.ctx)

        elif ctx.location == 'Thasos':
            ctx.location = 'Karabuk'
            blacksmith_price_generator(self.ctx)

        elif ctx.location == 'Karabuk':
            ctx.location = 'Salem'
            blacksmith_price_generator(self.ctx)
            return salem(self.ctx)

        elif ctx.location == 'Last Refuge':
            ctx.location = 'Rodez'
            blacksmith_price_generator(self.ctx)
            # end_game()
            return None

        return town(self.ctx)


# Town Description #
def town_description(ctx: Context):
    ctx.town_description()


# Start Game #
class start_game(State):
    def do(self) -> Optional['State']:
        self.ctx.location = 'Goodshire'
        blacksmith_price_generator(self.ctx)
        enemy_locator_generator(self.ctx)
        return town(self.ctx)


# Town #
class town(State):
    def do(self) -> Optional['State']:
        ctx = self.ctx

        clear()
        ctx.ui.print('You are in ' + ctx.location + '.')
        town_description(ctx)
        ctx.ui.print()
        ctx.ui.print('1 Tavern\n2 Blacksmith\n3 Character\n4 Adventure')
        selection = input('>: ')
        if selection == '1':
            clear()
            return tavern(self.ctx)

        if selection == '4':
            clear()
            ctx.counter = 0
            return the_map(ctx, LeaveTown)

        if selection == '2':
            clear()
            blacksmith(self.ctx)
        if selection == '3':
            clear()
            char_menu(self.ctx)
        return town(self.ctx)


class LeaveTown(State):
    def do(self) -> Optional['State']:
        ctx = self.ctx

        ctx.ui.print('You will brave the wilds for 5 days.')
        input('Press enter to continue')
        return adventuring(self.ctx)


# Tavern #
class tavern(State):
    def do(self) -> Optional['State']:
        ctx = self.ctx

        clear()
        ctx.ui.print('######################')
        ctx.ui.print('Gold: ' + str(ctx.gold) + '/' + str(ctx.max_gold) + '')
        ctx.ui.print('HP: ' + str(ctx.hp) + '/' + str(ctx.max_hp) + '')
        ctx.ui.print('Food: ' + str(ctx.food) + '/' + str(ctx.max_food) + '')
        ctx.ui.print('######################\n')
        ctx.ui.print('"Welcome to the ' + ctx.location + ' Inn. How may I serve you?"\n')
        ctx.ui.print('1 Rest (1 gold)\n2 Buy Food (5 gold)\n3 Sell Food (3 gold)\n4 Speak with random patron\n5 Back')
        selection = input('>: ')
        if selection == '1':
            if ctx.gold < 1:
                ctx.ui.print('You cannot afford a bed here.')
                input('Press enter to continue.')
            else:
                ctx.ui.print('You slept like a rock.')
                ctx.hp = ctx.hp + 99999
                hp_mechanic(self.ctx)
                ctx.gold = ctx.gold - 1
                input('Press enter to continue.')
            return tavern(self.ctx)

        if selection == '2':
            ctx.ui.print('How much food do you want to buy?')
            ctx.food_price = 5
            n = input('>: ')
            if n == '0':
                return tavern(self.ctx)
            n = int(n)
            total_cost = n * ctx.food_price
            if total_cost > ctx.gold:
                ctx.ui.print('You do not have enough gold to buy ' + str(n) + ' food.')
                input('Press enter to continue')
                return tavern(self.ctx)
            elif total_cost <= ctx.gold:
                ctx.food = ctx.food + n
                food_mechanic(self.ctx)
                ctx.gold = ctx.gold - total_cost
                ctx.ui.print('You complete the transaction')
                input('Press enter to continue')
                return tavern(self.ctx)
        if selection == '3':
            ctx.ui.print('How much food do you want to sell?')
            ctx.food_sell = 3
            n = input('>: ')
            if n == '0':
                return tavern(self.ctx)
            n = int(n)
            total_sell = n * ctx.food_sell
            if ctx.food < n:
                ctx.ui.print('You do not have that much food.')
                input('Press enter to continue')
                return blacksmith(self.ctx)
            if ctx.food >= n:
                ctx.food = ctx.food - n
                ctx.gold = ctx.gold + total_sell
                ctx.ui.print('You complete the transaction')
                gold_mechanic(self.ctx)
                input('Press enter to continue')
                clear()
                return tavern(self.ctx)
        if selection == '4':
            return talk(self.ctx)
        if selection == '5':
            return town(self.ctx)
        else:
            return tavern(self.ctx)


# Talk #
class talk(State):
    def do(self) -> Optional['State']:
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
        input('Press enter to continue')
        return tavern(self.ctx)


# Blacksmith #
class blacksmith(State):
    def do(self) -> Optional['State']:
        ctx = self.ctx

        clear()
        ctx.ui.print('######################')
        ctx.ui.print('Gold: ' + str(ctx.gold) + '/' + str(ctx.max_gold) + '')
        ctx.ui.print('Arrows: ' + str(ctx.arrows) + '/' + str(ctx.max_arrows) + '')
        ctx.ui.print('Martial Prowess: ' + str(ctx.martial_prowess) + '')
        ctx.ui.print('######################\n')
        ctx.ui.print('"What can I do for you, traveler?"')
        ctx.ui.print('1 Upgrade your ' + ctx.weapon + ' (' + str(
            ctx.blacksmith_price) + ') gold.\n2 Buy Arrows (5 gold)\n3 Sell Arrows (3 gold) \n4 Back')
        selection = input('>: ')
        if selection == '1':
            if ctx.gold < ctx.blacksmith_price:
                ctx.ui.print('You do not have enough gold to upgrade your ' + ctx.weapon_type + '.')
                input('Press enter to continue')
            else:
                ctx.gold = ctx.gold - ctx.blacksmith_price
                gold_mechanic(self.ctx)
                v = random.randint(10, 30)
                ctx.martial_prowess = ctx.martial_prowess + v
                ctx.ui.print('Your martial prowess increases by ' + str(v) + '.')
                input('Press enter to continue')
            return blacksmith(self.ctx)
        if selection == '2':
            ctx.ui.print('How many arrows do you want to buy?')
            arrow_price = 5
            n = input('>: ')
            n = int(n)
            total_cost = n * arrow_price
            if total_cost > ctx.gold:
                ctx.ui.print('You do not have enough gold to buy ' + str(n) + ' arrows.')
                input('Press enter to continue')
                blacksmith(self.ctx)
            if total_cost <= ctx.gold:
                ctx.arrows = ctx.arrows + n
                arrows_mechanic(self.ctx)
                ctx.gold = ctx.gold - total_cost
                ctx.ui.print('You complete the transaction')
                input('Press enter to continue')
                blacksmith(self.ctx)
        if selection == '3':
            ctx.ui.print('How many arrows do you want to sell?')
            arrow_sell = 3
            n = input('>: ')
            n = int(n)
            total_sell = n * arrow_sell
            if ctx.arrows < n:
                ctx.ui.print('You do not have that many arrows.')
                input('Press enter to continue')
                blacksmith(self.ctx)
            if ctx.arrows >= n:
                ctx.arrows = ctx.arrows - n
                ctx.gold = ctx.gold + total_sell
                ctx.ui.print('You complete the transaction')
                gold_mechanic(self.ctx)
                input('Press enter to continue')
                clear()
                blacksmith(self.ctx)

        if selection == '4':
            return town(self.ctx)
        else:
            return blacksmith(self.ctx)


# Blacksmith Price Generator #
def blacksmith_price_generator(ctx: Context):
    ctx.blacksmith_price = random.randint(51, 75)
    if ctx.location == 'Rodez':
        ctx.blacksmith_price = ctx.blacksmith_price + 25
    if ctx.location == 'Oristano':
        ctx.blacksmith_price = ctx.blacksmith_price + 45
    if ctx.location == 'Thasos':
        ctx.blacksmith_price = ctx.blacksmith_price + 65
    if ctx.location == 'Karabuk':
        ctx.blacksmith_price = ctx.blacksmith_price + 85
    if ctx.location == 'Last Refuge':
        ctx.blacksmith_price = ctx.blacksmith_price + 105


# Adventuring #
class adventuring(State):
    def do(self) -> Optional['State']:
        ctx = self.ctx

        if ctx.counter != 0:
            ctx.adventure_state = True
            if ctx.hp > 0:
                adventure_menu(self.ctx)
                ctx.ui.print('1 Continue\n2 Hunt\n3 Rest\n4 Map\n')
                selection = input('>: ')
                clear()
                if selection == '1':
                    food_endurance_mechanic(ctx)
                    adventure_menu(ctx)
                    ctx.counter = ctx.counter - 1

                    return random_event(ctx, adventuring)
                if selection == '2':
                    return hunt(self.ctx, adventuring)
                if selection == '3':
                    return rest(self.ctx, adventuring)
                if selection == '4':
                    return the_map(self.ctx, adventuring)
                else:
                    return adventuring(self.ctx)
            else:
                return death(self.ctx)

        return EndAdventure(self.ctx)


class EndAdventure(State):
    def do(self) -> Optional['State']:
        ctx = self.ctx

        ctx.counter = 0
        clear()
        adventure_menu(self.ctx)
        ctx.ui.print('You have survived the trip.')
        ctx.adventure_state = False
        ctx.ui.print('Enter 0 to continue.')
        selection = input('>: ')
        if selection == '0':
            return location_changer(self.ctx)
        else:
            return adventuring(self.ctx)  # was location_changer()


# Rest #
class rest(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        x = random.randint(15, 25)
        food_endurance_mechanic(self.ctx)

        if ctx.hp == ctx.max_hp:
            ctx.ui.print('You rest for one day. Your HP is already maxed out.')

            input('Press enter to continue')
            return adventuring(self.ctx)

        ctx.ui.print('You rest for one day, gaining ' + str(x) + ' HP.')
        ctx.hp = ctx.hp + x
        hp_mechanic(self.ctx)

        input('Press enter to continue')


# Hunt #
class hunt(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        x = random.randint(1, 10)
        y = random.randint(1, 25)

        if ctx.arrows == 0:
            ctx.ui.print('You do not have any arrows to hunt with.')
            input('Press enter to continue')
            return adventuring(self.ctx)

        elif ctx.arrows < x:
            adventure_menu(self.ctx)
            x = ctx.arrows
            ctx.arrows = ctx.arrows - x
            ctx.food = ctx.food + y
            arrows_mechanic(self.ctx)
            ctx.ui.print('You shot ' + str(x) + ' arrows, and gained ' + str(y) + ' food.')
            food_mechanic(self.ctx)

        else:
            adventure_menu(self.ctx)
            ctx.arrows = ctx.arrows - x
            ctx.food = ctx.food + y
            arrows_mechanic(self.ctx)
            food_mechanic(self.ctx)
            ctx.ui.print('You shot ' + str(x) + ' arrows, and gained ' + str(y) + ' food.')

        input('Press enter to continue')

        return None


#
# Random Events #
#
class random_event(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        n = random.randint(1, 20)
        if n == 1:
            return chest(ctx, self.default)
        if n == 2:
            return fight(ctx, self.default)
        if n == 3:
            return robbed(ctx, self.default)
        if n == 4:
            return traveller(ctx, self.default)
        if n == 5:
            return damaged(ctx, self.default)
        if n == 6:
            return miracle(ctx, self.default)
        if n == 7:
            return mushroom(ctx, self.default)
        if n == 8:
            return nothing(ctx, self.default)
        if n == 9:
            return fight(ctx, self.default)
        if n == 10:
            return fight(ctx, self.default)
        if n == 11:
            return chest(ctx, self.default)
        if n == 12:
            return fight(ctx, self.default)
        if n == 13:
            return robbed(ctx, self.default)
        if n == 14:
            return traveller(ctx, self.default)
        if n == 15:
            return damaged(ctx, self.default)
        if n == 16:
            return mystic(ctx, self.default)
        if n == 17:
            return bigger_bag(ctx, self.default)
        if n == 18:
            return lose_day(ctx, self.default)
        if n == 19:
            return fight(ctx, self.default)
        if n == 20:
            return fight(ctx, self.default)


# Mushroom #
class mushroom(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        ctx.ui.print('You see a strange mushroom.')
        ctx.ui.print('1 Consume\n2 Leave')
        selection = input('>: ')
        if selection == '1':
            x = random.randint(1, 4)
            if x == 1:
                if ctx.race == 'Satyr':
                    w = ctx.consumption_rate + ctx.consumption_rate + ctx.consumption_rate
                    ctx.consumption_rate = ctx.consumption_rate + w
                    ctx.ui.print('You eat the mushroom, and gain ' + str(w) + ' Endurance.')
                else:
                    ctx.ui.print('You eat the mushroom, and nothing happened.')
            if x == 2:
                if ctx.race == 'Satyr':
                    w = ctx.consumption_rate + ctx.consumption_rate + ctx.consumption_rate
                    ctx.consumption_rate = ctx.consumption_rate + w
                    ctx.ui.print('You eat the mushroom, and gain ' + str(w) + ' Endurance.')
                else:
                    ctx.ui.print('You eat the mushroom, and it causes you to vomit.')
                    food_endurance_mechanic(self.ctx)
            if x == 3:
                w = ctx.consumption_rate + ctx.consumption_rate
                ctx.consumption_rate = ctx.consumption_rate + w
                ctx.ui.print('You eat the mushroom, and gain ' + str(w) + ' Endurance.')
            if x == 4:
                if ctx.race == 'Satyr':
                    w = ctx.consumption_rate + ctx.consumption_rate
                    ctx.consumption_rate = ctx.consumption_rate + w
                    ctx.ui.print('You eat the mushroom, and gain ' + str(w) + ' Endurance.')
                else:
                    ctx.hp = 0
                    ctx.endurance = 0
                    ctx.ui.print('You eat the mushroom, and then fall to the ground, foaming at the mouth.')
                    input('Press enter to continue')
                    return death(self.ctx)

        elif selection == '2':
            ctx.ui.print('You leave the mushroom.')
        else:
            return mushroom(self.ctx, self.default)
        input('Press enter to continue')


# Miracle #
class miracle(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        if ctx.race == 'Halfling':
            ctx.ui.print('You see an old wizard, and the wizard beckons you over.')
            ctx.ui.print('"Ho, there, traveler!"')
            ctx.ui.print('"I did not expect to see a Halfing out in the wilderness."')
            ctx.ui.print('"This is delightful. Here, have a gift."')
            ctx.ui.print('Fill:\n1 Food\n2 Arrows\n3 Gold\n4 HP')
            selection = input('>: ')
            if selection == '1':
                ctx.food = ctx.max_food
                food_mechanic(self.ctx)
            if selection == '2':
                ctx.arrows = ctx.max_arrows
                arrows_mechanic(self.ctx)
            if selection == '3':
                ctx.gold = ctx.max_gold
                gold_mechanic(self.ctx)
            if selection == '4':
                ctx.hp = ctx.max_hp
                hp_mechanic(self.ctx)
            input('Press enter to continue')
        else:
            return nothing(self.ctx, self.default)


# Bigger Bag #
class bigger_bag(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        y = random.randint(1, 3)
        if y == 1:
            ctx.max_food = ctx.max_food + 10
            ctx.ui.print(
                'You find an empty food storage container on the side of the path, and it holds more food than your current one.')
            input('Press enter to take\n')
            ctx.ui.print('Max food increased by 10.')
        if y == 2:
            ctx.max_arrows = ctx.max_arrows + 10
            ctx.ui.print('You spot an empty quiver on the side of the path. It holds more arrows than your current one.')
            input('Press enter to take\n')
            ctx.ui.print('Max arrows increased by 10.')
        if y == 3:
            ctx.max_gold = ctx.max_gold + 100
            ctx.ui.print('You discover an empty coin purse on the side of the path. It holds more gold than your current one.')
            input('Press enter to take\n')
            ctx.ui.print('Max gold increased by 100.')
        ctx.ui.print()
        input('Press enter to continue')

        return None


# Lose a Day #
class lose_day(TransientState):
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
        # ctx.ui.print('"If you want to cross this bridge, you have to pay us, ' + str(k) 'ctx.gold.\n')
        #        ctx.ui.print('1 Pay ctx.gold\n2 Take a detour\n')
        #        selection = input('>: ')
        #        if selection == '1':
        #            if k > ctx.gold:
        #            ctx.ui.print('"That is not enough to cross, but we will keep what you gave us, and you can find another way around. Have fun out there."')
        #            ctx.gold = 0
        #            else:
        #               ctx.gold = ctx.gold - k
        #               ctx.ui.print('You gave the bandit ' + str(k) + ' ctx.gold, and they let you cross the bridge.')
        #       elif selection == '2'
        #       else:
        #           selection = input('>: ')

        input('Press enter to continue')

        return None


# Mystic #
class mystic(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        ctx.ui.print('You come upon a roaming mystic.')
        ctx.ui.print('The mystic offers you a blessing.\n')
        ctx.ui.print('Increase:\n1 Max HP\n2 Endurance\n3 Martial Prowess\n')
        # ctx.ui.print('Fill: ')
        selection = input('>: ')
        clear()
        if selection == '1':
            ctx.max_hp = ctx.max_hp + 10
            ctx.hp = ctx.hp + 10
            ctx.ui.print('Your max HP increases by 10.')
            input('Press enter to continue')
        elif selection == '2':
            ctx.endurance = ctx.endurance + ctx.consumption_rate
            ctx.ui.print('Your endurance increases by ' + str(ctx.consumption_rate) + '.')
            input('Press enter to continue')
        elif selection == '3':
            ctx.martial_prowess = ctx.martial_prowess + 10
            ctx.ui.print('Your martial prowess increases by 10.')
            input('Press enter to continue')
        else:
            return mystic(self.ctx, self.default)


# Nothing #
class nothing(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        ctx.ui.print('Nothing notable happens.')
        input('Press enter to continue')

        return None


# Damaged (Random Event) #
class damaged(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        # adventure_menu()
        v = random.randint(1, 20)
        n = random.randint(1, 3)
        ctx.hp = ctx.hp - v
        hp_mechanic(self.ctx)
        if n == 1:
            g = random.randint(1, 20)
            ctx.gold = ctx.gold + g
            ctx.ui.print('You sprain your ankle in a divot, taking ' + str(v) + ' damage.')
            ctx.ui.print('However, you find ' + str(g) + ' gold on the ground.')
            gold_mechanic(self.ctx)
        if n == 2:
            f = random.randint(1, 20)
            ctx.food = ctx.food + f
            ctx.ui.print('You are stung by a swarm of bees, taking ' + str(v) + ' damage.')
            ctx.ui.print('However, you manage to take ' + str(f) + ' honey before you flee.')
            food_mechanic(self.ctx)

        if n == 3:
            a = random.randint(1, 20)
            ctx.arrows = ctx.arrows + a
            ctx.ui.print('You walk into an hunter\'s trap, taking ' + str(v) + ' damage.')
            ctx.ui.print('However, you find ' + str(a) + ' arrows nearby.')
            arrows_mechanic(self.ctx)

        input('Press enter to continue')

        return None


# Traveller #
class traveller(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        ctx.ui.print('A friendly adventurer approaches you and wants to trade.')
        n = random.randint(1, 3)
        if n == 1:
            ctx.ui.print('"Good morning, traveler."\n')
        if n == 2:
            ctx.ui.print('"Good evening, traveler."\n')
        if n == 3:
            ctx.ui.print('"Good afternoon, traveler."\n')

        traveller_values(self.ctx)

        return None


# Traveller Values #
def traveller_values(ctx: Context):
    traveller_generation(ctx)
    input('Press enter to continue')


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
            ctx.ui.print('1 Accept\n2 Decline')
            selection = input('>: ')
            if selection == '1':
                if ctx.food < x:
                    ctx.ui.print('You cannot afford the trade.')
                else:
                    ctx.food = ctx.food - x
                    ctx.arrows = ctx.arrows + v
                    ctx.ui.print('You accept the trade.')
                    arrows_mechanic(ctx)

            else:
                ctx.ui.print('You decline the trade.')

        if p == 2:
            ctx.ui.print('The trader is willing to pay ' + str(v) + ' gold.')
            ctx.ui.print('1 Accept\n2 Decline')
            selection = input('>: ')
            if selection == '1':
                if ctx.food < x:
                    ctx.ui.print('You cannot afford the trade.')
                else:
                    ctx.food = ctx.food - x
                    ctx.gold = ctx.gold + v
                    ctx.ui.print('You accept the trade.')
                    gold_mechanic(ctx)

            else:
                ctx.ui.print('You decline the trade.')

        if p == 3:
            ctx.ui.print('The trader is willing to heal you ' + str(v) + ' HP.')
            ctx.ui.print('1 Accept\n2 Decline')
            selection = input('>: ')
            if selection == '1':
                if ctx.food < x:
                    ctx.ui.print('You cannot afford the trade.')
                else:
                    ctx.food = ctx.food - x
                    ctx.hp = ctx.hp + v
                    ctx.ui.print('You accept the trade.')
                    hp_mechanic(ctx)

            else:
                ctx.ui.print('You decline the trade.')
    if c == 2:
        ctx.ui.print('The trader wants ' + str(x) + ' arrows.')
        p = random.randint(1, 3)  # what trader is giving
        if p == 1:
            ctx.ui.print('The trader is willing to give ' + str(v) + ' food.')
            ctx.ui.print('1 Accept\n2 Decline')
            selection = input('>: ')
            if selection == '1':
                if ctx.arrows < x:
                    ctx.ui.print('You cannot afford the trade.')
                else:
                    ctx.arrows = ctx.arrows - x
                    ctx.food = ctx.food + v
                    ctx.ui.print('You accept the trade.')
                    food_mechanic(ctx)

            else:
                ctx.ui.print('You decline the trade.')
        if p == 2:
            ctx.ui.print('The trader is willing to give ' + str(v) + ' gold.')
            ctx.ui.print('1 Accept\n2 Decline')
            selection = input('>: ')
            if selection == '1':
                if ctx.arrows < x:
                    ctx.ui.print('You cannot afford the trade.')
                else:
                    ctx.arrows = ctx.arrows - x
                    ctx.gold = ctx.gold + v
                    ctx.ui.print('You accept the trade.')
                    gold_mechanic(ctx)

            else:
                ctx.ui.print('You decline the trade.')
        if p == 3:
            ctx.ui.print('The trader is willing to heal you for ' + str(v) + ' HP.')
            ctx.ui.print('1 Accept\n2 Decline')
            selection = input('>: ')
            if selection == '1':
                if ctx.arrows < x:
                    ctx.ui.print('You cannot afford the trade.')
                else:
                    ctx.arrows = ctx.arrows - x
                    ctx.hp = ctx.hp + v
                    ctx.ui.print('You accept the trade.')
                    hp_mechanic(ctx)

            else:
                ctx.ui.print('You decline the trade.')
    if c == 3:
        ctx.ui.print('The trader wants ' + str(x) + ' gold.')
        p = random.randint(1, 3)  # what trader is giving
        if p == 1:
            ctx.ui.print('The trader is willing to give ' + str(v) + ' food.')
            ctx.ui.print('1 Accept\n2 Decline')
            selection = input('>: ')
            if selection == '1':
                if ctx.gold < x:
                    ctx.ui.print('You cannot afford the trade.')
                else:
                    ctx.gold = ctx.gold - x
                    ctx.food = ctx.food + v
                    ctx.ui.print('You accept the trade.')
                    food_mechanic(ctx)

            else:
                ctx.ui.print('You decline the trade.')
        if p == 2:
            ctx.ui.print('The trader is willing to give ' + str(v) + ' arrows.')
            ctx.ui.print('1 Accept\n2 Decline')
            selection = input('>: ')
            if selection == '1':
                if ctx.gold < x:
                    ctx.ui.print('You cannot afford the trade.')
                else:
                    ctx.gold = ctx.gold - x
                    ctx.arrows = ctx.arrows + v
                    ctx.ui.print('You accept the trade.')
                    arrows_mechanic(ctx)

            else:
                ctx.ui.print('You decline the trade.')

        if p == 3:
            ctx.ui.print('The trader is willing to heal you ' + str(v) + ' HP.')
            ctx.ui.print('1 Accept\n2 Decline')
            selection = input('>: ')
            if selection == '1':
                if ctx.gold < x:
                    ctx.ui.print('You cannot afford the trade.')
                else:
                    ctx.gold = ctx.gold - x
                    ctx.hp = ctx.hp + v
                    ctx.ui.print('You accept the trade.')
                    hp_mechanic(ctx)

            else:
                ctx.ui.print('You decline the trade.')
    if c == 4:
        ctx.ui.print('The trader wants your blood. Specifically, ' + str(x) + ' HP.')
        p = random.randint(1, 3)  # what trader is giving
        if p == 1:
            ctx.ui.print('The trader is willing to give ' + str(v) + ' food.')
            ctx.ui.print('1 Accept\n2 Decline')
            selection = input('>: ')
            if selection == '1':
                if ctx.hp < x:
                    ctx.ui.print('You cannot afford the trade, but the trader is willing to let you slide, this time.')
                    ctx.hp = ctx.hp - x
                    ctx.food = ctx.food + v
                    food_mechanic(ctx)
                else:
                    ctx.hp = ctx.hp - x
                    ctx.food = ctx.food + v
                    ctx.ui.print('You accept the trade.')
                    food_mechanic(ctx)

            else:
                ctx.ui.print('You decline the trade.')
        if p == 2:
            ctx.ui.print('The trader is willing to give ' + str(v) + ' arrows.')
            ctx.ui.print('1 Accept\n2 Decline')
            selection = input('>: ')
            if selection == '1':
                if ctx.hp < x:
                    ctx.ui.print('You cannot afford the trade, but the trader is willing to let you slide, this time.')
                    ctx.hp = ctx.hp - x
                    ctx.food = ctx.food + v
                    food_mechanic(ctx)
                else:
                    ctx.hp = ctx.hp - x
                    ctx.arrows = ctx.arrows + v
                    ctx.ui.print('You accept the trade.')
                    arrows_mechanic(ctx)

            else:
                ctx.ui.print('You decline the trade.')
        if p == 3:
            ctx.ui.print('The trader is willing to give ' + str(v) + ' gold.')
            ctx.ui.print('1 Accept\n2 Decline')
            selection = input('>: ')
            if selection == '1':
                if ctx.hp < x:
                    ctx.ui.print('You cannot afford the trade, but the trader is willing to let you slide, this time.')
                    ctx.hp = ctx.hp - x
                    ctx.food = ctx.food + v
                    food_mechanic(ctx)
                else:
                    ctx.hp = ctx.hp - x
                    ctx.gold = ctx.gold + v
                    ctx.ui.print('You accept the trade.')
                    gold_mechanic(ctx)

            else:
                ctx.ui.print('You decline the trade.')


# Robbed #
class robbed(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        x = random.randint(1, 3)
        if ctx.food == 0 and ctx.arrows == 0 and ctx.gold == 0:
            return nothing(self.ctx, self.default)
        elif x == 1:
            v = random.randint(1, 50)
            if ctx.food < v:
                v = ctx.food

            ctx.food = ctx.food - v
            food_mechanic(self.ctx)
            y = random.randint(1, 2)
            # adventure_menu()
            if y == 1:
                ctx.ui.print('During the night, a shadowy figure stole ' + str(v) + ' of your food.')
            elif y == 2:
                ctx.ui.print('You check your food supply and find that ' + str(v) + ' food is missing.')
        elif x == 2:
            v = random.randint(1, 50)
            if ctx.arrows < v:
                v = ctx.arrows
            ctx.arrows = ctx.arrows - v
            arrows_mechanic(self.ctx)
            y = random.randint(1, 2)
            # adventure_menu()
            if y == 1:
                ctx.ui.print('During the night, a shadowy figure stole ' + str(v) + ' of your arrows.')
            elif y == 2:
                ctx.ui.print('You check your arrow quill, and find that ' + str(v) + ' arrows are missing.')

        elif x == 3:
            v = random.randint(1, 50)
            if ctx.gold < v:
                v = ctx.gold
            ctx.gold = ctx.gold - v
            gold_mechanic(self.ctx)
            y = random.randint(1, 2)
            # adventure_menu()
            if y == 1:
                ctx.ui.print('During the night, a shadowy figure stole ' + str(v) + ' of your gold.')
            elif y == 2:
                ctx.ui.print('You check your coin purse, and find that ' + str(v) + ' gold is missing.')

        input('Press enter to continue')


# Doppelganger #
def doppelganger(ctx: Context):
    if ctx.enemy_type == 'Doppelganger':
        ctx.ui.print('The doppelganger is wielding a ' + ctx.weapon + ' exactly like yours.')


# Fight #
class fight(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        enemy_generator(ctx)
        ctx.ui.print('You see a ' + ctx.enemy_adjective + ' ' + ctx.enemy_type + ' approaching.')
        doppelganger(ctx)
        ctx.ui.print('1 Fight\n2 Flee')
        selection = input('>: ')
        if selection == '1':
            return fight_simulation(ctx)

        if selection == '2':
            return flee_fight(ctx)

        else:
            return flee_fight(ctx)


# Fight Simulation #
class fight_simulation(State):
    def do(self) -> Optional['State']:
        ctx = self.ctx

        your_damage_taken(ctx)
        enemy_loot(ctx)

        input('Press enter to continue')
        # adventure_menu()
        ctx.counter = ctx.counter - 1

        return adventuring(self.ctx)


# Enemy Loot #
def enemy_loot(ctx: Context):
    f = random.randint(1, 10)
    ctx.enemy_food = ctx.enemy_food + f
    ctx.food = ctx.food + ctx.enemy_food
    a = random.randint(1, 5)
    ctx.enemy_arrows = ctx.enemy_arrows + a
    ctx.arrows = ctx.arrows + ctx.enemy_arrows
    g = random.randint(1, 10)
    ctx.enemy_gold = ctx.enemy_gold + g
    ctx.gold = ctx.gold + ctx.enemy_gold
    ctx.ui.print('You found ' + str(ctx.enemy_food) + ' food, ' + str(ctx.enemy_arrows) + ' arrows, and ' + str(
        ctx.enemy_gold) + ' gold on the corpse.')
    food_mechanic(ctx)
    arrows_mechanic(ctx)
    gold_mechanic(ctx)


# Your Damage Taken #
def your_damage_taken(ctx: Context):
    ctx.damage_taken = ctx.enemy_battle_score - ctx.martial_prowess
    ctx.hp = int(ctx.hp - ctx.damage_taken)
    if ctx.damage_taken < 1:
        ctx.hp = ctx.hp + ctx.damage_taken
        ctx.damage_taken = 0
        ctx.ui.print('The enemy was slain, and you took no damage.')
    else:
        ctx.ui.print('The enemy was slain, but you took ' + str(ctx.damage_taken) + ' damage.')


# Flee Fight #
class flee_fight(State):
    def do(self) -> Optional['State']:
        ctx = self.ctx

        n = random.randint(1, 2)
        if n == 1:
            ctx.ui.print('You escaped the fight.')
            input('Press enter to continue')
            adventure_menu(ctx)
        elif n == 2:
            ctx.ui.print('You failed to flee the fight.')
            input('Press enter to continue')
            return fight_simulation(self.ctx)

        ctx.counter = ctx.counter - 1
        return adventuring(self.ctx)


# Enemy Generator #
def enemy_generator(ctx: Context):
    enemy_resetter(ctx)
    enemy_adjective_generator(ctx)
    enemy_type_generator(ctx)


# Enemy Resetter #
def enemy_resetter(ctx: Context):
    ctx.enemy_type = ''
    ctx.enemy_food = 0
    ctx.enemy_arrows = 0
    ctx.enemy_gold = 0
    ctx.enemy_specific_gold = 0
    ctx.enemy_specific_arrows = 0
    ctx.enemy_specific_food = 0
    ctx.enemy_battle_score = 0
    ctx.enemy_adjective = ''


# Enemy Locator and Excluder Generator #
def enemy_locator_generator(ctx: Context):
    if ctx.location == 'Goodshire':
        ctx.enemy_locator = 'Goodshire'
        ctx.enemy_exclude = [3, 4, 5]
    if ctx.location == 'Rodez':
        ctx.enemy_locator = 'Rodez'
        ctx.enemy_exclude = [2, 4, 5]
    if ctx.location == 'Oristano':
        ctx.enemy_locator = 'Oristano'
        ctx.enemy_exclude = [1, 2, 5]
    if ctx.location == 'Thasos':
        ctx.enemy_locator = 'Thasos'
        ctx.enemy_exclude = [1, 2]
    if ctx.location == 'Karabuk':
        ctx.enemy_locator = 'Karabuk'
        ctx.enemy_exclude = [1, 2, 3]
    if ctx.location == 'Last Refuge':
        ctx.enemy_locator = 'Last Refuge'
        ctx.enemy_exclude = [2, 3]
    ctx.enemy_number = random.randint(1, 5)
    while ctx.enemy_number in ctx.enemy_exclude:
        ctx.enemy_number = random.randint(1, 5)


# Enemy Type Generator #
def enemy_type_generator(ctx: Context):
    enemy_locator_generator(ctx)

    if ctx.enemy_number == 1:
        ctx.enemy_type = 'Lone Wolf'
        ctx.enemy_battle_score = ctx.enemy_battle_score + 35
        ctx.enemy_specific_food = 2
        ctx.enemy_specific_arrows = 0
        ctx.enemy_specific_gold = 0
        ctx.enemy_food = ctx.enemy_food + ctx.enemy_specific_food
        ctx.enemy_arrows = ctx.enemy_arrows + ctx.enemy_specific_arrows
        ctx.enemy_gold = ctx.enemy_gold + ctx.enemy_specific_gold

    if ctx.enemy_number == 2:
        ctx.enemy_type = 'Large Maggot'
        ctx.enemy_battle_score = ctx.enemy_battle_score + 15
        ctx.enemy_specific_food = 1
        ctx.enemy_specific_arrows = 0
        ctx.enemy_specific_gold = 0
        ctx.enemy_food = ctx.enemy_food + ctx.enemy_specific_food
        ctx.enemy_arrows = ctx.enemy_arrows + ctx.enemy_specific_arrows
        ctx.enemy_gold = ctx.enemy_gold + ctx.enemy_specific_gold

    if ctx.enemy_number == 3:
        ctx.enemy_type = 'Rogue Vampire'
        ctx.enemy_battle_score = ctx.enemy_battle_score + 55
        ctx.enemy_specific_food = 0
        ctx.enemy_specific_arrows = 0
        ctx.enemy_specific_gold = 5
        ctx.enemy_food = ctx.enemy_food + ctx.enemy_specific_food
        ctx.enemy_arrows = ctx.enemy_arrows + ctx.enemy_specific_arrows
        ctx.enemy_gold = ctx.enemy_gold + ctx.enemy_specific_gold

    if ctx.enemy_number == 4:
        ctx.enemy_type = 'Dark Cultist'
        ctx.enemy_battle_score = ctx.enemy_battle_score + 85
        ctx.enemy_specific_food = 10
        ctx.enemy_specific_arrows = 0
        ctx.enemy_specific_gold = 10
        ctx.enemy_food = ctx.enemy_food + ctx.enemy_specific_food
        ctx.enemy_arrows = ctx.enemy_arrows + ctx.enemy_specific_arrows
        ctx.enemy_gold = ctx.enemy_gold + ctx.enemy_specific_gold

    if ctx.enemy_number == 5:
        ctx.enemy_type = 'Doppelganger'
        ctx.enemy_battle_score = ctx.enemy_battle_score + 105
        ctx.enemy_specific_food = 10
        ctx.enemy_specific_arrows = 0
        ctx.enemy_specific_gold = 10
        ctx.enemy_food = ctx.enemy_food + ctx.enemy_specific_food
        ctx.enemy_arrows = ctx.enemy_arrows + ctx.enemy_specific_arrows
        ctx.enemy_gold = ctx.enemy_gold + ctx.enemy_specific_gold

    # Enemy Adjective Generator #


def enemy_adjective_generator(ctx: Context):
    j = random.randint(1, 3)
    if j == 1:
        ctx.enemy_adjective = 'Bloodthirsty'
        ctx.enemy_battle_score = ctx.enemy_battle_score + 35
    if j == 2:
        ctx.enemy_adjective = 'Regular'
        ctx.enemy_battle_score = ctx.enemy_battle_score + 0
    if j == 3:
        ctx.enemy_adjective = 'Starved'
        ctx.enemy_battle_score = ctx.enemy_battle_score - 10


# Chest #
class chest(TransientState):
    def _do(self) -> Optional[State]:
        ctx = self.ctx

        p = random.randint(1, 2)
        if p == 1:
            ctx.ui.print('You see a treasure chest.')
        if p == 2:
            ctx.ui.print('You see a large hollow tree.')
        ctx.ui.print('1 Inspect\n2 Avoid')
        selection = input('>: ')
        if selection == '1':
            a = random.randint(1, 3)
            if a == 1:
                ctx.ui.print('It is empty. Nothing but cobwebs remain.')
                input('Press enter to continue')
                adventure_menu(self.ctx)
            if a == 2:
                ctx.ui.print('It was booby trapped. A dart flies out and hits you for 20 damage.')
                ctx.hp = ctx.hp - 20
                input('Press enter to continue')
                hp_mechanic(self.ctx)
                adventure_menu(self.ctx)
            # if a == 2 and ctx.luck > 0:
            # ctx.ui.print('It was booby trapped. A dart flies out and hits you for 20 damage.')
            # chest_loot()
            if a == 3:
                return chest_loot(self.ctx)

        elif selection == '2':
            ctx.ui.print()

        else:
            return chest(self.ctx, self.default)


# Chest Loot #
class chest_loot(State):
    def do(self) -> Optional['State']:
        ctx = self.ctx

        x = random.randint(1, 3)
        if x == 1:
            v = random.randint(50, 100)
            ctx.food = ctx.food + v
            ctx.ui.print('Inside, you found ' + str(v) + ' food.')
            food_mechanic(ctx)
        if x == 2:
            v = random.randint(50, 100)
            ctx.arrows = ctx.arrows + v
            ctx.ui.print('Inside, you found ' + str(v) + ' arrows.')
            arrows_mechanic(ctx)
        if x == 3:
            v = random.randint(50, 100)
            ctx.gold = ctx.gold + v
            ctx.ui.print('Inside, you found ' + str(v) + ' gold.')
            gold_mechanic(ctx)

        input('Press enter to continue')
        return adventure_menu(self.ctx)


# Salem #
class salem(State):
    def do(self) -> Optional['State']:
        ctx = self.ctx

        clear()
        ctx.ui.print('-----------------')
        ctx.ui.print('| G |   |   |   |')
        ctx.ui.print('+---+---+---+---+')
        ctx.ui.print('| R |   |   |   |')
        ctx.ui.print('+---+---+---+---+')
        ctx.ui.print('|   | O |   |   |')
        ctx.ui.print('+---+---+---+---+')
        ctx.ui.print('|   | T | K |   |')
        ctx.ui.print('+---+---+---+---+')
        ctx.ui.print('|   |   |   | S |')
        ctx.ui.print('+---------------+\n')
        ctx.ui.print('Salem\n')
        input('Press enter to continue')
        clear()

        ctx.ui.print(
            'You enter the ancient city of Salem, now blackened with fire and as silent as a graveyard, and see a man who looks like a commoner lounging upon a throne of skeletons in the courtyard.')
        ctx.ui.print('"Ah, ' + ctx.name + '", I was expecting you."\n')
        ctx.ui.print('Type \'who are you?\'')
        input('>: ')

        clear()
        ctx.ui.print('"I am the called by your order the Antipope or the Prince of Darkness, but my birth name is Chernobog."')
        ctx.ui.print(
            '"As you can see, I have already razed Salem. Your sacred temples and artifacts are totally destroyed. You have failed."')
        ctx.ui.print('"But I admire your willpower and resourcefulness to make it all the way here from Goodshire."')
        ctx.ui.print('"I want to make you an offer. Join me, and become my champion. Together, we will forge a New Dawn."')
        ctx.ui.print('"Your old ways are gone. You have failed your order, and they will no longer accept you."')
        ctx.ui.print(
            '"If you decline, I won\'t kill you, but I will beat you within an inch of your life and enslave you for eternity."\n')
        ctx.ui.print('"The choice is yours, ' + ctx.name + '."\n')
        ctx.ui.print('1 Accept offer\n2 Decline offer\n')
        selection = input('>: ')
        clear()

        if selection == '1':
            char_menu(ctx)
            ctx.ui.print(
                'You join the forces of Chernobog, the Prince of Darkness, and forsake your old way of life. You both combine your powers and forge a New Dawn.')
            ctx.ui.print()
            input('Press enter to end game')
            return title_screen(self.ctx)

        elif selection == '2':
            ctx.ui.print('"Very well, then." Chernobog stands up.')
            input('Press enter to fight')

            ctx.enemy_battle_score = 170
            ctx.damage_taken = ctx.enemy_battle_score - ctx.martial_prowess
            ctx.hp = int(ctx.hp - ctx.damage_taken)
            if ctx.hp > 0:
                ctx.ui.print('You have slain the Antipope. His body magically lights on fire, and leaves ashes on the ground.')
                ctx.ui.print(
                    'Your surroundings shimmer, and the city of Salem transforms from its ruined state to its former glory. You have succeeded in every goal.')
                input('Press enter to continue')
                char_menu(ctx)
                clear()
                ctx.ui.print('You win!')

                ctx.ui.print('Occupation: ' + ctx.occupation + '')
                input('Press enter to end game')
                return title_screen(self.ctx)

            else:
                ctx.hp = 0.1
                char_menu(ctx)
                ctx.ui.print()
                ctx.ui.print('You have lost the fight, letting Chernobog win. He enslaves you for all eternity, and he takes over the world.\n')
                input('Press enter to end game')
                return title_screen(self.ctx)

        else:
            return salem(self.ctx)


global_context.run(title_screen(global_context))
