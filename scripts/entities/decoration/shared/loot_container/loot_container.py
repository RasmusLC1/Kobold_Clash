import random
from scripts.entities.decoration.decoration import Decoration
from scripts.engine.keys.keys import keys
from scripts.engine.utility.luck_calculator import Luck_Calculator


class Loot_Container(Decoration):
    def __init__(self, game, type, pos, size = (32, 32), destructable = False, health = 100, destruction_sound = None, destruction_clatter = 500, max_version = 0) -> None:
        self.max_version = max_version # 0 indexed
        version = self.Set_Version(game)
        super().__init__(game, type, pos, size, destructable, health, destruction_sound, destruction_clatter, version, max_version)
        self.Set_Max_Rarity()
        self.Set_Min_Rarity()
        self.loot_type = 0
        self.empty = False
        self.loot_amount = 0
        self.text_cooldown = 0
        self.text_animation = 0
        self.loot_weights = {}
        self.Set_Loot_Types()
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
        rarity_value = Luck_Calculator.Calculate_Rarity_Value(self.game, self.min_rarity_value, self.max_rarity_value)
        affordable_loot_types = self.game.item_handler.Check_If_Loot_Is_Affordable(list(self.loot_weights.keys()), rarity_value)

        weight_values = [self.loot_weights[loot_type] for loot_type in affordable_loot_types]
        loot_type = random.choices(affordable_loot_types, weight_values, k=1)[0]

        if loot_type == keys.nothing:
            return
        
        self.Spawn_Loot(loot_type, self.Get_Pos(), rarity_value)
    
    def Get_Pos(self):
        rand_pos_x = self.pos[0] + random.randint(-100, 100)/10
        rand_pos_y = self.pos[1] + random.randint(-100, 100)/10
        return (rand_pos_x, rand_pos_y)

    # Return default version 0
    def Set_Version(self, game):
        return 0

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
            print("LOOT TYPE NOT FOUND", self.type, self.animation, rarity)
            rarity = 1
            return

        self.min_rarity_value = rarity * self.animation


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

        self.max_rarity_value = rarity * self.animation


    def Spawn_Loot(self, loot_type, pos, rarity_value):
        self.game.item_handler.Spawn_Item_By_Type(loot_type, pos, rarity_value = rarity_value)

    def Set_Loot_Types(self):
        pass

    def Destroyed(self):
        if not super().Destroyed():
            return False

        self.Drop_Loot()
        return True

