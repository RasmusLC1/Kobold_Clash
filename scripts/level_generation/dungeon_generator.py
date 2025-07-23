from scripts.level_generation.cellular_automata import Cellular_Automata
from scripts.level_generation.noise_map import Noise_Map
from scripts.engine.tilemap.tilemap import Tilemap
from scripts.engine.a_star import A_Star
from scripts.level_generation.room_generation.level_structure import Level_Structure
from scripts.level_generation.rooms.spawn_boss_room import Spawn_Boss_Room
from scripts.level_generation.rooms.spawn_loot_room import Spawn_Loot_Room
from scripts.level_generation.rooms.spawn_library import Spawn_Library
from scripts.level_generation.rooms.spawn_lakes import Spawn_Lakes
from scripts.level_generation.decoration_spawner.portal_shrine_spawner import Portal_Shrine_Spawner
from scripts.level_generation.decoration_spawner.hunter_shrine_spawner import Hunter_Shrine_Spawner
from scripts.level_generation.decoration_spawner.sacrifice_shrine_spawner import Sacrifice_Shrine_Spawner
from scripts.level_generation.entities.spawn_player import Spawn_Player
from scripts.level_generation.entities.spawn_enemy import Spawn_Enemy
from scripts.level_generation.decoration_spawner.trap_spawner import Trap_Spawner
from scripts.level_generation.decoration_spawner.chest_spawner import Chest_Spawner
from scripts.level_generation.decoration_spawner.vase_spawner import Vase_Spawner
from scripts.level_generation.decoration_spawner.potion_table import Potion_Table_Spawner
from scripts.level_generation.decoration_spawner.soul_well_spawner import Soul_Well_Spawner
from scripts.level_generation.decoration_spawner.teleport_circle import Teleportation_Circle_Spawner
from scripts.level_generation.decoration_spawner.effigy_tomb_spawner import Effigy_Tomb_Spawner
from scripts.level_generation.loot.weapon_spawner import Weapon_Spawner
from scripts.level_generation.loot.rune_spawner import Rune_Spawner
from scripts.level_generation.dungeon_enum_keys import *
import os
import random
from scripts.engine.keys.keys import keys

# TODO:  shrines, entrance and exit, keys 



