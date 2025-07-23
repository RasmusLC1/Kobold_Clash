import pygame
import random
from scripts.engine.keys.keys import keys
import math

TILESIZE = 32

class Decoration_Initialiser():
    def __init__(self, game):
        self.game = game
        self.tiles_not_touching_walls = self.game.tilemap.tiles_not_touching_wall
        self.floor_tiles = {}
        self.Get_Floor_Tiles()
        self.decorations = {}
        self.Spawn_Decorations()
    
    def Get_Floor_Tiles(self):
        for tile_key, tile in self.game.tilemap.tilemap.items():
            if keys.floor in tile.type:
                self.floor_tiles[tile_key] = tile 

    def Spawn_Decorations(self):
        self.Spawn_Chests()
        self.Spawn_Vase()
        self.Spawn_Lightsource()

    def Spawn_Chests(self):
        amount = random.randint(10, 20)
        self.Find_Floor_Tiles(keys.chest, amount)

    def Spawn_Vase(self):
        amount = random.randint(20, 30)
        self.Find_Floor_Tiles(keys.vase, amount)

    def Spawn_Lightsource(self):
        # Ensure the light_source key exists in the decorations dictionary
        if keys.light_source not in self.decorations:
            self.decorations[keys.light_source] = []

        torch_tiles = []  # Keeps track of already placed torch positions (in tile coordinates)
        density = 40      # Controls how sparse the torch placement is (lower = more torches)

        # Convert floor_tiles to a list to avoid runtime errors from modifying the dict during iteration
        for tile_key, tile in list(self.floor_tiles.items()):
            # Skip tiles that already have entities on them
            if tile.entities:
                continue

            i, j = tile.pos 

            # Random chance to try placing a torch at this tile
            if random.randint(0, density) == 1:
                too_close = False

                # Check distance to all previously placed torches
                for torch_pos in torch_tiles:
                    if math.hypot(i - torch_pos[0], j - torch_pos[1]) < 8:
                        too_close = True
                        break  # Too close to an existing torch, skip placement

                # If no nearby torch found, place one here
                if not too_close:
                    torch_tiles.append((i, j))  # Track this torch position
                    self.decorations[keys.light_source].append((i * TILESIZE, j * TILESIZE))
                    del self.floor_tiles[tile_key]




    def Find_Floor_Tiles(self, key, amount):
        spawns = 0
        fail = 0
        while spawns < amount:
            
            if fail > amount:
                return

            tile_key, floor_tile = random.choice(list(self.floor_tiles.items()))
            
            if floor_tile.entities:
                fail += 1
                continue
            
            del self.floor_tiles[tile_key]

            if key not in self.decorations:
                self.decorations[key] = []

            self.decorations[key].append((floor_tile.pos[0] * TILESIZE, floor_tile.pos[1] * TILESIZE))

            spawns += 1

