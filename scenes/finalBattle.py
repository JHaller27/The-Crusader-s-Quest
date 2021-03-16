from typing import Optional

from state import State
from utils.ui import ui
import utils.enemy as enemy

import scenes.introduction as introduction


# Final Battle #
class FinalBattle(State):
    def do(self) -> Optional[State]:
        ctx = self.ctx

        ui.clear()
        ui.display_map(ctx.map)
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
            self.ctx.char_menu()
            ui.print("You join the forces of Chernobog, the Prince of Darkness, and forsake your old way of life. You both combine your powers and forge a New Dawn.")
            ui.print()
            ui.wait("end game")

        else:
            ui.print('"Very well, then." Chernobog stands up.')
            ui.wait("fight")

            ctx.enemy = enemy.Enemy(self.ctx.enemy_config.final)
            damage_taken = ctx.combat_damage()
            ctx.player.hp -= damage_taken

            if ctx.player.is_alive():
                ui.print("You have slain the Antipope. His body magically lights on fire, and leaves ashes on the ground.")
                ui.print("Your surroundings shimmer, and the city of Salem transforms from its ruined state to its former glory. You have succeeded in every goal.")
                ui.wait()

                self.ctx.char_menu()
                ui.clear()
                ui.print("You win!")

                ui.print(f"Occupation: {ctx.player.occupation}")

            else:
                self.ctx.char_menu()
                ui.print()
                ui.print("You have lost the fight, letting Chernobog win. He enslaves you for all eternity, and he takes over the world.\n")

            ui.wait("end game")

        return introduction.TitleScreen(self.ctx)
