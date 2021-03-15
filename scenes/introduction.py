from typing import Optional

from state import State
from utils import ui

from scenes import Town


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

        races = self.ctx.player_config.races

        selection = ui.choose([r.name for r in races]) - 1
        selected_race = races[selection]

        player.race = selected_race.name
        player.max_hp = selected_race.hp
        player.hp = selected_race.hp
        player.martial_prowess = selected_race.martial_prowess
        player.consumption_rate = selected_race.consumption_rate
        player.endurance = selected_race.endurance
        player.max_gold = player.gold = selected_race.gold
        player.luck = selected_race.luck
        player.speed = selected_race.speed

        return SetOccupation(self.ctx)


class SetOccupation(State):
    def do(self) -> Optional[State]:
        player = self.ctx.player

        ui.clear()
        ui.print("What is your occupation?\n")

        occupations = self.ctx.player_config.occupations

        selection = ui.choose([o.name for o in occupations]) - 1
        selected_occupation = occupations[selection]

        player.occupation = selected_occupation.name
        player.max_hp += selected_occupation.hp
        player.hp += selected_occupation.hp
        player.max_food += selected_occupation.max_food
        player.food += selected_occupation.food
        player.max_arrows += selected_occupation.max_arrows
        player.arrows += selected_occupation.arrows
        player.max_gold += selected_occupation.max_gold
        player.gold += selected_occupation.gold
        player.martial_prowess += selected_occupation.martial_prowess

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


# Start Game #
class StartGame(State):
    def do(self) -> Optional[State]:
        return Town(self.ctx)
