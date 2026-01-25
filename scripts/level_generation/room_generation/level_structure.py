import random
from scripts.level_generation.dungeon_enum_keys import *
from scripts.engine.keys.keys import keys


class Level_Structure():
    def __init__(self, game):
        self.game = game

    def Level_Structure(self, map, tile_size, size_x, size_y, player_spawn, offgrid_tiles):
        tilemap = {}
        self.Set_Dungeon_Type()

        traps = [keys.spike_trap, keys.spike_poison_trap, keys.pit_trap]

        for j in range(size_y):
            for i in range(size_x):
                if map[i][j] == WALL: 
                    if not self.Wall_Checker(map, i, j, size_x, size_y, tilemap):
                        tilemap[(i, j)] = {keys.type: self.wall_bottom, keys.variant: 0, keys.pos: (i, j)}


                elif map[i][j] == FLOOR: # Floor
                    random_variant = random.randint(0, 10)
                    tilemap[(i, j)] = {keys.type: self.floor, keys.variant: random_variant, keys.pos: (i, j)}

                elif map[i][j] == LAVA:
                    tilemap[(i, j)] = {keys.type: keys.lava_env, keys.variant: 0, keys.pos: (i, j)}
                elif map[i][j] == DOOR:
                    tilemap[(i, j)] = {keys.type: self.floor, keys.variant: 0, keys.pos: (i, j)}
                    offgrid_tiles.append({
                                    keys.type: keys.door_basic,
                                    keys.variant: 0,
                                    keys.pos: (i * tile_size, j * tile_size)
                                })
                elif map[i][j] == TRAP:
                    trap_type = random.randint(0, 2)
                    tilemap[(i, j)] = {keys.type: traps[trap_type], keys.variant: 0, keys.pos: (i, j)}

        tilemap = self.Spawn_Player_Area(player_spawn, tilemap)
        offgrid_tiles.append({keys.type: keys.spawners, keys.variant: 0, keys.pos: (player_spawn[0] * tile_size, player_spawn[1] * tile_size)})


        return tilemap


    def Spawn_Player_Area(self, player_spawn, tilemap):
        player_spawn = (20, 20)
        for y in range(player_spawn[1] - 5, player_spawn[1] + 5):
            for x in range(player_spawn[0] - 5, player_spawn[0] + 5):
                random_variant = random.randint(0, 10)
                tilemap[(x, y)] = {keys.type: keys.floor, keys.variant: random_variant, keys.pos: (x, y)}
        
        return tilemap
    

    def Wall_Checker(self, map, i, j, size_x, size_y, tilemap):
        random_variant = random.randint(0, 3)
        # Handle Edge cases first to prevent crashes
        if i <= 1:
            tilemap[(i, j)] = {keys.type: self.wall_left, keys.variant: random_variant, keys.pos: (i, j)}
            return True

        elif i >= size_x - 2:
            tilemap[(i, j)] = {keys.type: self.wall_right, keys.variant: random_variant, keys.pos: (i, j)}
            return True
        
        elif j <= 1:
            tilemap[(i, j)] = {keys.type: self.wall_top, keys.variant: random_variant, keys.pos: (i, j)}
            return True
        
        elif j >= size_y - 2:
            tilemap[(i, j)] = {keys.type: self.wall_top, keys.variant: random_variant, keys.pos: (i, j)}
            return True
        


        if map[i][j + 1] != WALL:
            tilemap[(i, j)] = {keys.type: self.wall_top, keys.variant: random_variant, keys.pos: (i, j)}
            return True



        if self.Corner_Handling(map, i, j, random_variant, tilemap):
            return True
        

        if map[i + 1][j] != WALL and map[i - 1][j] != WALL:
            tilemap[(i, j)] = {keys.type: self.wall_middle, keys.variant: random_variant, keys.pos: (i, j)}
            return True

        if map[i + 1][j] != WALL:
            tilemap[(i, j)] = {keys.type: self.wall_left, keys.variant: random_variant, keys.pos: (i, j)}
            return True


        if map[i - 1][j] != WALL:
            tilemap[(i, j)] = {keys.type: self.wall_right, keys.variant: random_variant, keys.pos: (i, j)}
            return True

        return False
    
    def Corner_Handling(self, map, i, j, random_variant, tilemap) -> bool:
        if not map[i][j - 1] != WALL:
            return False
        
        left_side = 0
        right_side = 1
        both_sides = 2
        if map[i + 1][j] != WALL and map[i - 1][j] != WALL:
            tilemap[(i, j)] = {keys.type: self.wall_bottom_corner, keys.variant: both_sides, keys.pos: (i, j)}

        elif map[i + 1][j] != WALL:
            tilemap[(i, j)] = {keys.type: self.wall_bottom_corner, keys.variant: right_side, keys.pos: (i, j)}

        elif map[i - 1][j] != WALL:
            tilemap[(i, j)] = {keys.type: self.wall_bottom_corner, keys.variant: left_side, keys.pos: (i, j)}

        else:
            tilemap[(i, j)] = {keys.type: self.wall_bottom, keys.variant: random_variant, keys.pos: (i, j)}
        return True
    

    def Set_Dungeon_Type(self):
        if self.game.dungeon_type == keys.ancient_crypt:
            self.floor = keys.floor
            self.wall_left = keys.wall_left
            self.wall_right = keys.wall_right
            self.wall_bottom = keys.wall_bottom
            self.wall_bottom_corner = keys.wall_bottom_corner
            self.wall_middle = keys.wall_middle
            self.wall_top = keys.wall_top
        else:
            self.floor = keys.floor
            self.wall_left = keys.wall_left
            self.wall_right = keys.wall_right
            self.wall_bottom = keys.wall_bottom
            self.wall_bottom_corner = keys.wall_bottom_corner
            self.wall_middle = keys.wall_middle
            self.wall_top = keys.wall_top