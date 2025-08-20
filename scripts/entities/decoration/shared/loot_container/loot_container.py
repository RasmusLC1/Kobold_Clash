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

    def Spawn_Loot(self, loot_type, pos):
        self.game.item_handler.loot_handler.Spawn_Loot_Type(loot_type, pos)

    def Set_Loot_Types(self):
        pass

    def Destroyed(self):
        if not super().Destroyed():
            return False

        self.Drop_Loot()
        return True

