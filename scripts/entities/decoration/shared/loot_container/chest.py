from scripts.entities.decoration.shared.loot_container.loot_container import Loot_Container
from scripts.engine.keys.keys import keys
from scripts.engine.utility.luck_calculator import Luck_Calculator
from scripts.entities.decoration.shared.shared_registry import register_ability

@register_ability(keys.chest)
class Chest(Loot_Container):
    def __init__(self, game, pos) -> None:
        super().__init__(game, keys.chest, pos, (32, 32), True, 20, keys.chest_break, 500, max_version = 7)

    def Save_Data(self):
        super().Save_Data()
        self.saved_data['animation'] = self.animation
        

    def Load_Data(self, data):
        super().Load_Data(data)
        self.animation = data['animation']

    def Open(self):
        if not super().Open():
            return False
        
        self.game.decoration_handler.Remove_Decoration(self)

        self.Generate_Sound(keys.chest_open, 0.1, 500)

    def Set_Version(self, game):
        MIN_RARITY = 1
        MAX_RARITY = 100

        # Rarity ranges from 0 to 100. Max version is 7 (8 possible versions).
        MAX_VERSION_INDEX = 7 
        TOTAL_VERSIONS = 8 # (0-7)

        rarity_value = Luck_Calculator.Calculate_Rarity_Value(game, MIN_RARITY, MAX_RARITY, clamp_values=False)
        

        # We use a small factor adjustment to prevent floating point errors that 
        # might incorrectly assign 100.0 to version 8.
        scaling_factor = TOTAL_VERSIONS / MAX_RARITY
        
        # Calculate the raw version index
        raw_version_float = rarity_value * scaling_factor
        
        # Clamp between 0 and 7 after taking the floor (or truncation)
        version = int(min(MAX_VERSION_INDEX, max(0, raw_version_float)))
        
        return version
    
    def Update_Animation(self):
        pass

    def Set_Loot_Types(self):
        self.loot_weights = {
                             keys.passive : 0.05,
                             keys.key : 0.1,
                             keys.bomb : 0.1,
                             keys.potion : 0.1,
                             keys.revive : 0.04,
                             keys.utility : 0.2,
                             keys.curse : 99990.1,
                             keys.valuable : 0.2,
                             keys.gem_ingot : 0.2}


