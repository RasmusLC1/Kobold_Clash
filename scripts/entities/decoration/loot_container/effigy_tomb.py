from scripts.entities.decoration.loot_container.loot_container import Loot_Container
from scripts.engine.keys.keys import keys
import random


class Effigy_Tomb(Loot_Container):
    def __init__(self, game, pos) -> None:
        self.enemies = {}
        super().__init__(game, keys.effigy_tomb, pos, False, 99, (32, 64))
        self.animation_max = 1

    def Open(self):
        if not super().Open():
            return False
        
        self.Generate_Sound('tomb_lid', 0.3, 500)

        self.Set_Animation(1)
        return True

    def Drop_Loot(self):
        loot_types = list(self.loot_weights.keys())
        weight_values = [self.loot_weights[loot_type] for loot_type in loot_types]
        loot_type = random.choices(loot_types, weight_values, k=1)[0]
        if loot_type == keys.enemy:
            enemy_type = random.choices(
                population=list(self.enemies.keys()),
                weights=list(self.enemies.values()),
                k=1
            )[0]
            self.game.enemy_handler.Enemy_Spawner(self.Get_Pos(), enemy_type)
            return
        else:
            self.Spawn_Loot(loot_type, self.Get_Pos())



    def Set_Loot_Types(self):
        self.loot_weights = {keys.enemy : 0.5,
                             keys.revive : 0.2,
                             keys.curse : 0.3}
        
        self.enemies = {
            keys.wight_king : 0.1,
            keys.skeleton_bell_toller : 0.2,
            keys.skeleton_warrior : 0.5,
            keys.skeleton_undertaker : 0.2,
            keys.skeleton_cleric : 0.1,
        }