class Dungeon_Generator():
    def __init__(self, game) -> None:
        self.game = game
        self.player_spawn = (0, 0)
        self.cellular_automata = Cellular_Automata()
        self.tile_size = 32
        self.tilemap = Tilemap(self, tile_size=self.tile_size)
        self.a_star = A_Star()
        # TODO: IMPLEMENT MORE TRAPS AND ADD THEM HERE
        self.noise_map = Noise_Map()
        
        self.torches = []



    # Customise the internal map structure
    def Generate_Map(self, map_id):
        self.Update_Load_Menu(1)

        self.tilemap.Clear_Tilemap()
        self.cellular_automata.Create_Map()
        self.Update_Load_Menu(2)

        Spawn_Lakes.Spawn_Lakes(self.noise_map, self.cellular_automata, 7, FLOOR, LAVA, self.tilemap.offgrid_tiles)
        size_x = self.cellular_automata.size_x
        size_y = self.cellular_automata.size_y
        
        self.Update_A_Star_Map()

        self.player_spawn = Spawn_Player.Player_Spawn(self.tile_size, self.tilemap)
        self.a_star.Set_Map('custom')
        Trap_Spawner.Spawn_Traps(self.cellular_automata.map, 1, size_x, size_y)
        self.Update_Load_Menu(3)

        # Spawn more loot rooms in lower levels of dungeon
        # TODO: PROPER LEVEL SYSTEM
        if not Spawn_Loot_Room.Spawn_Loot_Room(self.cellular_automata.map, size_x, size_y, map_id, self.player_spawn, self.A_Star_Search, self.tilemap.offgrid_tiles):
            self.Generate_Map(map_id)
            return
        
        if not Spawn_Library.Spawn_Library(self.cellular_automata.map, size_x, size_y, map_id, self.player_spawn, self.A_Star_Search, self.tilemap.offgrid_tiles):
            self.Generate_Map(map_id)
            return

        self.Update_A_Star_Map()

        self.Update_Load_Menu(4)

        Spawn_Boss_Room.Spawn_Boss_Room(self.cellular_automata.map, self.tile_size, size_x, size_y, self.player_spawn, self.A_Star_Search, self.tilemap.offgrid_tiles)

        self.Update_A_Star_Map()

        # Call itself recursively and generate a new map if it fails to spawn enemies
        if not Spawn_Enemy.Enemy_Spawner(self.cellular_automata.map, self.tile_size, size_x, size_y, self.A_Star_Search, self.tilemap.offgrid_tiles):
            self.Generate_Map(map_id)
            return
        
        self.Update_Load_Menu(5)
        
        if not self.Spawn_Decoration(map_id, size_x, size_y):
            self.Generate_Map(map_id)
            return

        self.Update_A_Star_Map()


        Weapon_Spawner.Spawn_Weapons(self.cellular_automata.map, map_id, self.tile_size, size_x, size_y, self.tilemap.offgrid_tiles)

        Rune_Spawner.Spawn_Runes(self.cellular_automata.map, map_id, self.tile_size, size_x, size_y, self.tilemap.offgrid_tiles)

        Level_Structure.Level_Structure(self.cellular_automata.map, self.tile_size, size_x, size_y, self.tilemap)

        self.Update_Load_Menu(6)
        self.tilemap.save(f'data/maps/{map_id}.json')

    def Spawn_Decoration(self, map_id, size_x, size_y):
        # Chest_Spawner.Spawn_Chest(self.cellular_automata.map, map_id, size_x, size_y, self.tile_size, self.tilemap.offgrid_tiles, self.A_Star_Search)
        
        # Vase_Spawner.Spawn_Vase(self.cellular_automata.map, map_id, size_x, size_y, self.tile_size, self.tilemap.offgrid_tiles, self.A_Star_Search)
        
        if not Portal_Shrine_Spawner.Spawn_Portal_Shrine(self.cellular_automata.map, self.player_spawn, size_x, size_y, self.tile_size, self.A_Star_Search, self.tilemap.offgrid_tiles):
            return False
        
        Hunter_Shrine_Spawner.Spawn_Hunter_Shrine(self.cellular_automata.map, size_x, size_y, self.tile_size, self.tilemap.offgrid_tiles, self.A_Star_Search)
        
        Sacrifice_Shrine_Spawner.Spawn_Sacrifice_Shrine(self.cellular_automata.map, size_x, size_y, self.tile_size, self.tilemap.offgrid_tiles, self.A_Star_Search)

        Soul_Well_Spawner.Spawn_Soul_Well(self.cellular_automata.map, map_id, size_x, size_y, self.tile_size, self.tilemap.offgrid_tiles, self.A_Star_Search)

        Teleportation_Circle_Spawner.Spawn_Teleport_Circle(self.cellular_automata.map, size_x, size_y, self.tile_size, self.tilemap.offgrid_tiles, self.A_Star_Search)
        
        Effigy_Tomb_Spawner.Spawn_Effigy_Tomb(self.cellular_automata.map, map_id, size_x, size_y, self.tile_size, self.tilemap.offgrid_tiles, self.A_Star_Search)

        Effigy_Tomb_Spawner.Spawn_Effigy_Tomb(self.cellular_automata.map, map_id, size_x, size_y, self.tile_size, self.tilemap.offgrid_tiles, self.A_Star_Search)

        return True


    def Update_Load_Menu(self, value):
        self.game.menu_handler.Loading_Menu_Update(value)

    def Update_A_Star_Map(self):
        self.a_star.Setup_Custom_Map(self.cellular_automata.map, self.cellular_automata.size_x, self.cellular_automata.size_y)

    def A_Star_Search(self, start_x, start_y):
        return self.a_star.a_star_search_no_diagonals([start_x, start_y], [self.player_spawn[0], self.player_spawn[1]], 'custom')
    

    def Delete_Map_File(self, file_path):

        # Check if the file exists
        if os.path.exists(file_path):
            os.remove(file_path)
  