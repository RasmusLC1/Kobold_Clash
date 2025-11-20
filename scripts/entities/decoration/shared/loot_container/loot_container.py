import random
from scripts.entities.decoration.decoration import Decoration
from scripts.engine.keys.keys import keys


class Loot_Container(Decoration):
    def __init__(self, game, type, pos, size = (32, 32), destructable = False, health = 100, destruction_sound = None, destruction_clatter = 500, version = 1) -> None:
        super().__init__(game, type, pos, size, destructable, health, destruction_sound, destruction_clatter)
        self.version = version
        self.loot_type = 0
        self.empty = False
        self.loot_amount = 0
        self.Set_Min_Rarity()
        self.Set_Max_Rarity()
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
        # Depth 0–7 → 0–30
        depth_factor = (self.game.depth / 7) * 30

        # Luck 0–10 → 0–30
        luck_factor = (self.game.player.luck / 10) * 30

        # Clatter 0–10 → 0–30
        clatter_factor = (self.game.clatter.Get_Awakening_Level() / 10) * 30

        # Base randomness (small noise): 0–20
        noise = random.uniform(0, 10)

        # Swing randomness (rare bumps/dips): -10 to +10
        swing = random.uniform(-5, 5)

        total = depth_factor + luck_factor + clatter_factor + noise + swing
        return self.Clamp_Rarity(total)


    # Clamp the rarity value to prevent legendaries from dropping in vases
    def Clamp_Rarity(self, rarity_value):
        return max(self.min_rarity_value, min(self.max_rarity_value, rarity_value))



    def Set_Min_Rarity(self):
        min_rarity_values = {
            keys.chest : 5,
            keys.plinth : 20,
            keys.potion_table : 30,
            keys.weapon_rack : 5,
            keys.bookshelf : 20,
            keys.effigy_tomb : 40,
            keys.vase : 1
        }

        rarity = min_rarity_values.get(self.type)

        if not rarity:
            rarity = 1
            print("LOOT TYPE NOT FOUND", self.type)

        self.min_rarity_value = rarity * self.version


    def Set_Max_Rarity(self):
        max_rarity_values = {
            keys.chest : 20,
            keys.plinth : 60, # High end runes are available in shrines
            keys.potion_table : 80,
            keys.weapon_rack : 20,
            keys.bookshelf : 80,
            keys.effigy_tomb : 90,
            keys.vase : 5
        }

        rarity = max_rarity_values.get(self.type)

        if not rarity:
            rarity = 1
            print("LOOT TYPE NOT FOUND", self.type)

        self.max_rarity_value = rarity * self.version


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

