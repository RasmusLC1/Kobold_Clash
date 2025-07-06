import random
import math
from scripts.engine.keys.keys import keys

class Torch_Spawner():


    @staticmethod
    # Spawns torches based on density, it then checks distance to nearest torch to prevent overlap
    # Higher density = More torches
    def Torch_Spawner(i, j, tile_size, density, torches, offgrid_tiles):
        spawn_torch = random.randint(0, density)
        if spawn_torch == 1:
            for torch in torches:
                distance = math.sqrt((i - torch[0]) ** 2 + (j - torch[1]) ** 2)
                if distance < 8:
                    return
            torches.append((i, j))
            offgrid_tiles.append({keys.type: keys.light_source, keys.variant: 0, "pos": [i * tile_size, j * tile_size]})
