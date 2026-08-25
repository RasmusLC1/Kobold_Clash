import random
from scripts.entities.decoration.decoration import Decoration
from scripts.engine.keys.keys import keys
from scripts.entities.decoration.shared.loot_container.loot_component import LootComponent

class Loot_Container(Decoration):
    # Centralized defaults for base container types
    MIN_RARITY_DEFAULTS = {
        keys.chest: 5,
        keys.plinth: 20,
        keys.potion_table: 30,
        keys.weapon_rack: 5,
        keys.bookshelf: 20,
        keys.effigy_tomb: 40,
        keys.vase: 1,
    }

    MAX_RARITY_DEFAULTS = {
        keys.chest: 20,
        keys.plinth: 60,
        keys.potion_table: 80,
        keys.weapon_rack: 20,
        keys.bookshelf: 80,
        keys.effigy_tomb: 90,
        keys.vase: 10,
    }

    def __init__(self, game, type, pos, size=(32, 32), destructable=False, health=100, destruction_sound=None, destruction_clatter=500, max_animation=0) -> None:
        self.max_animation = max_animation # 0 indexed
        version = self.Set_Version(game)
        super().__init__(game, type, pos, size, destructable, health, destruction_sound, destruction_clatter, version, max_animation)
        
        self.text_cooldown = 0
        self.text_animation = 0
        self.sub_category = keys.loot_container

        # Retrieve rarity boundaries for this container type
        min_rarity = self.MIN_RARITY_DEFAULTS.get(self.type, 1)
        max_rarity = self.MAX_RARITY_DEFAULTS.get(self.type, 1)

        # Build loot weights via subclass override or default to empty
        loot_weights = self.Get_Loot_Types()

        # Instantiate component
        self.loot_component = LootComponent(
            game=game,
            entity_type=self.type,
            min_rarity=min_rarity,
            max_rarity=max_rarity,
            loot_weights=loot_weights
        )

    def Save_Data(self):
        super().Save_Data()
        self.saved_data['empty'] = self.loot_component.empty

    def Load_Data(self, data):
        super().Load_Data(data)
        self.loot_component.empty = data.get('empty', False)

    def Open(self):
        if self.loot_component.empty:
            return False
            
        self.Drop_Loot()
        return True

    def Drop_Loot(self):
        self.loot_component.Drop_Loot(self.Get_Pos())

    def Get_Pos(self):
        rand_pos_x = self.pos[0] + random.randint(-100, 100) / 10
        rand_pos_y = self.pos[1] + random.randint(-100, 100) / 10
        return (rand_pos_x, rand_pos_y)

    def Set_Version(self, game):
        return 0

    # Overwritten by base classes
    def Get_Loot_Types(self):
        return {}

    def Destroyed(self):
        if not super().Destroyed():
            return False
        self.Drop_Loot()
        return True