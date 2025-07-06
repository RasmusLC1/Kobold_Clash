from scripts.engine.utility.helper_functions import Helper_Functions
from scripts.engine.tilemap.tile import Tile
from scripts.engine.keys.keys import keys

import random
import json
import pygame
import math
import copy

# Tiles that are checked for physics
NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'wall', keys.wall_left, keys.wall_right, keys.wall_middle, keys.wall_top, keys.wall_bottom}
FLOOR_TTLES = {keys.floor}

class Tilemap:
    def __init__(self, game, tile_size=32) -> None:
        self.game = game
        self.tile_size = 32
        self.tilemap = {}
        self.offgrid_tiles = []
        self.update_timer = 0
        self.saved_data = {}
        self.min_x = 99999
        self.max_x = -99999
        self.min_y = 99999
        self.max_y = -99999
     

    def save(self, path):
        f = open(path, 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles}, f)
        f.close()
    
    
    # Load in tilemap and offgrid and instantiate tiles
    def Load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()
        self.tile_size = map_data['tile_size']
        
        tilemap = map_data['tilemap']
        for tile_key in tilemap:
            self.Generate_Tile(tile_key, tilemap)

        offgrid_tiles = map_data['offgrid']

        for tile_values in offgrid_tiles:
            type = tile_values[keys.type]
            variant = tile_values[keys.variant]
            pos = (tile_values[keys.pos][0], tile_values[keys.pos][1])
            
            tile = Tile(self.game, type, variant, pos, self.tile_size, 0, 0, False, True)
            self.offgrid_tiles.append(tile)

        self.Check_Next_To_Wall()


    def Generate_Tile(self, tile_key, tilemap):
        tile_values = tilemap[tile_key]
        type = tile_values[keys.type]
        variant = tile_values[keys.variant]
        pos = tuple(map(int, tile_key.split(';')))
        active = tile_values['active']
        light_level = tile_values['light']
        physics = False
        translucent = True
        if 'wall' in type:
            physics = True
            translucent = False

        tile = Tile(self.game, type, variant, pos, self.tile_size, active, light_level, physics, translucent)
        self.tilemap[tile_key] = tile
        self.min_x = min(self.min_x, pos[0])
        self.max_x = max(self.max_x, pos[0])
        self.min_y = min(self.min_y, pos[1])
        self.max_y = max(self.max_y, pos[1])
        


    # Takes an ID an looks for matches in tilemap and offgrid tiles
    def extract(self, id_pairs, keep=False):
        matches = []
        for tile in self.offgrid_tiles:
            if (tile.type, tile.variant) in id_pairs:
                matches.append(copy.copy(tile))
                if not keep:
                    self.offgrid_tiles.remove(tile)
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if (tile.type, tile.variant) in id_pairs:
                matches.append(copy.copy(tile))
                matches[-1].pos = (matches[-1].pos[0] * self.tile_size, matches[-1].pos[1] * self.tile_size)

                if not keep:
                    del self.tilemap[loc]
        
        return matches
    
    # Gets list of decorations and extracts them
    def Extract_Decorations(self, decoration_types):
        decorations = []
        for tile in self.offgrid_tiles:
            if (tile.type) in decoration_types:
                decorations.append(copy.copy(tile))
        
        return decorations

    # Runs one time when loading, but expensive to compute
    def Check_Next_To_Wall(self):
        for tile_key in self.tilemap:
            if 'wall' in self.tilemap[tile_key].type:
                self.tilemap[tile_key].Set_Next_To_Wall(True)
                continue


            x_key, y_key = map(int, tile_key.split(";"))
            for x in range(x_key - 1, x_key + 1):
                for y in range(y_key - 1, y_key + 1):
                    key = str(x) + ';' + str(y)
                    if not key in self.tilemap:
                        continue

                    if 'wall' in self.tilemap[key].type:
                        self.tilemap[tile_key].Set_Next_To_Wall(True)
                        break

                if self.tilemap[tile_key].next_to_Wall:
                    break


    def Search_Nearby_Tiles(self, max_distance, pos, category, ID = 0):
        pos = (pos[0] // self.tile_size, pos[1] // self.tile_size)
        
        
        entities = []
        for x in range(math.floor(pos[0] - max_distance), math.floor(pos[0] + max_distance)):
            for y in range(math.floor(pos[1] - max_distance), math.floor(pos[1] + max_distance)):
                if x <= self.min_x or y <= self.min_y:
                    continue

                if x >= self.max_x or y >= self.max_y:
                    continue

                tile_key = str(x) + ';' + str(y)
                tile = self.tilemap[tile_key]
                if not tile:
                    continue

                if not tile.entities:
                    continue

                new_entities = tile.Search_Entities(category, ID)
                if not new_entities:
                    continue
                        
                entities.extend(new_entities)

        
        return entities

    def Search_Nearby_Tiles_For_Type(self, max_distance, pos, type, ID = 0):
        pos = (pos[0] // self.tile_size, pos[1] // self.tile_size)
        
        
        entities = []
        for x in range(math.floor(pos[0] - max_distance), math.floor(pos[0] + max_distance)):
            for y in range(math.floor(pos[1] - max_distance), math.floor(pos[1] + max_distance)):
                if x <= self.min_x or y <= self.min_y:
                    continue

                if x >= self.max_x or y >= self.max_y:
                    continue

                tile_key = str(x) + ';' + str(y)
                tile = self.tilemap[tile_key]
                if not tile:
                    continue

                if not tile.entities:
                    continue

                new_entities = tile.Search_Type(type, ID)
                if not new_entities:
                    continue
                        
                entities.extend(new_entities)

        
        return entities


    # return the entities on a tile           
    def Get_Tile_Entities(self, tile_key):
        return self.tilemap[tile_key].entities


    # Add an remove entities from tiles dynamically as needed
    def Remove_Entity_From_Tile(self, tile, entity_ID):
        if not tile:
            print("Error removing entity from  tile")
            return
        tile.Clear_Entity(entity_ID)

    def Add_Entity_To_Tile(self, tile, entity):
        if not tile:
            print("Error adding entity to  tile", entity.type)
            return
        tile.Add_Entity(entity)

    # Get the position of tiles in the tilemap
    def Get_Pos(self):
        positions = []
        for tile in self.tilemap.values():
            positions.append(tile.pos)
        return positions
    
    # Get the position of tiles in the tilemap
    def Set_Global_Brightness(self, light_level):
        for tile in self.tilemap.values():
            tile.Set_Light_Level(light_level)
            tile.Set_Active(10000)
        return
    


    # Get surrounding tiles
    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
        
    # Check what tile type is in a given position
    def Current_Tile_Type_Without_Offset(self, pos):
        check_loc = str(pos[0]) + ';' + str(pos[1])
        if check_loc in self.tilemap:
            return self.tilemap[check_loc].type
        else:
            return None
    
    def Add_Tile(self, type, variant, pos, physics, active = 0, light_level = 0, translucent = True):
        tile = Tile(self.game, type, variant, pos, self.tile_size, active, light_level, physics, translucent)
        tile_key = ';'.join(map(str, pos))
        self.game.ray_caster.Remove_Tile(self.tilemap[tile_key]) # Remove old tile from renderer 
        self.tilemap[tile_key] = None
        self.tilemap[tile_key] = tile
        
    # Check what tile is in a given position and return the full tile
    def Current_Tile(self, tile_key):
        if not tile_key in self.tilemap:
            return None
        tile = self.tilemap[tile_key]
        if not tile:
            return None
        
        return tile


    # Finds nearby tiles 
    def Find_Nearby_Tiles(self, pos, max_distance):
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        normalised_max_distance = max_distance // self.tile_size
        nearby_tiles = []
        for tile_key in self.tilemap:
            tile = self.tilemap[tile_key]
            # Calculate the Euclidean distance
            distance = Helper_Functions.Abs_Distance_Float(tile_loc, tile.pos)
            if distance < normalised_max_distance:
                nearby_tiles.append(tile)
        return nearby_tiles
    
    def Update_Tile_Type(self, tile, new_type):
        tile.Set_Type(new_type)
        tile.Set_Sprite()


    # Check for collision on relevant tile
    def Collision_Check(self, pos):
        tile = self.Current_Tile_Type(pos)
        if not tile:
            return False
        if tile.type == keys.floor:
            return True
        else:
            return False

    

    
    # Check for collision with solid tiles
    # Returns tile if there is collision
    def solid_check(self, pos):
        tile_loc = str(int(pos[0] // self.tile_size)) + ';' + str(int(pos[1] // self.tile_size))
        if not tile_loc in self.tilemap:
            return None
        if self.tilemap[tile_loc].physics:
            return self.tilemap[tile_loc]
    
    # Check for collision with solid tiles
    def Solid_Check_Tile(self, tile):
        if not tile in self.tilemap:
            return
        if self.tilemap[tile].physics:
            return self.tilemap[tile]
    
    # Check for physics tiles
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if not tile:
                print(tile, pos)
                continue
            if tile.physics:
                rects.append(pygame.Rect(tile.pos[0] * self.tile_size, tile.pos[1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
    
    # Check for physics tiles
    def floor_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if not tile:
                print(tile, pos)
                continue
            if tile.type in FLOOR_TTLES:
                rects.append(pygame.Rect(tile.pos[0] * self.tile_size, tile.pos[1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
    
    def Render_All_Tiles(self):
        self.game.ray_caster.Set_Disable_Distance_Debugger(True)
        for tile_key in self.tilemap:
            self.tilemap[tile_key].Render_All()
            self.game.ray_caster.Add_Tile(self.tilemap[tile_key])


    def Set_Light_Level(self, tile, new_light_level):
        tile.Set_Light_Level(new_light_level)

    def Get_Random_Tile_With_Path_To_Player(self):
        tiles = []
        for tile in self.tilemap.values():
            if not tile.type == keys.floor:
                continue

            tiles.append(tile)
        tile_found = False
        random_tile = None
        player = self.game.player
        while not tile_found:
            random_tile = random.choice(tiles)
            tile_pos = (random_tile.pos[0] - self.game.a_star.min_x, random_tile.pos[1] - self.game.a_star.min_y)
            player_pos = (round(player.pos[0] // self.game.tilemap.tile_size) - self.game.a_star.min_x, round(player.pos[1] // self.game.tilemap.tile_size) - self.game.a_star.min_y)
            path = self.game.a_star.a_star_search(tile_pos, player_pos)
            if path:
                tile_found = True

        return random_tile

    def Clear_Tilemap(self):
        self.tilemap.clear()
        self.offgrid_tiles.clear()
    
    # Render function that shows the entire screen
    # Not really used
    def Render(self, surf, offset=(0, 0)):
        for tile in self.tilemap.values():
            surf.blit(self.game.assets[tile.type][tile.variant], (tile.pos[0] * self.tile_size - offset[0], tile.pos[1] * self.tile_size - offset[1]))

        for tile in self.offgrid_tiles:
            if 'Room' in tile.type:
                continue
            surf.blit(self.game.assets[tile.type][tile.variant], (tile.pos[0] - offset[0], tile.pos[1] - offset[1]))

    # Render function that only renders the tiles in the tiles array
    def Render_Tiles(self, tiles, surf, offset=(0, 0)):
        for tile in tiles:
            if not tile:
                continue
            tile.Render(surf, offset)
            


