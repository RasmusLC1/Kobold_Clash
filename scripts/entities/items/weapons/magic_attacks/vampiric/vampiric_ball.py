from scripts.entities.items.weapons.magic_attacks.base_attacks.elemental_ball import Elemental_Ball
from scripts.entities.items.weapons.magic_attacks.vampiric.soul_pit import Soul_Pit
from scripts.engine.keys.keys import keys


class Vampiric_Ball(Elemental_Ball):
    def __init__(self, game, pos, entity, damage, speed, special_attack, direction):
        super().__init__(game, pos, entity, keys.vampiric_ball, damage, speed, 2, keys.vampiric, 200, special_attack, direction)


    def Reset_Shot(self):
        soul_pit = Soul_Pit(self.game, self.pos, self.damage)
        self.game.item_handler.Add_Item(soul_pit)
        return super().Reset_Shot()

