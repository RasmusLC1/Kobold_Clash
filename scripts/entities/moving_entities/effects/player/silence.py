from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys
from .player_registry import register_effect

@register_effect(keys.silence)
# Don't generate sound and clatter
class Silence(Effect):
    def __init__(self, entity):
        description = 'Reduces noise'

        super().__init__(entity, keys.silence, 0, 0, (2, 3), description)


    def Set_Effect(self, effect_time, permanent=False):
        set_effect =  super().Set_Effect(effect_time, permanent)
        if set_effect:
            # Treat silence as effect as it requires frequent lookups
            self.entity.Set_Active_Ability(keys.silence)

        return set_effect

    
    def Remove_Effect(self, reduce_permanent=0):
        remove_effect = super().Remove_Effect(reduce_permanent)
        if remove_effect:
            self.entity.Remove_Active_Ability()

        return remove_effect