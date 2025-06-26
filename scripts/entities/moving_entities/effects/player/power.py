from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.assets.keys import keys

# Power effect is added to the rune's power in the rune itself
class Power(Effect):
    def __init__(self, entity):
        description = 'Increases Rune power'
        super().__init__(entity, keys.power, 0, 0, (120, 160), description)

    def Set_Effect(self, effect_time, permanent=False):
        if not super().Set_Effect(effect_time, permanent):
            return False
        
        self.entity.game.inventory.rune_inventory.Set_Descriptions()

        return True
    
    def Remove_Effect(self, reduce_permanent=0):
        if not super().Remove_Effect(reduce_permanent):
            return False
        
        self.entity.game.inventory.rune_inventory.Set_Descriptions()
        
        return True