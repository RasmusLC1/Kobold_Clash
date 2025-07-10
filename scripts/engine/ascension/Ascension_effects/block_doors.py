from scripts.engine.keys.keys import keys

class Block_Doors():
    def __init__(self, game):
        self.game = game 

    def Block_Door(self):
        door = self.game.decoration_handler.Get_Random_Decoration_Of_Type(keys.door)

        door_pos = door.pos.copy()

        door.Delete()

        self.game.tilemap.Add_Tile(keys.wall_left, 0, (door_pos[0], door_pos[1]), True)
