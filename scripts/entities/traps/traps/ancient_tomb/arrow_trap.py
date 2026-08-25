from scripts.engine.keys.keys import keys
from scripts.entities.traps.trap import Trap
from .ancient_tomb_registry import register_trap

import random

COOLDOWN_MAX = 2

@register_trap(keys.arrow_trap, 0.2)
class Arrow_Trap(Trap):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.arrow_trap)
        self.attack_direction = (0, 0)
        self.Find_Direction()
        self.arrows = []
        self.Spawn_Arrows()
        self.next_available_arrow = 0
        if self.tile:
            self.tile.Set_Physics(True)

    def Save_Data(self):
        super().Save_Data()
        arrow_ids = []
        for arrow in self.arrows:
            arrow_ids.append(arrow.ID)
        self.saved_data['arrows'] = arrow_ids

    
    def Load_Data(self, data):
        super().Load_Data(data)

        arrow_ids = data['arrows']
        self.arrows.clear()
        item_handler = self.game.item_handler
        for arrow_id in arrow_ids:
            arrow = item_handler.Find_Item(arrow_id)
            if not arrow:
                arrow = item_handler.Spawn_Arrow_For_Trap((-999,-999))
            
            self.arrows.append(arrow)

    def Spawn_Arrows(self):
        item_handler = self.game.item_handler

        for _ in range(3):
            arrow = item_handler.Spawn_Arrow_For_Trap((-999,-999))
            arrow.pickup_allowed = False
            self.arrows.append(arrow)




    # Finds the longest direction
    def Find_Direction(self):
        tile_size = self.game.tilemap.tile_size
        directions = {
            (0, 1): 0,
            (1, 0): 0,
            (0, -1): 0,
            (-1, 0): 0,
        }

        for dir_x, dir_y in directions:
            distance = 0
            pos_x, pos_y = self.pos[0] // tile_size, self.pos[1] // tile_size

            while True:
                pos_x += dir_x
                pos_y += dir_y

                tile = self.game.tilemap.Current_Tile((pos_x, pos_y))

                if not tile:  # Still a valid tile
                    break

                if tile.physics:
                    break

                distance += 1

            directions[(dir_x, dir_y)] = distance
            if distance > 20:
                self.attack_direction = (dir_x, dir_y)
                return

        # Get the direction with the longest visible path
        self.attack_direction = max(directions, key=directions.get)

                

    def Update(self, delta_time):
        if not self.render:
            return False
        if not self.Update_Cooldown(delta_time):
            return False
        
        self.Shoot_Arrow()
        self.Check_If_Arrows_Need_Reset()
        return True


    def Shoot_Arrow(self):
        arrow_speed = 3
        arrow = self.arrows[self.next_available_arrow]

        if not arrow:
            print(arrow, self.arrows)
            return
        arrow.Set_Position(self.pos.copy())
        arrow.Set_Tile()
        arrow.Shooting_Setup(self, self.attack_direction)
        arrow.Initialise_Shooting(arrow_speed)
        self.next_available_arrow += 1
        if self.next_available_arrow >= len(self.arrows):
            self.next_available_arrow = 0

    def Check_If_Arrows_Need_Reset(self):
        for arrow in self.arrows:
            if arrow.shoot_distance or arrow.shoot_speed:
                continue
            arrow.Set_Position((-999, -999))

    def Update_Cooldown(self, delta_time):
        if self.entity_check_cooldown > 0:
            self.entity_check_cooldown -= delta_time
            return False

        self.entity_check_cooldown = random.uniform(COOLDOWN_MAX / 2, COOLDOWN_MAX)
        return True
    
    # Handle cooldown of entities in the trap seperately to ensure fast trigger on trap
    # but controlled damage
    def Update_Damage_Cooldown(self, delta_time):
        pass
    
    def Update_Trapped_Entities(self):
        pass
    
    def Find_Nearby_Entities(self):
        pass

    
    def Add_Entity(self, entity):
        pass
