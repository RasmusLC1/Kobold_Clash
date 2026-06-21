from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys

# Make entity invisible and prevent enemy aggro
class Invisibility(Effect):
    def __init__(self, entity):
        description = 'Invisible to\nother entities'
        super().__init__(entity, keys.invisibility, 0, 0, (2, 3), description)


    def Set_Effect(self, effect_time, permanent=False):
        set_effect =  super().Set_Effect(effect_time, permanent)
        if set_effect:
            # Treat invisibility as effect as it requires frequent lookups
            self.entity.Set_Active_Ability(keys.invisibility)

        return set_effect


    def Update_Effect(self, delta_time):
        if not super().Update_Effect(delta_time):
            return False
        
        # Use direct call instead of Set_Active since Set_Active is locked when invisible
        self.entity.active = (max(0, 110 - self.effect_strength * 10))
        self.entity.render_needs_update = True
        return True
    


    def Remove_Effect(self, reduce_permanent=0):
        remove_effect = super().Remove_Effect(reduce_permanent)
        if remove_effect:
            self.entity.Remove_Active_Ability()

        return remove_effect