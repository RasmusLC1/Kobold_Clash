from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys
from ..registry import register_effect

@register_effect(keys.anchor)
# Set entity movement speed to zero
class Anchor(Effect):
    def __init__(self, entity):
        description = 'Prevents pushing'
        super().__init__(entity, 'anchor', 0, 0, (3, 4), description)

    
    def Push(self, direction):
        self.entity.Set_Frame_movement((0, 0)) # Cancel frame movement