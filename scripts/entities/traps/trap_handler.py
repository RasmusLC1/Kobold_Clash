
from scripts.engine.keys.keys import keys
from .trap_spawner import Trap_Spawner


class Trap_Handler:
    def __init__(self, game):
        self.game = game
        self.traps = []
        self.nearby_traps = []
        self.saved_data = {}
        self.nearby_traps_cooldown = 0
        self.trap_spawner = None

    def Initialise(self):
        self.trap_spawner = Trap_Spawner(self.game)

    def Spawn_Traps(self):
        self.traps = self.trap_spawner.Initialise()


    def Save_Trap_Data(self):
        for trap in self.traps:
            trap.Save_Data()
            self.saved_data[trap.ID] = trap.saved_data

    def Load_Data(self, data):
        if not self.trap_spawner:
            self.Initialise()


        for item_id, item_data in data.items():
            if not item_data:
                continue
            type = item_data[keys.type]
            pos = item_data[keys.pos]
            try: 
                self.trap_spawner.Spawn_Traps(pos, type, item_data)
            except Exception as e:
                print("DATA WRONG TRAPHANDLER", item_data, e)

        self.traps = self.trap_spawner.traps

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



    def Find_Nearby_Traps(self, entity, max_distance):
        return self.game.tilemap.Search_Nearby_Tiles(max_distance, entity.pos, keys.trap, entity.ID)

    def Find_Traps_Near_Player(self):
        nearby_traps = []
        player = self.game.player
        min_trap_distance = 200*200
        player_pos = player.pos
        for trap in self.traps:
            # Calculate the Euclidean distance

            dx = player_pos[0] - trap.pos[0]
            dy = player_pos[1] - trap.pos[1]
            if dx*dx + dy*dy < min_trap_distance:
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
        trap.Remove_Tile()
        if trap in self.traps:
            self.traps.remove(trap)
        if trap in self.nearby_traps:
            self.nearby_traps.remove(trap)
        del(trap)

    def Add_Trap(self, trap):
        self.traps.append(trap)



    