from scripts.engine.keys.keys import keys
import random

class Block_Doors():
    def __init__(self, game):
        self.game = game 

    def Block_Door(self):
        door = self.game.decoration_handler.Get_Random_Decoration_Of_Type(keys.door_basic)

        if not door:
            return

        door_pos = list(door.tile.pos).copy()

        door.Delete()
        self.game.tilemap.Add_Tile(keys.wall_left, 0, (door_pos[0], door_pos[1]), True)


        value = random.randint(0, 1)

        if value == 0:
            self.game.sound_handler.Play_Sound(keys.awakening_1, 0.3)
        else:
            self.game.sound_handler.Play_Sound(keys.awakening_2, 0.3)