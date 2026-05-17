from scripts.entities.textbox.effect_textbox import Effect_Textbox
import pygame
from scripts.engine.keys.keys import keys

# Effect icons are only used by the player for UI
# active check handled by if they have an effect
class Effect_Icon():
    def __init__(self, game):
        self.game = game
        self.effect = None
        self.pos = (-999, -999)
        self.size = (20, 20)
        self.icon_text = None
        self.textbox = Effect_Textbox(self)

    def Update(self):
        self.Update_Effect_Text()

        if self.effect not in self.game.player.effects.active_effects:
            return True
        
        return False


    def Set_Effect(self, effect):
        self.effect = effect
        # Set Icon text to none if there is no effect
        self.Update_Effect_Text()
    
    def Update_Effect_Text(self):
        if self.effect:
            self.icon_text = f"{self.effect.effect_type} {self.effect.effect_strength}" 
        else:
            self.icon_text = None

    def Set_Position(self, pos):
        self.pos = pos

    def Update_Y_Position(self, adjustment):
        self.pos = (self.pos[0], self.pos[1] - adjustment)

    def Set_Active(self, pos, effect):
        self.Set_Position(pos)
        self.Set_Effect(effect)

    def Disable(self):
        self.Set_Active((-999, -999), None)

    
    def Handle_Mouse_Collision(self, surf):
        if not self.Check_Mouse_Collision():
            return
        
        self.textbox.Render(surf, self.pos, self.game.render_scroll) 
    
    
    def Check_Mouse_Collision(self):
        return self.rect().colliderect(self.game.mouse.rect_pos(self.game.render_scroll))


    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def Render(self, surf):
        if not self.effect:
            return
        
        self.Handle_Mouse_Collision(surf)

        self.game.mixed_symbols.Render_Mixed_Text(surf, self.icon_text, self.pos)
