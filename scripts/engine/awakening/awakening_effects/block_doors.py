from scripts.engine.keys.keys import keys
import random
from scripts.engine.awakening.awakening_effects.awakening_function import Awakening_Function


class Block_Doors(Awakening_Function):

    def Block_Door(self):
        door = self.game.decoration_handler.Get_Random_Decoration_Of_Type(keys.door_basic)

        if not door:
            return

        door_pos = list(door.tile.pos).copy()

        door.Delete()
        self.game.tilemap.Add_Tile(keys.wall_left, 0, (door_pos[0], door_pos[1]), True)

        self.Play_Sound()
