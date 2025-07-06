from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys

# Reduce the cost runes
class Magnet(Effect):
    def __init__(self, entity):
        description = 'Pulls items\ntowards player'
        super().__init__(entity, keys.magnet, 0, 0, (200, 250), description)
        self.effect_max = 4


    def Update_Effect(self):
        if not super().Update_Effect():
            return False
        self.entity.game.item_handler.Pick_Up_All_Nearby_Items(self.effect)
        return True

    

    
    