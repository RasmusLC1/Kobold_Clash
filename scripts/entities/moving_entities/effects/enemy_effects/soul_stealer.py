from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys

# Increase souls from entity kills
class Soul_Stealer(Effect):
    def __init__(self, entity):
        description = 'Enemy steals souls from player'
        super().__init__(entity, keys.soul_stealer, 0, 0, (200, 250), description)

    
    def Damage_Dealt(self, damage):
        self.entity.game.player.Decrease_Souls(self.effect_strength)