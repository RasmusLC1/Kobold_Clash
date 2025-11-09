import random
from scripts.entities.decoration.decoration import Decoration
from scripts.engine.keys.keys import keys


class Loot_Container(Decoration):
    def __init__(self, game, type, pos, size = (32, 32), destructable = False, health = 100, destruction_sound = None, destruction_clatter = 500) -> None:
        super().__init__(game, type, pos, size, destructable, health, destruction_sound, destruction_clatter)
        self.loot_type = 0
        self.empty = False
        self.loot_amount = 0
        self.text_cooldown = 0
        self.text_animation = 0
        self.loot_weights = {}
        self.Set_Loot_Types()
        self.rarity_value = self.Calculate_Rarity_Value()
        self.sub_category = keys.loot_container

    def Save_Data(self):
        super().Save_Data()
        self.saved_data['empty'] = self.empty
        

    def Load_Data(self, data):
        super().Load_Data(data)
        self.empty = data['empty']

    def Open(self):
        if self.empty:
            return False
        
        self.Drop_Loot()
        self.empty = True
        self.game.item_handler.Reset_Nearby_Items_Cooldown()
        
        return True

    def Drop_Loot(self):
        loot_types = list(self.loot_weights.keys())
        weight_values = [self.loot_weights[loot_type] for loot_type in loot_types]
        loot_type = random.choices(loot_types, weight_values, k=1)[0]

        if loot_type == keys.nothing:
            return
        
        self.Spawn_Loot(loot_type, self.Get_Pos())
    
    def Get_Pos(self):
        rand_pos_x = self.pos[0] + random.randint(-100, 100)/10
        rand_pos_y = self.pos[1] + random.randint(-100, 100)/10
        return (rand_pos_x, rand_pos_y)


    def Calculate_Rarity_Value(self):
        base = random.uniform(0.8, 1.2)
        depth_factor = self.game.depth * 1.5
        luck_factor = self.game.player.luck * 2
        clatter_factor = self.game.clatter.Get_Awakening_Level() * 2.5

        rarity_value = (base + depth_factor + luck_factor + clatter_factor)

        normalised_rarity_value = self.Normalise_Rarity(rarity_value)
        return max(0, normalised_rarity_value)

    def Normalise_Rarity(self, rarity_value):
        # --- Dynamic normalization ---
        max_depth = self.game.depth  # define this once in your game setup
        min_value = 0.8 + 1.5 * 1  # minimum possible depth=1, luck=0, clatter=0
        max_value = 1.2 + 1.5 * max_depth + 2 * 10 + 2.5 * 5  # full caps

        normalised_rarity_value = (rarity_value - min_value) / (max_value - min_value)
        normalised_rarity_value = max(0, min(1, normalised_rarity_value))  # clamp to 0–1 just in case
        return normalised_rarity_value

    def Spawn_Loot(self, loot_type, pos):
        rarity_value = self.Calculate_Rarity_Value()
        self.game.item_handler.Spawn_Item_By_Type(loot_type, pos, rarity_value = rarity_value)

    def Set_Loot_Types(self):
        pass

    def Destroyed(self):
        if not super().Destroyed():
            return False

        self.Drop_Loot()
        return True

