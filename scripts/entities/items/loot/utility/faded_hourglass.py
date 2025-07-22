from scripts.entities.items.loot.radius_effect_loot import Radius_Effect_Loot
import random
from scripts.engine.keys.keys import keys

class Faded_Hourglass(Radius_Effect_Loot):
    def __init__(self, game, pos):
        amount = random.randint(2, 4)
        super().__init__(game, keys.faded_hourglass, pos, 320, keys.utility, 4, amount)
        self.Set_Description()
        self.max_amount = 5
        self.slowdown_triggered = 0
        self.animation_cooldown = 20
        self.max_animation = 4
        self.slowdown_amount = 8
   

    def Set_Description(self):
        self.description = 'Slow nearby\n enemies'

    def Update(self, delta_time):
        self.Handle_Slowdown(delta_time)
        return super().Update(delta_time)

    def Handle_Slowdown(self, delta_time):
        if self.slowdown_triggered <= 0:
            return
        
        self.slowdown_triggered -= delta_time

        if self.slowdown_triggered <= 0:
            return
        
        for enemy in self.nearby_entities:
            enemy.Remove_Effect(keys.slow, self.slowdown_amount)

        self.nearby_entities = None

    # If out of animations, reset the hourglass
    def Reset_Hourglass(self):
        self.amount -= 1

        if self.amount:
            self.clicked = False
            self.Set_Description() # Update description
            return
        
        self.game.item_handler.Remove_Item(self, True)
        self.game.inventory.Remove_Item(self)
    
    # The update function in the inventory
    def Update_In_Inventory(self):
        if not super().Update_In_Inventory():
            return False
        
        if self.slowdown_triggered:
            return False

        if self.game.mouse.left_click:
            self.Slow_Enemies()

        return True


    def Render_Line(self, surf, offset, alpha):
        pass

    # Effect of opening door on key
    def Slow_Enemies(self):
        self.Find_Nearby_Entities_Mouse()
        self.slowdown_triggered = 3
        for enemy in self.nearby_entities:
            enemy.Set_Effect(keys.slow, self.slowdown_amount)
        self.Reset_Hourglass()

        self.game.sound_handler.Play_Sound(self.type, 1)

