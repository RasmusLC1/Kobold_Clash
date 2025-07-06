from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys

# Increase souls from entity kills
class Arcane_Hunger(Effect):
    def __init__(self, entity):
        description = 'Gain souls\nfrom kills'
        super().__init__(entity, keys.arcane_hunger, 0, 0, (200, 250), description)