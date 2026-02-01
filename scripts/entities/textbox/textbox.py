import pygame
from scripts.engine.keys.keys import keys

class Text_Box():
    def __init__(self, entity) -> None:
        self.entity = entity
        self.render = False
        self.x_size = 0
        self.y_size = 0
        self.Set_Headline_Font()
        self.rectangle_surface = self.Set_Text_Box_Size()

        self.mixed_symbols = self.entity.game.mixed_symbols

    def Update(self, hitbox_1, hitbox_2):
        # Handle when entity is in inventory
        if hitbox_1.colliderect(hitbox_2):
            self.render = True
            return True
        
        if self.render:
            self.render = False

        return False

    def Edit_Entity_Name(self):
        entity_name = self.entity.type
        entity_name = entity_name.replace('_resistance', ' res')
        return entity_name
    
    def Set_Text_Box_pos(self, offset):
        text_box_pos = (0,0)
        # Render entitybox different depending on if it's picked up or not
        if self.entity.picked_up:
            text_box_pos = (self.entity.pos[0], self.entity.pos[1] -  self.y_size)
        else:
            text_box_pos = (self.entity.pos[0] - offset[0], self.entity.pos[1] - offset[1] - self.y_size)
        
        return text_box_pos
    
    def Set_Text_Box_Size(self):
        self.Set_Y_Size()
        self.Set_X_Size()
        rectangle_surface = pygame.Surface((self.x_size, self.y_size), pygame.SRCALPHA)
        rectangle_color = (0, 0, 0, 200)  # Black with 50% transparency (128 out of 255)
        rectangle_surface.fill(rectangle_color)
        return rectangle_surface
    
    def Set_Headline_Font(self):
        self.headline_font = self.entity.game.default_font

    # Seperate function for size flexibility
    def Set_Y_Size(self):
        self.y_size = 70

    def Set_X_Size(self):
        self.x_size = 100

    def Text_Box_Setup(self, surf, entity_name, offset):
        # Scale the textbox to the name of the entity
        try:
            text_box_pos = self.Set_Text_Box_pos(offset)

            surf.blit(self.rectangle_surface, text_box_pos)
        except TypeError as e:
            print(f"Text_Box_Setup not valid: {e}", self.rectangle_surface, text_box_pos, surf, self.y_size, offset)
        
        return text_box_pos

    def Render(self, surf, offset=(0, 0)):
        if not self.render:
            return
        entity_name = self.Edit_Entity_Name()

        text_box_pos = self.Text_Box_Setup(surf, entity_name, offset)
        if not text_box_pos:
            return

        self.Render_Headline(surf, entity_name, text_box_pos)

        # Render the description of the entity
        self.mixed_symbols.Render_Mixed_Text(surf, self.entity.description, (text_box_pos[0], text_box_pos[1] + 20), 0.5)

        return 
    
 
    def Render_Headline(self, surf, entity_name, text_box_pos):
        self.headline_font.Render_Word(surf, entity_name, text_box_pos, keys.textbox_headline)
