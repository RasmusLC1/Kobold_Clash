from scripts.entities.moving_entities.effects.effect import Effect
from scripts.engine.keys.keys import keys

# Return damage dealth to entity
class Thorns(Effect):
    def __init__(self, entity):
        description = 'Reflects damage\nback to\nattackers'
        super().__init__(entity, keys.thorns, 0, 0, (3, 4), description)
        self.type = 'slash'


    def Set_Type(self, type):
        self.type = type
