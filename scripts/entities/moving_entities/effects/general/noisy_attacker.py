from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys
from ..registry import register_effect

@register_effect(keys.noisy_attacker)
class Noisy_Attacker(Effect):
    def __init__(self, entity):
        description = 'Generate noise\non attack'
        super().__init__(entity, "increase_strength", 0, 0, (2, 3), description)
    
    # Replace
    def Damage_Dealt(self, damage):
        sound_strength = self.effect_strength * damage * 5
        self.entity.Generate_Sound(keys.bell, 0.3, sound_strength)