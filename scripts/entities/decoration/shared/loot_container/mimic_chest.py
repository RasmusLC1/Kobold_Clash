from scripts.entities.decoration.shared.loot_container.chest import Chest
from scripts.engine.keys.keys import keys
from scripts.entities.decoration.shared.shared_registry import Register_Decoration
import random


@Register_Decoration(keys.mimic_chest)
class Mimic_Chest(Chest):

    def Drop_Loot(self):
        enemy_type = random.choices(
            population=list(self.enemies.keys()),
            weights=list(self.enemies.values()),
            k=1
        )[0]
        self.game.enemy_handler.Enemy_Spawner(self.Get_Pos(), enemy_type)
        self.game.player.Set_Effect(keys.slow, 4)


    def Get_Loot_Types(self):
        self.loot_weights = {}
        
        self.enemies = {
            keys.skeleton_bell_toller : 0.2,
            keys.skeleton_warrior : 0.5,
            keys.skeleton_guardian : 0.2,
            keys.skeleton_undertaker : 0.2,
            keys.skeleton_cleric : 0.1,
        }