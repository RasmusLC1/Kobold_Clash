class Spawn_Enemies():
    def __init__(self, game):
        self.game = game

    def Spawn_Enemy(self):
        tile = self.game.tilemap.Get_Random_Tile_With_Path_To_Player()
        pos = list((tile.pos[0] * 32, tile.pos[1] * 32))
        self.game.enemy_handler.Enemy_Spawner(pos)