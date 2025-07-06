from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys

# Make entity invisible and prevent enemy aggro
class Invisibility(Effect):
    def __init__(self, entity):
        description = 'Invisible to\nother entities'
        super().__init__(entity, keys.invisibility, 0, 0, (130, 160), description)

    def Update_Effect(self):
        if not self.effect:
            return False
        
        # Use direct call instead of Set_Active since Set_Active is locked when invisible
        self.entity.active = (max(0, 110 - self.effect * 10))
        self.entity.render_needs_update = True
        self.Update_Cooldown()
        return True
    