import pygame
import math
from scripts.interface.menu.rune_button import Rune_Button
from scripts.interface.menu.menu import Menu
from scripts.engine.keys.keys import keys
import pygame

# TODO: REWORK since runes have been changed

class Rune_Shrine_Menu(Menu):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.runes = []
        self.active_rune = None
        self.available_rune = None
        self.available_rune_name = ''
        self.rune_bought = False
        self.Init_Rune_Upgrade_Buttons()
        self.rect_surface.set_alpha(255)
        self.shrine = None


        # Highlights which rune is active
        self.rune_highlight = pygame.Surface((60, 60))
        self.rune_highlight.fill((150, 150, 150))



    
    def Init_Rune_Upgrade_Buttons(self):
        self.rune_upgrade_buttons = []
        width = self.game.screen_width // self.game.render_scale // 2
        button_size_x = 200
        button_size_y = 40
        self.Generate_Rune_Button((width - button_size_x // 2, 200), (button_size_x, button_size_y), keys.souls, keys.souls, (100, 100, 150))
        self.Generate_Rune_Button((width - button_size_x // 2, 260), (button_size_x, button_size_y), keys.power, keys.power, (140, 0, 0))
        self.Generate_Rune_Button((width - button_size_x // 2, 230), (button_size_x, button_size_y), 'Purchase', 'purchase', (140, 0, 0))

        

    def Init_Buttons(self):
        width = self.game.screen_width // self.game.render_scale // 2
        height = self.game.screen_height // self.game.render_scale
        button_size_x = 200
        button_size_y = 40
        self.Generate_Button((width - button_size_x // 2, height - button_size_y), (button_size_x, button_size_y), 'resume', 'run_game', False, (100, 100, 100))
    
    def Generate_Rune_Button(self, pos, size, text, effect, color = (0, 0, 0)):
        rune_button = Rune_Button(self.game, pos, size, text, effect, color)
        self.rune_upgrade_buttons.append(rune_button)

    def Update(self):
        super().Update()
        self.Rune_Interactions()
        self.game.ui_handler.souls_interface.Update()

        self.Update_Rune_Buttons()

    
    def Update_Rune_Buttons(self):
        if not self.active_rune:
            return
        for rune_button in self.rune_upgrade_buttons:
            # Don't update buttons if the rune cannot use that upgrade
            if self.active_rune.original_soul_cost == 0 and rune_button.effect == keys.souls:
                continue

            if self.active_rune.original_power == 0 and rune_button.effect == keys.power:
                continue
            
            self.Rune_Button_Press(rune_button)

    def Rune_Button_Press(self, rune_button):
        
        # Checks for button click
        if not rune_button.Update(self.active_rune):
            return
        
        if rune_button.effect == 'purchase':
            self.rune_bought = True
        else:
            self.Upgrade_Rune()
    
    def Upgrade_Rune(self):
        rune_cost = self.active_rune.Get_Upgrade_Cost()
        if self.game.player.Get_Total_Available_Souls() < rune_cost:
            return False
        self.game.player.Decrease_Souls(rune_cost)


    def Rune_Interactions(self):
        # Check interaction with runes
        for rune in self.runes:
            if rune.Menu_Rect().colliderect(self.game.mouse.rect_click()):
                if self.Replace_Rune(rune):
                    return
                self.active_rune = rune
                # Clear the previous text
                return

        if not self.available_rune:
            return

        if self.available_rune.Menu_Rect().colliderect(self.game.mouse.rect_click()):

            self.active_rune = self.available_rune

            return

    def Replace_Rune(self, rune_to_replace):
        if not self.rune_bought:
            return False
        
        clear_available_rune = pygame.Surface((50, 60))
        clear_available_rune.fill((20,20,20)) # Gold color

        self.game.display.blit(clear_available_rune, (self.available_rune.menu_pos[0] - 5, self.available_rune.menu_pos[1] - 30))
        self.game.item_handler.Replace_Rune_In_Inventory(rune_to_replace, self.available_rune)

        # self.game.rune_handler.Add_Rune_To_Rune_Inventory(self.available_rune.type)
        self.game.player.Decrease_Souls(self.available_rune.Calculate_Value())

        self.Set_Active_Runes_Menu_Pos()
        self.available_rune = None
        self.available_rune_name = ''
        self.rune_bought = False
        self.active_rune = None
        self.shrine.Remove_Available_Rune()
        return True


        
    def Reset_Rune_Bought(self):
        self.rune_bought = False



    def Check_Keyboard_Input(self):
         if self.game.keyboard_handler.is_key_pressed(pygame.K_ESCAPE):
            self.game.keyboard_handler.Set_Escape_Key(False)
            self.game.state_machine.Set_State('run_game')

    # Get a random Rune
    def Initialise_Runes(self, shrine, available_rune = None):
        self.Set_Active_Runes_Menu_Pos()
        self.shrine = shrine
        if not available_rune:
            return
        self.available_rune = available_rune
        rune_name = available_rune.type
        self.available_rune_name = rune_name.replace('_rune', '')
        self.available_rune.Set_Menu_Pos((self.game.screen_width // self.game.render_scale - 100, self.game.screen_height // 2 // self.game.render_scale))


    
    def Set_Active_Runes_Menu_Pos(self):
        self.runes = self.game.item_handler.Get_Active_Runes()
        pos_x = 40
        pos_y = 130
        for rune in self.runes:
            rune.Set_Menu_Pos((pos_x, pos_y))
            pos_y += 60

        
    def Purchase_Button(self, surf, rune_button):
        if rune_button.effect != 'purchase':
            return False
        
        if self.rune_bought:
            pos_x = self.game.screen_width // self.game.render_scale // 2 - 20
            pos_y = rune_button.pos[1] + rune_button.size[1] // 2 - 8
            self.game.default_font.Render_Word(surf, 'Select Rune', (pos_x, pos_y))
            self.game.default_font.Render_Word(surf, 'To Replace', (pos_x, pos_y + 12))
            
            return True
        pos_x = rune_button.pos[0] + rune_button.size[0] - 40
        pos_y = rune_button.pos[1] + rune_button.size[1] // 2 - 8
        rune_button.Render(surf)

        self.game.default_font.Render_Word(surf, str(self.active_rune.Calculate_Value()), (pos_x, pos_y))
        soul_symbol_x_pos_offset = 16 * len(str(self.active_rune.upgrade_cost))

        self.game.symbols.Render_Symbol(surf, 'soul', (pos_x + soul_symbol_x_pos_offset, pos_y - 2), 1.5)
        return True




    def Render(self, surf):
        super().Render(surf)
        if self.active_rune:
            surf.blit(self.rune_highlight, (self.active_rune.menu_pos[0] - 6, self.active_rune.menu_pos[1] - 6))
            self.game.default_font.Render_Word(surf, "Name:   " + self.active_rune.type, (20, 20))        
            self.game.default_font.Render_Word(surf, "Souls Cost:   " + str(self.active_rune.soul_cost), (20, 44))        
            self.game.default_font.Render_Word(surf, "Power:        " + str(self.active_rune.power), (20, 68))        
            self.game.default_font.Render_Word(surf, "Upgrade Cost: " + str(self.active_rune.upgrade_cost), (20, 92))
            soul_symbol_x_pos_offset = 240 + 10 * len(str(self.active_rune.upgrade_cost))
            self.game.symbols.Render_Symbol(surf, 'soul',  (soul_symbol_x_pos_offset, 90), 1.5)
            self.game.symbols.Render_Symbol(surf, 'soul',  (soul_symbol_x_pos_offset, 42), 1.5)


        self.game.ui_handler.souls_interface.Render(self.game.display)


        # render active runes
        for rune in self.runes:
            rune.Render_Menu(surf)

        # Handle available rune
        if self.available_rune:
            self.game.default_font.Render_Word(surf, self.available_rune_name, (self.available_rune.menu_pos[0] - 10, self.available_rune.menu_pos[1] - 15))

            self.available_rune.Render_Menu(surf)

        # If no rune has been selected return
        if not self.active_rune:
            return
        
        
        # Handle buttons for active rune
        for rune_button in self.rune_upgrade_buttons:
            if self.active_rune == self.available_rune:

                if self.Purchase_Button(surf, rune_button):
                    return
                else:
                    continue
                


            if self.active_rune.original_soul_cost == 0 and rune_button.effect == keys.souls:
                continue

            if self.active_rune.original_power == 0 and rune_button.effect == keys.power:
                continue

            if rune_button.effect == 'purchase':
                continue
            rune_button.Render(surf)


