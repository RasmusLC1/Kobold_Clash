from scripts.entities.traps.traps.spike import Spike
from scripts.entities.traps.traps.rubble import Rubble
from scripts.entities.traps.traps.bell_pressure_plate import Bell_Pressure_plate
from scripts.entities.traps.traps.spike_poisoned import Spike_Poisoned
from scripts.entities.traps.traps.soul_trap import Soul_Trap
from scripts.entities.traps.traps.spike_pit import Spike_Pit
from scripts.entities.traps.traps.fire_trap import Fire_Trap
from scripts.entities.traps.environment.lava import Lava
from scripts.entities.traps.environment.water import Water
from scripts.entities.traps.environment.ice import Ice
from scripts.entities.traps.traps.spider_web import Spider_Web
from scripts.entities.traps.traps.tomb_pressure_plate import Tomb_Pressure_Plate
from scripts.entities.traps.traps.arrow_trap import Arrow_Trap
from scripts.engine.keys.keys import keys
import math
import random

TILESIZE = 32
TRAP_DENSITY = 30 # Lower = more traps


TRAP_TABLE = { # Expand with new traps as needed
    keys.pit_trap : 0.4,
    keys.spike_poison_trap : 0.4,
    keys.spike_trap : 0.6,
    keys.rubble : 2,
    keys.tomb_pressure_plate : 0.2,
    keys.bell_pressure_plate : 0.3,
    # keys.soul_trap : 0.3,
    keys.arrow_trap : 2.3,
}

