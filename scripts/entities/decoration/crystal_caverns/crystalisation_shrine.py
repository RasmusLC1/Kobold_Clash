from scripts.entities.decoration.shared.shrine.shrine import Cycling_Shrine
from scripts.engine.keys.keys import keys
from .crystal_caverns_registry import Register_Decoration
import random


@Register_Decoration(keys.crystalisation_shrine)
class Crystalisation_Shrine(Cycling_Shrine):
    SPAWN_SCATTER = 10

    def __init__(self, game, pos) -> None:
        super().__init__(game, keys.crystalisation_shrine, pos,
                         max_animation=4, animation_cooldown_max=1.5)
        self.description = "Trade gem for another"

    # Replace a gem stack with one of a different gem at amount - 1
    def Spawn_Reward(self, item) -> bool:
        if not self.Check_If_Item_Is_Valid(item):
            return False

        pos_x = self.pos[0] + random.randint(-self.SPAWN_SCATTER, self.SPAWN_SCATTER)
        pos_y = self.pos[1] + random.randint(-self.SPAWN_SCATTER, self.SPAWN_SCATTER)

        new_gem = self.game.item_handler.Spawn_Item_By_Type(
            category=keys.gem,
            pos=(pos_x, pos_y),
            rarity_value=item.value,
        )
        
        if not new_gem:
            print(f"Crystalisation_Shrine: failed to spawn gem "
                  f"(rarity={item.value}, item={item})")
            return False

        new_gem.Set_Amount(item.amount - 1)
        item.Delete_Item()
        return True

    def Check_If_Item_Is_Valid(self, item) -> bool:
        return item.sub_category == keys.gem and item.amount > 1