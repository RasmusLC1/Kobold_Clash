from scripts.entities.decoration.shared.loot_container.display_loot_container import Display_Loot_Container
from scripts.engine.keys.keys import keys

BASE_VALUE = 20

class Weapon_rack(Display_Loot_Container):
    def __init__(self, game, pos) -> None:
        super().__init__(game, type=keys.weapon_rack, pos=pos, size=(32, 32), destructable=True, health=20, destruction_sound='weapon_rack_break', destruction_clatter= 400)


    def Drop_Loot(self):
        self.game.item_handler.Spawn_Weapon((self.pos[0], self.pos[1] - 3), value = BASE_VALUE)