class Trap_Handler:
    def __init__(self, game):
        self.game = game
        self.traps = []
        self.nearby_traps = []
        self.saved_data = {}
        self.floor_tiles = {}
        self.traps_to_spawn = {}
        self.nearby_traps_cooldown = 0
        
    
    def Save_Trap_Data(self):
        for trap in self.traps:
            trap.Save_Data()
            self.saved_data[trap.ID] = trap.saved_data

    def Load_Data(self, data):
        for item_id, item_data in data.items():
            if not item_data:
                continue

            type = item_data[keys.type]
            pos = item_data[keys.pos]
            size = item_data['size']
            try: 
                self.Trap_Spawner(pos, type, size, item_data)
            except Exception as e:
                print("DATA WRONG", item_data, e)

    # Only update traps that are close t the player
    def Update(self, delta_time):
        if self.Update_Nearby_Traps_Cooldown(delta_time):
            self.nearby_traps.clear()
            self.nearby_traps = self.Find_Traps_Near_Player()

        self.Update_Nearby_Trap_Animation(delta_time)
        self.Update_Nearby_Traps_Logic(delta_time)

    def Update_Nearby_Trap_Animation(self, delta_time):
        if not self.nearby_traps:
            return
        for trap in self.nearby_traps:
            if not trap:
                continue
            trap.Animation_Update(delta_time)

    def Update_Nearby_Traps_Logic(self, delta_time):
        if not self.nearby_traps:
            return
        for trap in self.nearby_traps:
            trap.Update(delta_time)
    


    def Clear_Traps(self):
        self.traps.clear()
        self.nearby_traps.clear()
        self.saved_data.clear()


    def Initialise(self):
        self.Initialise_Traps()
        for trap_type, trap_positions in self.traps_to_spawn.items():
            for trap_pos in trap_positions:
                self.Trap_Spawner(trap_pos, trap_type)
        
        self.Spawn_Trap_Tiles()

    def Spawn_Trap_Tiles(self):
        for trap in self.game.tilemap.extract([(keys.lava_env, 0)].copy(), True):
            size = (self.game.assets[trap.type][0].get_width(), self.game.assets[trap.type][0].get_height())
            self.Trap_Spawner(trap.pos, trap.type)

        for trap in self.game.tilemap.extract([(keys.shallow_water_env, 0)].copy(), True):
            size = (self.game.assets[trap.type][0].get_width(), self.game.assets[trap.type][0].get_height())
            self.Trap_Spawner(trap.pos, trap.type)


        for trap in self.game.tilemap.extract([(keys.medium_water_env, 0)].copy(), True):
            size = (self.game.assets[trap.type][0].get_width(), self.game.assets[trap.type][0].get_height())
            self.Trap_Spawner(trap.pos, trap.type)

        for trap in self.game.tilemap.extract([(keys.deep_water_env, 0)].copy(), True):
            size = (self.game.assets[trap.type][0].get_width(), self.game.assets[trap.type][0].get_height())
            self.Trap_Spawner(trap.pos, trap.type)


        for trap in self.game.tilemap.extract([(keys.shallow_ice_env, 0)].copy(), True):
            size = (self.game.assets[trap.type][0].get_width(), self.game.assets[trap.type][0].get_height())
            self.Trap_Spawner(trap.pos, trap.type)


        for trap in self.game.tilemap.extract([(keys.medium_ice_env, 0)].copy(), True):
            size = (self.game.assets[trap.type][0].get_width(), self.game.assets[trap.type][0].get_height())
            self.Trap_Spawner(trap.pos, trap.type)

        for trap in self.game.tilemap.extract([(keys.deep_ice_env, 0)].copy(), True):
            size = (self.game.assets[trap.type][0].get_width(), self.game.assets[trap.type][0].get_height())
            self.Trap_Spawner(trap.pos, trap.type)


    def Trap_Spawner(self, pos, type, data = None):
        trap = None
        if keys.spike_trap == type:
            trap = self.Spawn_Spike_Trap(pos)

        elif type == keys.spike_poison_trap:
            trap = self.Spawn_Spike_Poisoned(pos)

        elif keys.pit_trap == type:
            trap = self.Spawn_Spike_Pit(pos)

        elif keys.rubble == type:
            trap = self.Spawn_Rubble(pos)

        elif keys.tomb_pressure_plate == type:
            trap = self.Spawn_Tomb_Pressure_Plate(pos)

        elif keys.bell_pressure_plate == type:
            trap = self.Spawn_Bell_Pressure_Plate(pos)

        elif keys.soul_trap == type:
            trap = self.Spawn_Soul_Trap(pos)

        elif keys.arrow_trap == type:
            trap = self.Spawn_Arrow_Trap(pos)

        elif keys.lava_env == type:
            trap = self.Spawn_Lava(pos)

        elif 'ice' in type:
            trap = self.Spawn_Ice(pos, type)

        elif 'water' in type:
            trap = self.Spawn_Water(pos, type)

        elif type == keys.fire_trap:
            trap = self.Spawn_Fire_Trap(pos)

        elif type == keys.spider_web:
            trap = self.Spawn_Spider_Web(pos)
        else:
            print("FAILED TO FIND TRAPTYPE", type)
        if not trap:
            return False
        
        if data:
            trap.Load_Data(data)

        self.traps.append(trap)
        return True



    
    def Spawn_Ice(self, pos, type):
        return Ice(self.game, pos, type)
    
    def Spawn_Water(self, pos, type):
        return Water(self.game, pos, type)
    
    def Spawn_Lava(self, pos):
        return Lava(self.game, pos)
    
    def Spawn_Fire_Trap(self, pos):
        return Fire_Trap(self.game, pos)
    
    def Spawn_Spike_Pit(self, pos):
        return Spike_Pit(self.game, pos)
    
    def Spawn_Spike_Poisoned(self, pos):
        return Spike_Poisoned(self.game, pos)
    
    def Spawn_Spike_Trap(self, pos):
        return Spike(self.game, pos)
    
    def Spawn_Rubble(self, pos):
        return Rubble(self.game, pos)
    
    def Spawn_Tomb_Pressure_Plate(self, pos):
        return Tomb_Pressure_Plate(self.game, pos)
    
    def Spawn_Arrow_Trap(self, pos):
        return Arrow_Trap(self.game, pos)

    def Spawn_Soul_Trap(self, pos):
        return Soul_Trap(self.game, pos)
    
    def Spawn_Bell_Pressure_Plate(self, pos):
        return Bell_Pressure_plate(self.game, pos)
    
    def Spawn_Spider_Web(self, pos):
        return Spider_Web(self.game, pos)
    

    def Find_Nearby_Traps(self, entity, max_distance):
        return self.game.tilemap.Search_Nearby_Tiles(max_distance, entity.pos, 'trap', entity.ID)

    def Find_Traps_Near_Player(self):
        nearby_traps = []
        player = self.game.player
        for trap in self.traps:
            # Calculate the Euclidean distance
            distance = math.sqrt((player.pos[0] - trap.pos[0]) ** 2 + (player.pos[1] - trap.pos[1]) ** 2)
            if distance < 200:
                nearby_traps.append(trap)
        
        return nearby_traps


    def Reset_Nearby_Traps_Cooldown(self):
        self.nearby_traps_cooldown = 1

    def Update_Nearby_Traps_Cooldown(self, delta_time):
        if self.nearby_traps_cooldown:
            self.nearby_traps_cooldown = max(0, self.nearby_traps_cooldown - delta_time)
            return False
        self.nearby_traps_cooldown = 1 # Update nearby traps every second
        return True

    def Remove_Trap(self, trap):
        self.game.ray_caster.Remove_Trap(trap)
        if trap in self.traps:
            self.traps.remove(trap)
        if trap in self.nearby_traps:
            self.nearby_traps.remove(trap)
        del(trap)

    def Add_Trap(self, trap):
        self.traps.append(trap)


    def Get_Floor_Tiles(self):
        for tile_key, tile in self.game.tilemap.tilemap.items():
            if keys.floor in tile.type:
                self.floor_tiles[tile_key] = tile 

    def Initialise_Traps(self):
        self.Get_Floor_Tiles()
        trap_tiles = []  # Keeps track of already placed trap positions (in tile coordinates)
        tilemap = self.game.tilemap.tilemap


        # Convert floor_tiles to a list to avoid runtime errors from modifying the dict during iteration
        for tile_key, tile in list(self.floor_tiles.items()):
            # Skip tiles that already have entities on them
            if tile.contains_decoration:
                del self.floor_tiles[tile_key]
                continue

            i, j = tile.pos 

            # Random chance to try placing a trap at this tile
            if random.randint(0, TRAP_DENSITY) == 1:
                too_close = False

                # Check distance to all previously placed trapes
                for trap_pos in trap_tiles:
                    if math.hypot(i - trap_pos[0], j - trap_pos[1]) < 8:
                        too_close = True
                        break  # Too close to an existing trap, skip placement

                # If no nearby trap found, place one here
                if too_close:
                    continue

                trap_tiles.append((i, j))  # Track this trap position
                trap = random.choices(
                    population=list(TRAP_TABLE.keys()),
                    weights=list(TRAP_TABLE.values()),
                    k=1
                )[0]

                if trap not in self.traps_to_spawn:
                    self.traps_to_spawn[trap] = []

                self.traps_to_spawn[trap].append((i * TILESIZE, j * TILESIZE))
                tilemap[tile_key].Set_Contains_Decoration(True)
                del self.floor_tiles[tile_key]