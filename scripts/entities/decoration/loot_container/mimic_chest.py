from scripts.entities.decoration.loot_container.loot_container import Loot_Container
from scripts.engine.keys.keys import keys
import random


class Mimic_Chest(Loot_Container):
    def __init__(self, game, pos, version) -> None:
        super().__init__(game, keys.chest, pos, True, 5)
        self.version = version

    def Save_Data(self):
        super().Save_Data()
        self.saved_data['version'] = self.version
        

    def Load_Data(self, data):
        super().Load_Data(data)
        self.version = data['version']

    def Open(self):
        if not super().Open():
            return False
        
        self.game.decoration_handler.Remove_Decoration(self)

        self.Generate_Sound('chest_open', 0.1, 500)


    def Drop_Loot(self):
        enemy_type = random.choices(
            population=list(self.enemies.keys()),
            weights=list(self.enemies.values()),
            k=1
        )[0]
        self.game.enemy_handler.Enemy_Spawner(self.Get_Pos(), enemy_type)
        self.game.player.Set_Effect(keys.slow, 4)


    def Set_Loot_Types(self):
        self.loot_weights = {}
        
        self.enemies = {
            keys.skeleton_bell_toller : 0.2,
            keys.skeleton_warrior : 0.5,
            keys.skeleton_guardian : 0.2,
            keys.skeleton_undertaker : 0.2,
            keys.skeleton_cleric : 0.1,
        }