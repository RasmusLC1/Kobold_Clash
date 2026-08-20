from scripts.entities.decoration.shared.loot_container.display_loot_container import Display_Loot_Container
from scripts.engine.keys.keys import keys
from scripts.entities.decoration.shared.shared_registry import register_ability

@register_ability(keys.plinth)
class Plinth(Display_Loot_Container):
    def __init__(self, game, pos):
        super().__init__(game, keys.plinth, pos, (32, 32), True, 60, 'plinth_shatter', 700)
        
        

    def Drop_Loot(self):
        rarity_value = self.Calculate_Rarity()

        if rarity_value == keys.nothing:
                    return
        
        self.game.item_handler.Spawn_Rune(pos = (self.pos[0] + 3, self.pos[1]), type = None, rarity_value = rarity_value)

