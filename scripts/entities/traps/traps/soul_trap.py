from scripts.entities.traps.trap import Trap

import random
from scripts.engine.keys.keys import keys

# TODO: ADD sprite
class Soul_Trap(Trap):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.soul_trap)
        self.animation = random.randint(0, 1)


    def Apply_Entity_Effect(self, entity):
        if entity.type != keys.player:
            return False
        if self.animation:
            return False
        
        self.animation = 1

        tile = self.game.tilemap.Get_Random_Tile_With_Path_To_Player()
        treasure = self.game.item_handler.loot_handler.Spawn_Loot_Type(keys.valuable, tile.scaled_pos, None, keys.soul_shard)
        self.game.player.Set_Effect(keys.soul_drained, 1, True)

        return True