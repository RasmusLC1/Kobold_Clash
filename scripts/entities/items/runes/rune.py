from scripts.entities.items.item import Item
import pygame
import math
from scripts.entities.textbox.rune_textbox import Rune_Textbox
from scripts.engine.keys.keys import keys
import traceback


class Rune(Item):
    def __init__(self, game, type, pos, soul_cost, power, animation_time_max = 0.5, animation_size_max = 15):
        self.player = game.player
        self.menu_pos = pos
        self.upgrade_cost = math.ceil(soul_cost / 3)
        self.Initialise_Upgrades(soul_cost, power)
        self.animation_time = 0
        self.animation_time_max = animation_time_max
        self.animation_size = 0
        self.animation_size_max = animation_size_max
        self.effect = type.replace('_rune', '')
        self.cost_to_buy = soul_cost // 2 * power // 2
        self.activate_cooldown = 0
        self.activate_cooldown_max = 5
        self.clicked = False # Used for projectiles
        super().__init__(game,  type, keys.rune, pos, size=(16, 16), amount=1, max_amount=1, add_to_tile=False, rarity_value=soul_cost, durability=100, max_durability=100)


    def Save_Data(self):
        super().Save_Data()
        self.saved_data['effect'] = self.effect
        self.saved_data['upgrade_cost'] = self.upgrade_cost
        self.saved_data['power'] = self.power
        self.saved_data['soul_cost'] = self.soul_cost
        self.saved_data['menu_pos'] = self.menu_pos
        return self.saved_data
    
    def Load_Data(self, data):
        super().Load_Data(data)
        self.effect = data['effect'] 
        self.upgrade_cost = data['upgrade_cost'] 
        self.power = data['power']
        self.soul_cost = data['soul_cost'] 
        self.menu_pos = data['menu_pos']

    
    def Update(self, delta_time):
        self.Update_Activate_Cooldown(delta_time)
        return super().Update(delta_time)
    
    # Calls when the rune is activated, starts by checking for cooldown, then
    # Checks defauls activation is valid, then checks if the player can pay the souls
    # Then trigger the effect
    def Activate(self):
        if self.activate_cooldown:
            return False
        if not super().Activate():
            return False
        if self.player.Get_Total_Available_Souls() < self.soul_cost:
            return False
        self.Trigger_Effect()

        return True

    # Add the player's current power level to the runes power and checks if it is
    # Valid. If yes then it triggers the rune and subtract the cost
    def Trigger_Effect(self):
        if self.player.Set_Effect(self.effect, self.power + self.player.rune_power):
            self.Trigger_Rune()

    # Trigger the rune, cost already verified as possible in activate
    def Trigger_Rune(self):
        self.Compute_Souls_Cost()
        self.Set_Animation_Time()
        self.Reset_Animation_Size()
        self.Set_Activate_Cooldown(self.activate_cooldown_max)
        self.player.weapon_handler.Set_Attack_Lock(True)

        durability_damage = int(max(1, self.power // 2))
        self.Decrease_Durability(durability_damage)
        self.clicked = False

    
    def Compute_Souls_Cost(self):
        arcane_effect = self.player.Get_Acane_Conduit()
        if arcane_effect:
            self.player.Decrease_Souls(max(1, self.soul_cost - arcane_effect))
        else:
            self.player.Decrease_Souls(self.soul_cost)

    def Set_Menu_Pos(self, pos):
        self.menu_pos = pos

    
    def Set_Text_Box(self):
        self.text_box = Rune_Textbox(self)

    # Used to initialise rune
    def Initialise_Upgrades(self, soul_cost, power):
        
        self.power = power
        self.soul_cost = soul_cost



    def Remove_Rune_From_Inventory(self):
        pass

    def Modify_Souls_Cost(self, change):
        min_soul_cost = 1 # Reprevent soul cost from going to 0
        if self.player.Get_Total_Available_Souls() < self.upgrade_cost:
            return False
        if self.soul_cost + change < min_soul_cost:
            return False
        self.soul_cost += change
        return True

    def Upgrade_Cost(self):
        self.upgrade_cost = (5 * self.power**2) + (5 * self.power) + 30

        return True
    
    def Modify_Power(self, change):
        if self.player.Get_Total_Available_Souls() < self.upgrade_cost:
            return False
        self.Increase_Power(change)
        return True
    
    def Increase_Power(self, amount):
        for i in range(amount):
            self.power += 1
            self.Upgrade_Cost()
            
    
    def Update_Activate_Cooldown(self, delta_time):
        if self.activate_cooldown:
            self.activate_cooldown = max(0, self.activate_cooldown - delta_time)
            if self.activate_cooldown > 0:
                self.player.weapon_handler.Set_Attack_Lock(True)
            else:
                self.player.weapon_handler.Set_Attack_Lock(False)

            return

    # Updated in rune inventory when player's power is modified
    def Set_Description(self):
        self.description = (
                            f"{keys.souls} {self.soul_cost}\n"
                            f"{keys.power} {self.power + self.player.rune_power}\n"
                            f"Dur {self.durability}/{self.max_durability}\n"
                            f"{self.Calculate_Value()} {keys.gold}\n"
                        )  

    
    def Set_Activate_Cooldown(self, value):
        self.activate_cooldown = value

    def Set_Animation_Time(self):
        self.animation_time = self.animation_time_max

    def Reset_Animation_Size(self):
        self.animation_size = 0

    def Increase_Animation_Size(self):
        self.animation_size = min(self.animation_size + 0.1, self.animation_size_max)


    def Update_Animation(self, delta_time):
        if self.animation_time:
            self.animation_time = max(0, self.animation_time - delta_time)
            self.Increase_Animation_Size()
    
    # Defualt the Render function to render in inventory
    def Render_Menu(self, surf, scale = 1.5):
        item_image = pygame.transform.scale(self.game.assets[self.type][self.animation], (self.size[0] * scale, self.size[1] * scale))  
        surf.blit(item_image, (self.menu_pos[0], self.menu_pos[1]))

    def Set_Clicked(self, state):
        self.clicked = state
    
    def Render_Animation(self, surf, offset=(0, 0)):
        if not self.animation_time:
            return
        inversed_animation_size = (20 - self.animation_size) / 10 + 1
        
        self.game.symbols.Render_Symbol(surf, self.effect,  (self.player.pos[0] - offset[0] + 8 - inversed_animation_size, self.player.pos[1] - offset[1] - inversed_animation_size), inversed_animation_size)

    def Calculate_Value(self):
        return math.ceil(self.value * self.power)

    def Place_Down(self):
        self.game.item_handler.Remove_Rune_From_Active_Runes(self)
        self.Delete_Item()


    def Render_In_Bounds(self, player_pos, mouse_pos, surf, offset = (0,0)):
         # Copy image and set alpha
        entity_image =  pygame.transform.scale(self.entity_image.copy(), self.floor_size)

        # Create red overlay
        red_overlay = pygame.Surface(entity_image.get_size(), pygame.SRCALPHA)
        red_overlay.fill((255, 0, 0, 100))  # Red with transparency

        # Blit entity and red overlay
        pos = (mouse_pos[0] - offset[0], mouse_pos[1] - offset[1])
        surf.blit(entity_image, pos)
        surf.blit(red_overlay, pos)

    def Menu_Rect(self):
        return pygame.Rect(self.menu_pos[0], self.menu_pos[1], (self.size[0] * 1.5), (self.size[1] * 1.5))

    def Render_Floor(self, surf, offset=(0, 0)):
        
        if not self.Update_Light_Level():
            return
        
        self.Update_Dark_Surface()
        
        # Render the item
        if not self.rendered_image:
            self.Set_Sprite()
            if not self.rendered_image:
                print(self.type, vars(self))
                self.broken_rendering_counter += 1
                if self.broken_rendering_counter >= 10:
                      self.Delete_Item()
                return
        # Hack to render the runes above the plinth they're sitting on. Runes should
        # rarely be on floor, so it shouldn't affect other visuals
        surf.blit(self.rendered_image, (self.pos[0] - offset[0], self.pos[1] - offset[1] - 10)) 