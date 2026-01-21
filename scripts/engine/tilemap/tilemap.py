from scripts.engine.utility.helper_functions import Helper_Functions
from scripts.engine.tilemap.tile import Tile
from scripts.engine.tilemap.minimap import Minimap
from scripts.engine.keys.keys import keys

import random
import json
import pygame
import math
import copy


# Tiles that are checked for physics
NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]

class Tilemap:
    def __init__(self, game, tile_size=32) -> None:
        self.game = game
        self.tile_size = 32
        self.saved_data = {}
        self.tilemap = {}
        self.tiles_not_touching_wall = {}
        self.offgrid_tiles = []
        self.update_timer = 0
        self.min_x = 99999
        self.max_x = -99999
        self.min_y = 99999
        self.max_y = -99999
        self.dungeon_type = None
        self.minimap = Minimap(game, self)
     
    def Save_data(self):
        self.saved_data['depth'] = self.game.depth
        self.saved_data['dungeon_type'] = self.game.dungeon_type
        self.saved_data['wall_tiles'] = []
        for tile in self.tiles_not_touching_wall.values():
            self.saved_data['wall_tiles'].append(tile.pos)

        self.saved_data['tiles'] = {}
        for tile in self.tilemap.values():
            tile.Save_Data()
            tile_key = self.Convert_Tile_Pos_To_Key(tile.pos)
            self.saved_data['tiles'][tile_key] = tile.saved_data
    
        minimap_tiles =  self.minimap.Get_Tiles()
        self.saved_data['minimap'] = []
        for tile_pos in minimap_tiles:
            self.saved_data['minimap'].append(self.Convert_Tile_Pos_To_Key(tile_pos))

    def Load_Data(self, data = None):
        # Set the dungeon information
        if data:
            self.game.depth = data['depth']
            self.game.dungeon_type = data['dungeon_type']
            self.dungeon_type = self.game.dungeon_type
            
            for tile_key, tile_data in data['tiles'].items():
                tile_pos = self.Tuple_From_String(tile_key)
                tile = self.Generate_Tile(tile_pos, tile_data)
                tile.Load_Data(tile_data)

            for tile_pos in data['wall_tiles']:
                tile = self.Get_Tile(tile_pos)
                if not tile:
                    print(tile_pos)
                    continue
                self.tiles_not_touching_wall[tile_pos] = tile
            
        for tile_key in data['minimap']:
            tile_pos = self.Tuple_From_String(tile_key)
            tile = self.Get_Tile(tile_pos)
            if not tile:
                print("FAILED TO FIND TILE FOR MINIMAP", tile_key)
                return
            self.Add_Tile_To_Minimap(tile)

    def Tuple_From_String(self, tile_key):
        x, y = map(int, tile_key.split(';'))
        tile_pos = (x, y)
        return tile_pos

    def Convert_Tile_Pos_To_Key(self, pos):
        return f"{pos[0]};{pos[1]}"

    def Convert_Dungeon_Generation_Dic_To_Tilemap(self, tilemap, offgrid_data):
        self.Set_Dungeon_Type()
        for tile_pos, tile_values in tilemap.items():
            self.Generate_Tile(tile_pos, tile_values)

        self.offgrid_tiles = offgrid_data
        self.Find_Tiles_Not_Touching_Wall()



    def Generate_Tile(self, tile_pos, tile_values):
        type = tile_values[keys.type]
        sub_type = self.Set_Sub_Type(type)
        variant = tile_values[keys.variant]
        
        active = tile_values.get('active', 0)
        light_level = tile_values.get('light', 0)
        physics = False
        translucent = True

        if 'wall' in type:
            physics = True
            translucent = False

        tile = Tile(self.game, type, sub_type, variant, tile_pos, active, light_level, physics, translucent)
        self.tilemap[tile_pos] = tile
        self.min_x = min(self.min_x, tile_pos[0])
        self.max_x = max(self.max_x, tile_pos[0])
        self.min_y = min(self.min_y, tile_pos[1])
        self.max_y = max(self.max_y, tile_pos[1])
        return tile

    def Set_Dungeon_Type(self):
        dungeon_types = {
            keys.ancient_crypt : "crypt_",
            keys.crystal_caverns : "crystal_cavern_",
        }
        self.dungeon_type = dungeon_types.get(self.game.dungeon_type)



    def Set_Sub_Type(self, type):
        return self.dungeon_type + type

    # Runs one time when loading, but expensive to compute
    def Find_Tiles_Not_Touching_Wall(self):
        self.tiles_not_touching_wall.clear()
        for tile_key, tile in self.tilemap.items():
            if not tile or tile.type != keys.floor:
                continue
            x, y = tile.pos
            touching_wall = False

            for offset in NEIGHBOR_OFFSETS:
                nx, ny = x + offset[0], y + offset[1] # Get neigbour key
                neighbor_key = (nx, ny)

                if neighbor_key not in self.tilemap:
                    continue
                
                neighbor_tile = self.tilemap[neighbor_key]
                if neighbor_tile and neighbor_tile.physics:
                    touching_wall = True
                    break
            
            if not touching_wall:
                self.tiles_not_touching_wall[tile_key] = tile
            else:
                self.tilemap[tile_key].Set_Next_To_Wall(True)




    # Takes an ID an looks for matches in tilemap and offgrid tiles
    def extract(self, id_pairs, keep=False):
        matches = []
        to_remove = []

        for offgrid_tile in self.offgrid_tiles:
            if (offgrid_tile[keys.type], offgrid_tile[keys.variant]) in id_pairs:
                matches.append(copy.copy(offgrid_tile))
                if not keep:
                    to_remove.append(offgrid_tile)

        for tile in to_remove:
            self.offgrid_tiles.remove(tile)

        for loc in list(self.tilemap):
            tile = self.tilemap[loc]
            if (tile.type, tile.variant) in id_pairs:
                matches.append(copy.copy(tile))
                matches[-1].pos = (matches[-1].pos[0] * self.tile_size, matches[-1].pos[1] * self.tile_size)
                if not keep:
                    del self.tilemap[loc]

        return matches

    def Search_Nearby_Tiles(self, max_distance, pos, category, ID = 0):
        pos = (pos[0] // self.tile_size, pos[1] // self.tile_size)
        
        
        entities = []
        for x in range(math.floor(pos[0] - max_distance), math.floor(pos[0] + max_distance)):
            for y in range(math.floor(pos[1] - max_distance), math.floor(pos[1] + max_distance)):
                if x <= self.min_x or y <= self.min_y:
                    continue

                if x >= self.max_x or y >= self.max_y:
                    continue

                tile_key = (x, y)
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

                tile_key = (x, y)
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
        tile = self.tilemap.get(tile_key)
        
        if not tile:
            return None
        
        return tile.entities
    
    def Get_Tile(self, tile_key):
        tile = self.tilemap.get(tile_key)
        return tile



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
            check_loc = (tile_loc[0] + offset[0], tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
        
    # Check what tile type is in a given position
    def Current_Tile_Type_Without_Offset(self, pos):
        if pos in self.tilemap:
            return self.tilemap[pos].type
        else:
            return None
    
    def Add_Tile(self, type, variant, pos, physics, active = 0, light_level = 0, translucent = True):
        sub_type = self.Set_Sub_Type(type)
        tile = Tile(self.game, type, sub_type, variant, pos, active, light_level, physics, translucent)
        self.game.ray_caster.Remove_Tile(self.tilemap[pos]) # Remove old tile from renderer 
        self.tilemap[pos] = None
        self.tilemap[pos] = tile
        
    # Check what tile is in a given position and return the full tile
    def Current_Tile(self, tile_pos):
        try:
            tile_key = (round(tile_pos[0]), round(tile_pos[1]))
        except Exception as e:
            print("CAN'T FIND TILEKEY", e, tile_pos)
            return
        tile = self.tilemap.get(tile_key)
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
        return not tile.physics

    
    # Check for collision with solid tiles
    # Returns tile if there is collision
    def solid_check(self, pos):
        tile_loc = (pos[0] // self.tile_size, pos[1] // self.tile_size)
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
                rects.append(pygame.Rect(tile.scaled_pos[0], tile.scaled_pos[1], self.tile_size, self.tile_size))
        return rects
    
    def Get_Floor_Tiles(self):
        floor_tiles = {}
        for tile_key, tile in self.tilemap.items():
            if tile.type == keys.floor:
                floor_tiles[tile_key] = tile 

        return floor_tiles

    # Check for physics tiles
    def floor_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if not tile:
                print(tile, pos)
                continue
            if tile.type == keys.floor:
                rects.append(pygame.Rect(tile.scaled_pos[0], tile.scaled_pos[1], self.tile_size, self.tile_size))
        return rects
    

    def Set_Light_Level(self, tile, new_light_level):
        tile.Set_Light_Level(new_light_level)

    def Get_Random_Tile_With_Path_To_Player(self):
        tiles = []
        for tile in self.tiles_not_touching_wall.values():
            if tile.type != keys.floor:
                continue

            tiles.append(tile)
        if not tiles:
            print("TILES NOT FOUND", self.tiles_not_touching_wall)
            for tile in self.tiles_not_touching_wall.values():
                print(tile.sub_type, tile.type)
            return
        tile_found = False
        random_tile = None
        player = self.game.player
        fail = 0

        while not tile_found:
            random_tile = random.choice(tiles)
            tile_pos = (random_tile.pos[0] - self.game.a_star.min_x, random_tile.pos[1] - self.game.a_star.min_y)
            player_pos = (round(player.tile.pos[0]) - self.game.a_star.min_x, round(player.tile.pos[1]) - self.game.a_star.min_y)
            path = self.game.a_star.a_star_search([tile_pos[0], tile_pos[1]], [player_pos[0], player_pos[1]])
            if path:
                tile_found = True
                break

            fail += 1

            if fail > 40:
                return random.choice(tiles)
        return random_tile

    def Get_Random_Tile_With_Path_Tile(self, target_tile):
        tiles = []
        for tile in self.tiles_not_touching_wall.values():
            if tile.type != keys.floor:
                continue

            tiles.append(tile)
        tile_found = False
        random_tile = None
        fail = 0
        while not tile_found:
            random_tile = random.choice(tiles)
            tile_pos = (random_tile.pos[0] - self.game.a_star.min_x, random_tile.pos[1] - self.game.a_star.min_y)
            target_tile_pos = (target_tile.pos[0] - self.game.a_star.min_x, target_tile.pos[1] - self.game.a_star.min_y)
            path = self.game.a_star.a_star_search([tile_pos[0], tile_pos[1]], [target_tile_pos[0], target_tile_pos[1]])
            if path:
                tile_found = True
                break

            fail += 1

            if fail > 40:
                return None
        return random_tile
    
    def Clear_Tilemap(self):
        self.tilemap.clear()
        self.offgrid_tiles.clear()
        self.minimap.Clear()

    
    # Render function that shows the entire screen
    # Not really used
    def Render(self, surf, offset=(0, 0)):
        for tile in self.tilemap.values():
            surf.blit(self.game.assets[tile.type][tile.variant], (tile.scaled_pos[0] - offset[0], tile.scaled_pos[1] - offset[1]))

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



    def Add_Tile_To_Minimap(self, tile):
        if not tile.Add_To_Minimap():
            return False
        
        self.minimap.Add_Tile_To_Minimap(tile)
        return True

    def Render_Minimap(self, surf):
        self.minimap.Render(surf)
