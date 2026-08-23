from scripts.entities.decoration.shared.loot_container.loot_container import Loot_Container
from scripts.engine.keys.keys import keys
import math

# Spawns the items when player gets near and displays it
class Display_Loot_Container(Loot_Container):
    def __init__(self, game, type, pos, size = (32, 32), destructable = False, health = 100, destruction_sound = None, destruction_clatter = 500, max_animation = 0) -> None:
        super().__init__(game, type, pos, size, destructable, health, destruction_sound, destruction_clatter, max_animation)
        self.distance_cooldown = 0
        self.radius = 15

        
    def Update(self, delta_time):
        if self.Calculate_Distance():
            self.empty = True
            self.Drop_Loot()
        return super().Update(delta_time)

    def Drop_Loot(self):
        pass


    def Calculate_Distance(self):
        if self.empty:
            return
        
        if self.distance_cooldown > 0:
            self.distance_cooldown -= 1
            return False
        # Calculate distance and set the cooldown to the distance to avoid computation
        distance = math.sqrt((self.game.player.pos[0] - self.pos[0]) ** 2 + (self.game.player.pos[1] - self.pos[1]) ** 2)        
        self.distance_cooldown = distance // 10
        if distance < self.radius * 16:
            return True
        
        return False