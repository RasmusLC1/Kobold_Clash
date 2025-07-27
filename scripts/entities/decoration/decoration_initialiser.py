import pygame
import random
from scripts.engine.keys.keys import keys
import math

TILESIZE = 32
NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]

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


    # Spawn large objects first as they need more space, therefore it's harder to
    # find space for them if there's a lot of small objects scattered around
    def Spawn_Decorations(self):
        self.Spawn_Lightsource()
        self.Spawn_Rooms()
        self.Spawn_Large_Objects()
        self.Spawn_Small_Objects()


    def Spawn_Large_Objects(self):
        self.Spawn_Portal_Shrine()
        self.Spawn_Effigy_Tomb()
        self.Spawn_Hunter_Shrine()
        self.Spawn_Sacrifice_Shrine()
        self.Spawn_Soul_Well()

    def Spawn_Small_Objects(self):
        self.Spawn_Chests()
        self.Spawn_Vase()
        self.Spawn_Teleport()

    def Spawn_Chests(self):
        amount = random.randint(5, 10)
        self.Find_Floor_Tiles(keys.chest, amount)

    def Spawn_Vase(self):
        amount = random.randint(20, 30)
        self.Find_Floor_Tiles(keys.vase, amount)

    def Spawn_Weapon_Rack(self):
        amount = random.randint(20, 30)
        self.Find_Floor_Tiles(keys.vase, amount)

    def Spawn_Teleport(self):
        amount = random.randint(20, 30)
        if amount % 2:
            amount += 1
        print(amount)
        self.Find_Floor_Tiles(keys.teleportation_circle, amount)

    def Spawn_Effigy_Tomb(self):
        amount = random.randint(10, 15)
        self.Find_Floor_Tiles_Large_Object(keys.effigy_tomb, amount)

    def Spawn_Hunter_Shrine(self):
        amount = random.randint(2, 4)
        self.Find_Floor_Tiles_Large_Object(keys.hunter_shrine, amount)

    def Spawn_Sacrifice_Shrine(self):
        self.Find_Floor_Tiles_Large_Object(keys.sacrifice_shrine, 2)

    
    def Spawn_Portal_Shrine(self):
        self.Find_Floor_Tiles_Large_Object(keys.portal_shrine, 1, True)

    def Spawn_Soul_Well(self):
        self.Find_Floor_Tiles_Large_Object(keys.soul_well, 2, True)


    # TODO: Might need a seperate class for handling rooms
    def Spawn_Rooms(self):
        return
        self.Spawn_Library()
        self.Spawn_Loot_Room()
        self.Spawn_Boss_Room()


    def Spawn_Library(self):
        libraries = self.game.tilemap.extract([(keys.room, keys.library)])
        for library in libraries:
            self.Spawn_Library_Decoration(library)
        return
    
    def Spawn_Library_Decoration(self, library):
        print(library)
        return
        start_y = library.start_y
        size_y = library.size_y
        start_x = library.size_x
        size_x = library.size_x
        door_location = library.door_location
        tilemap = self.game.tilemap
        loot_count = 0
        table_spawned = False
        self.decorations[keys.bookshelf] = []
        self.decorations[keys.potion_table] = []

        for y in range(start_y + 1, start_y + size_y - 1):
            # Prevent bookhelfs from spawning on same x and y axis as the door
            if y == door_location[1]:
                continue
            for x in range(start_x + 1, start_x + size_x -1):
                if x == door_location[0]:
                    continue
                tile_key = (x, y)
                tile = tilemap.Current_Tile(tile_key)

                if tile.contains_decoration:
                    continue

                spawn_loot = random.randint(0, loot_count)
                if spawn_loot == 0: # guranteed to spawn at least one bookshelf since count starts at 0
                    loot_count += 1
                    self.decorations[keys.bookshelf].append(tile_key)

                    continue
                
                # Spawn a single table
                if not table_spawned:
                    table_spawned = True
                    loot_count += 1
                    self.decorations[keys.potion_table].append(tile_key)
                    continue


    def Spawn_Loot_Room(self):
        libraries = self.game.tilemap.extract([(keys.room, keys.loot_room)])


    def Spawn_Boss_Room(self):
        libraries = self.game.tilemap.extract([(keys.room, keys.boss_room)])


    def Spawn_Lightsource(self):
        # Ensure the light_source key exists in the decorations dictionary
        if keys.light_source not in self.decorations:
            self.decorations[keys.light_source] = []

        torch_tiles = []  # Keeps track of already placed torch positions (in tile coordinates)
        density = 40      # Controls how sparse the torch placement is (lower = more torches)
        tilemap = self.game.tilemap.tilemap

        # Convert floor_tiles to a list to avoid runtime errors from modifying the dict during iteration
        for tile_key, tile in list(self.floor_tiles.items()):
            # Skip tiles that already have entities on them
            if tile.contains_decoration:
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
                    tilemap[tile_key].Set_Contains_Decoration(True)
                    del self.floor_tiles[tile_key]




    def Find_Floor_Tiles(self, key, amount, check_for_path_to_player = False):
        spawns = 0
        fail = 0
        tilemap_dic = self.game.tilemap.tilemap
        player_pos = self.game.player.pos
        keys = []
        self.decorations[key] = []

        while spawns < amount:
            
            if fail > amount and fail > 20:
                return

            tile_key, floor_tile = random.choice(list(self.floor_tiles.items()))
            del self.floor_tiles[tile_key]
            
            if floor_tile.contains_decoration:
                fail += 1
                continue
            

            if not self.Check_Path_Finding_To_Player(check_for_path_to_player, player_pos, floor_tile):
                fail += 1
                continue
            

            tilemap_dic[tile_key].Set_Contains_Decoration(True)

            tile_pos = (floor_tile.pos[0] * TILESIZE, floor_tile.pos[1] * TILESIZE)
            self.decorations[key].append(tile_pos)

            spawns += 1
            keys.append(floor_tile.pos)

        return keys


    def Find_Floor_Tiles_Large_Object(self, key, amount, check_for_path_to_player = False):
        spawns = 0
        fail = 0

        keys = []
        player_pos = self.game.player.pos



        while spawns < amount:
            
            if fail > amount and fail > 20:
                return

            tile_key, floor_tile = random.choice(list(self.floor_tiles.items()))
            del self.floor_tiles[tile_key]
            
            if not self.Check_Path_Finding_To_Player(check_for_path_to_player, player_pos, floor_tile):
                fail += 1
                continue


            x, y = map(int, tile_key.split(";"))

            neigbour_tile_contains_decoration = self.Check_Neighbours(x, y)
            
            if not neigbour_tile_contains_decoration:
                fail += 1
                continue
            
            self.Set_Decoration_Neighbours(x, y)

            if key not in self.decorations:
                self.decorations[key] = []

            self.decorations[key].append((floor_tile.pos[0] * TILESIZE, floor_tile.pos[1] * TILESIZE))

            spawns += 1
            keys.append(floor_tile.pos)

        return keys
    

    def Check_Path_Finding_To_Player(self, check_for_path_to_player, player_pos, floor_tile):
        if not check_for_path_to_player:
            return True
        
        dest_x = round(player_pos[0] // self.game.tilemap.tile_size) - self.game.a_star.min_x 
        dest_y = round(player_pos[1] // self.game.tilemap.tile_size) - self.game.a_star.min_y 

        src_x = floor_tile.pos[0] - self.game.a_star.min_x 
        src_y = floor_tile.pos[1] - self.game.a_star.min_y
        
        path = self.game.a_star.a_star_search([src_x, src_y], [dest_x, dest_y])
        if not path:
            return False
        return True
        


    def Check_Neighbours(self, x, y):
        tilemap = self.game.tilemap.tilemap

        for offset in NEIGHBOR_OFFSETS:
            nx, ny = x + offset[0], y + offset[1] # Get neigbour key
            neighbor_key = f"{nx};{ny}"

            if neighbor_key not in tilemap:
                continue

            neighbor_tile = tilemap[neighbor_key]

            if neighbor_tile.contains_decoration or neighbor_tile.physics:
                return False
            
        return True

    def Set_Decoration_Neighbours(self, x, y):
        tilemap = self.game.tilemap.tilemap

        for offset in NEIGHBOR_OFFSETS:
            nx, ny = x + offset[0], y + offset[1] # Get neigbour key
            neighbor_key = f"{nx};{ny}"

            if neighbor_key not in tilemap:
                continue

            tilemap[neighbor_key].Set_Contains_Decoration(True)

            if neighbor_key in self.floor_tiles:
                del self.floor_tiles[neighbor_key]

            