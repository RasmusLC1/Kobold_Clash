from scripts.entities.decoration.shared.loot_container.loot_container import Loot_Container
from scripts.engine.keys.keys import keys
from scripts.entities.decoration.ancient_tomb.ancient_tomb_registry import Register_Decoration
import random

@Register_Decoration(keys.blood_shrine)
class Effigy_Tomb(Loot_Container):
    def __init__(self, game, pos) -> None:
        self.enemies = {}
        super().__init__(game, keys.effigy_tomb, pos, (32, 64))
        self.animation_max = 1

    def Open(self):
        if not super().Open():
            return False
        
        self.Generate_Sound(keys.tomb_lid, 0.3, 500)

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
            rarity_value = self.Calculate_Rarity()
            self.Spawn_Loot(loot_type, self.Get_Pos(), rarity_value)



    def Set_Loot_Types(self):
        self.loot_weights = {keys.enemy : 0.5,
                             keys.revive : 0.2,
                             keys.curse : 0.3}
        
        self.enemies = {
            keys.vampire : 0.01,
            keys.skeleton_bell_toller : 0.2,
            keys.skeleton_warrior : 0.5,
            keys.skeleton_guardian : 0.2,
            keys.skeleton_undertaker : 0.2,
            keys.skeleton_cleric : 0.1,
        }

    def Set_Loot_To_Always_Spawn_Enemy(self):
        self.loot_weights = {keys.enemy : 100}