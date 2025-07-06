from scripts.entities.items.weapons.magic_attacks.base_attacks.elemental_explosion import Elemental_Explosion
from scripts.engine.keys.keys import keys

class Electric_Explosion(Elemental_Explosion):
    def __init__(self, game, pos, power, entity = None):
        super().__init__(game, keys.electric_explosion, keys.electric, pos, power, 5, 5, 5, entity)
        self.light_source = self.game.light_handler.Add_Light(self.pos, 5, self.tile)
        self.light_level = self.game.light_handler.Initialise_Light_Level(self.tile)

