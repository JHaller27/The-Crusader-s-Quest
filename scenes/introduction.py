from typing import Optional
import yaml

from state import State
from utils import ui

from scenes import Town


with open("./data/player_options.yml", "r") as fp:
    player_options_config = yaml.safe_load(fp)


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


# Start Game #
class StartGame(State):
    def do(self) -> Optional[State]:
        return Town(self.ctx)
