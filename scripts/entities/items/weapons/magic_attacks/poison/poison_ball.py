from scripts.entities.items.weapons.magic_attacks.base_attacks.elemental_ball import Elemental_Ball
from scripts.entities.items.weapons.magic_attacks.poison.poison_explosion import Poison_Explosion
from scripts.engine.keys.keys import keys

class Poison_Ball(Elemental_Ball):
    def __init__(self, game, pos, entity, damage, speed, special_attack, direction):
        super().__init__(game, pos, entity, keys.poison_ball, damage, speed, 2, keys.poison, 200, special_attack, direction)
        


    def Reset_Shot(self):
        fire_explosion = Poison_Explosion(self.game, self.pos, self.damage)
        self.game.item_handler.Add_Item(fire_explosion)
        return super().Reset_Shot()

