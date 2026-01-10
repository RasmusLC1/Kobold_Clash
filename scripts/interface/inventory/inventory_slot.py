import pygame
from scripts.engine.keys.keys import keys

class Inventory_Slot():
    def __init__(self, game, pos, type, size, item, index, key = None):
        self.game = game
        self.pos = pos
        self.type = type
        self.index = index
        self.size = size
        self.item = item
        self.item_type = None
        self.key = key
        self.background = None
        self.inventory_type = None
        self.Setup_Inventory_Texture()
        self.active = False
        self.activate_counter = 0
        self.border_color = (0, 0, 0)
        self.white_list_items = []
 
    def Update_Pos(self, pos):
        self.pos = pos
        if self.item:
            self.Move_Item()


    def Setup_Inventory_Texture(self):
        light_grey = (211, 211, 211)
        self.box_surface = pygame.Surface(self.size)
        self.box_surface.fill(light_grey)
        self.box_surface.set_alpha(179)

    def Set_Active(self, status):
        self.active = status

    def Reset_Inventory_Slot(self):
        self.item = None
        self.active = False
        self.activate_counter = 0

    def Update(self):
        if self.active:
            self.activate_counter += 1
            return
        
        self.Check_Item_Durability()
        return
    
    def Check_Item_Durability(self):
        if not self.item:
            return False
        
        if self.item.durability > 0:
            return False
        
        self.game.item_handler.Remove_Item(self.item, True)
        self.item = None
        return True

    def Update_Item(self, delta_time):
        if not self.item:
            return
        if self.item.sub_category == keys.weapon:
            return
        if self.item.sub_category == keys.loot:
            self.item.Update_In_Inventory()
        
        if not self.item:
            return
        self.item.Update(delta_time)

    def Move_Item(self):
        self.item.Move((self.pos[0] + 5, self.pos[1] + 5))


    def Add_Item(self, item):
        if not item:
            return False
        if not item.sub_category in self.white_list_items:
            return False
        
        self.item = item
        self.item.active = True
        self.item.picked_up = True
        self.Move_Item()
        self.item.Set_Inventory_Index(self.index)
        self.item_type = item.type
        if self.inventory_type:
            self.item.Set_Inventory_Type(self.inventory_type)
        else:
            self.item.Set_Inventory_Type(None)
        return True

    def Remove_Item(self):
        self.item = None

    def Remove_Item_On_Amount(self):
        if not self.item.amount <= 0:
            return False
        self.item = None
        return True
    
    def Clear(self):
        self.active = False
        self.item = None

    def Set_White_List(self, items):
        self.white_list_items = items

    def Add_Background(self, background):
        self.background = background

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def Render(self, surf):

        # Render the box surface with scaling
        scaled_box_surface = pygame.transform.scale(self.box_surface, (self.size[0], self.size[1]))
        surf.blit(scaled_box_surface, self.pos)
        pygame.draw.rect(surf, self.border_color, self.rect(), 1)
       

        if self.background and not self.item:
            background_image = pygame.transform.scale(self.background, self.size)
            surf.blit(background_image, self.pos)

        if not self.item:
            return
        
        # Renders the item cooldown
        if self.item.clicked:
            self.item.Render_Active(surf, self.game.render_scroll)

        if self.item and not self.active:
            self.item.Render_Inventory(surf, self.pos, self.size)
        else:

            return

        self.Render_Key(surf)
        if not self.item.amount > 1:
            return
        
        self.Render_Item_Amount(surf)

    # Render the amount of an item
    def Render_Item_Amount(self, surf):
        x_offset = 0
        if self.item.amount > 10:
            x_offset = 0
        # self.game.default_font.Render_Word(surf, str(self.item.amount + '/' + self.item.max_amount), (self.pos[0] + x_offset, self.pos[1] + self.item.size[1]))
        self.game.default_font.Render_Word(surf, 
            str(self.item.amount) + '/' + str(self.item.max_amount), 
            (self.pos[0] + x_offset, self.pos[1] + 25),
            keys.font_small
        )

    # Render the keyboard shortcut
    def Render_Key(self, surf):
        if not self.key:
            return
        self.game.default_font.Render_Word(surf, str(self.key), (self.pos[0], self.pos[1]))