from scripts.entities.items.runes.rune import Rune
import math
import pygame
from scripts.engine.assets.keys import keys

class Projectile_Rune(Rune):
    def __init__(self, game, type, pos, power, soul_cost):
        super().__init__(game, type, pos, power, soul_cost)
        self.effect = None
        self.charge = 0

    
    def Activate(self):
        if not super().Activate():
            return
        self.clicked = True
   

    def Update(self):
        super().Update()

        if not self.clicked:
            return 
        
        self.Handle_Shooting()
        if self.game.mouse.right_click:
            self.clicked = False
        return

    def Handle_Shooting(self):
        if not self.game.mouse.left_click or self.activate_cooldown:
            self.Reset_Charge()

            return
        
        # Handle intial setup
        if not self.charge:
            if self.game.player.Get_Total_Available_Souls() < self.current_soul_cost:
                return
            self.Set_Charge()
            self.Set_Activate_Cooldown(self.activate_cooldown_max )
            self.Compute_Souls_Cost()
        
        # Handle shooting
        if self.charge:
            self.game.player.Attack_Direction_Handler()
            self.Generate_Projectile()
            return
        

    def Set_Charge(self):
        self.charge = 1

    def Reset_Charge(self):
        self.charge = 0

    def Generate_Projectile(self):
        pass

    def Render_Animation(self, surf, offset=(0, 0)):
        if not self.clicked:
            return
        
        temp_surf = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
        # Draw a line on the temporary surface
        player_pos = (self.game.player.rect().center[0] - offset[0], self.game.player.rect().center[1] - offset[1])
        mouse_pos = (self.game.mouse.player_mouse[0] - offset[0], self.game.mouse.player_mouse[1] - offset[1])

        distance =  math.sqrt((player_pos[0] - mouse_pos[0]) ** 2 + (player_pos[1] - mouse_pos[1]) ** 2)
        alpha = 160
        if distance > 100:
            alpha = 50

        light_grey = (211,211,211, alpha)

        pygame.draw.line(temp_surf, light_grey, player_pos, mouse_pos, 2) 

        surf.blit(temp_surf, (0, 0))

    