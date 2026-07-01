from scripts.level_generation.cellular_automata import Cellular_Automata
from scripts.level_generation.noise_map import Noise_Map
from scripts.engine.tilemap.tilemap import Tilemap
from scripts.engine.a_star import A_Star
from scripts.level_generation.room_generation.level_structure import Level_Structure
from scripts.level_generation.rooms.spawn_boss_room import Spawn_Boss_Room
from scripts.level_generation.rooms.spawn_loot_room import Spawn_Loot_Room
from scripts.level_generation.rooms.spawn_lakes import Spawn_Lakes
from scripts.level_generation.entities.spawn_enemy import Spawn_Enemy
from scripts.level_generation.loot.weapon_spawner import Weapon_Spawner
from scripts.level_generation.loot.rune_spawner import Rune_Spawner
from scripts.level_generation.dungeon_enum_keys import *
import os

# TODO:  shrines, entrance and exit, keys 



class Dungeon_Generator():
    def __init__(self, game) -> None:
        self.game = game
        self.player_spawn = (0, 0)
        self.cellular_automata = Cellular_Automata()
        self.tile_size = 32
        self.player_spawn = (20, 20)
        self.offgrid_tiles = []
        self.a_star = A_Star(game)
        # TODO: IMPLEMENT MORE TRAPS AND ADD THEM HERE
        self.noise_map = Noise_Map()
        self.level_structure = Level_Structure(game)
        
        self.torches = []



    # Customise the internal map structure
    def Generate_Map(self, map_id):
        self.Update_Load_Menu(1)

        self.game.tilemap.Clear_Tilemap() # Clears tiles and offgrid
        self.cellular_automata.Create_Map()
        self.Update_Load_Menu(2)

        Spawn_Lakes.Spawn_Lakes(self.noise_map, self.cellular_automata, 7, FLOOR, LAVA, self.offgrid_tiles)
        size_x = self.cellular_automata.size_x
        size_y = self.cellular_automata.size_y
        
        self.Update_A_Star_Map()

        
        self.a_star.Set_Map('custom')
        self.Update_Load_Menu(3)

        # Spawn more loot rooms in lower levels of dungeon
        # TODO: PROPER LEVEL SYSTEM
        if not Spawn_Loot_Room.Spawn_Loot_Room(self.cellular_automata.map, size_x, size_y, map_id, self.player_spawn, self.A_Star_Search, self.offgrid_tiles):
            self.Generate_Map(map_id)
            return
        
        self.Update_A_Star_Map()

        self.Update_Load_Menu(4)

        Spawn_Boss_Room.Spawn_Boss_Room(self.cellular_automata.map, self.tile_size, size_x, size_y, self.player_spawn, self.A_Star_Search, self.offgrid_tiles)

        self.Update_A_Star_Map()

        # Call itself recursively and generate a new map if it fails to spawn enemies
        if not Spawn_Enemy.Enemy_Spawner(self.cellular_automata.map, self.tile_size, size_x, size_y, self.A_Star_Search, self.offgrid_tiles):
            self.Generate_Map(map_id)
            return
        
        self.Update_Load_Menu(5)
  

        Weapon_Spawner.Spawn_Weapons(self.cellular_automata.map, map_id, self.tile_size, size_x, size_y, self.offgrid_tiles)

        Rune_Spawner.Spawn_Runes(self.cellular_automata.map, map_id, self.tile_size, size_x, size_y, self.offgrid_tiles)

        tile_data = self.level_structure.Level_Structure(self.cellular_automata.map, self.tile_size, size_x, size_y, self.player_spawn, self.offgrid_tiles)

        self.Update_Load_Menu(6)
        self.game.tilemap.Convert_Dungeon_Generation_Dic_To_Tilemap(tile_data, self.offgrid_tiles)



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
  