from scripts.entities.items.weapons.magic_attacks.vampiric.soul_reap import Soul_Reap
import math
from scripts.engine.keys.keys import keys


class Soul_Reap_Shooter():
    def __init__(self, game):
        self.game = game


    def Spawn_Soul_Reap(self, entity, damage):
        speed = 1.5
        max_range = 240

        # Calculate the base angle using atan2(y, x)
        base_angle = math.atan2(entity.attack_direction[1], entity.attack_direction[0])

        pos_x = math.cos(base_angle) * speed
        pos_y = math.sin(base_angle) * speed
        direction = (pos_x, pos_y)
        ice_particle = Soul_Reap(
                self.game,
                entity.rect(),
                damage,
                speed,
                max_range,
                100,
                direction,  # Pass the direction here
                entity
            )
        
        self.game.item_handler.Add_Item(ice_particle)