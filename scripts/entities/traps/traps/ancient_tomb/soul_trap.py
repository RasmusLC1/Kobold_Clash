from scripts.entities.traps.trap import Trap

import random
from scripts.engine.keys.keys import keys

# TODO: ADD sprite
class Soul_Trap(Trap):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.soul_trap)
        self.animation = 0


    def Apply_Entity_Effect(self, entity):
        if entity.type != keys.player:
            return False
        if self.animation:
            return False
        
        target_tile = self.game.tilemap.Current_Tile((self.tile.pos[0], self.tile.pos[1] + 1))

        if not target_tile:
            print("TARGET TILE NOT FOUND", target_tile, (self.tile.pos[0], self.tile.pos[1] + 1))
            return False
        tile = self.game.tilemap.Get_Random_Tile_With_Path_Tile(target_tile)
        if not tile:
            return False

        self.animation = 1
        treasure = self.game.item_handler.loot_handler.Spawn_Loot_Type(keys.valuable, tile.scaled_pos, type = keys.soul_shard)
        self.game.player.Set_Effect(keys.soul_drained, 1, True)
        return True