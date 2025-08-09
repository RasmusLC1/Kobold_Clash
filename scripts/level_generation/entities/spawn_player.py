import random
from scripts.engine.keys.keys import keys

class Spawn_Player():

    @staticmethod
    def Player_Spawn(tile_size, tilemap):
        player_spawn = (20, 20)
        for y in range(player_spawn[1] - 5, player_spawn[1] + 5):
            for x in range(player_spawn[0] - 5, player_spawn[0] + 5):
                random_variant = random.randint(0, 10)

                tilemap.tilemap[(x, y)] = {keys.type: keys.floor, keys.variant: random_variant, keys.pos: (x, y), 'active': 0, 'light': 0}
        
        tilemap.offgrid_tiles.append({keys.type: keys.spawners, keys.variant: 0, keys.pos: (player_spawn[0] * tile_size, player_spawn[1] * tile_size)})



        return player_spawn