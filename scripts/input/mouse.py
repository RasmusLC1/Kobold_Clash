import pygame
from scripts.engine.keys.keys import keys

class Mouse_Handler:
    def __init__(self, game):
        self.left_click = False  # Left mouse button has been clicked
        self.right_click = False  # Right mouse button has been clicked
        self.game = game  # Game
        self.click_pos = (0, 0)  # Get the position of the last click
        self.mpos = (0, 0)  # Mouse position with offset
        self.player_mouse = (0, 0)  # Mouse position without offset
        self.menu_mouse = (0, 0) # Mouse without renderscale
        self.hold_down_left = 0  # Left mouse button hold down time in ticks
        self.hold_down_right = 0  # Right mouse button hold down time in ticks
        self.time_since_last_click = 0  # Check the time since last click
        self.double_click = 0  # Timer to signal double clicking
        self.single_click_delay = 0  # Single click timer
        self.inventory_clicked = 0 # Check if the inventory has been clicked
        
        

    # Mouse inputs that need to be updated for each frame
    def Mouse_Update(self):
        self.Double_Click_Timer()
        self.Decrement_Inventory_Clicked()
        self.Hold_Down_Left()
        self.Hold_Down_Right()
        self.Player_Mouse_Update()


    # Mouse inputs that only need to be updated when there is an input
    def Mouse_Input(self, key_press, offset=(0, 0)):
        self.Mpos_Update(offset)
        if key_press.type == pygame.MOUSEBUTTONDOWN:

            if key_press.button == 1:  # Check for left click (button 1)
                self.left_click = True
                self.Set_Click_Pos((key_press.pos[0] / self.game.render_scale, key_press.pos[1] / self.game.render_scale))
                if self.time_since_last_click:
                    self.double_click = 20
                self.time_since_last_click = 20

            if key_press.button == 3:  # Check for right click (button 3)
                self.right_click = True
                self.hold_down_right += 1

        if key_press.type == pygame.MOUSEBUTTONUP:
            self.Set_Click_Pos((-999, -999))
            if key_press.button == 1:  # Check for left click (button 1)
                self.left_click = False
                if not self.single_click_delay:
                    self.single_click_delay = 5  # Start the single click delay

            if key_press.button == 3:  # Check for right click (button 3)
                self.right_click = False

            if key_press.button in {4, 5}:  # Scroll wheel click
                self.game.inventory.Increment_Weapon_Inventory()


    # Hold down left click timers
    def Hold_Down_Left(self):
        if self.left_click:
            self.hold_down_left += 1
        elif not self.left_click and self.hold_down_left:
            self.hold_down_left = 0

    # Hold down right click timers
    def Hold_Down_Right(self):
        if self.right_click:
            self.hold_down_right += 1
        elif not self.right_click and self.hold_down_right:
            self.hold_down_right = 0

    # Handle the double click timers
    def Double_Click_Timer(self):
        if self.time_since_last_click:
            self.time_since_last_click -= 1
        if self.double_click:
            self.double_click -= 1
        if self.single_click_delay:
            self.single_click_delay -= 1

    # Rest double click logic
    def Reset_Double_Click(self):
        self.time_since_last_click = 0  
        self.double_click = 0  
        self.single_click_delay = 0  
        
    # Update the mouse position when left clicking
    def Mpos_Update(self, offset = (0,0)):
        mouse_pos = pygame.mouse.get_pos()
        mpos_x = mouse_pos[0] / self.game.render_scale + offset[0]
        mpos_y = mouse_pos[1] / self.game.render_scale + offset[1]
        self.mpos = (mpos_x, mpos_y)
        self.mpos_not_offset = mouse_pos

    def Player_Mouse_Update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.player_mouse = (mouse_pos[0] / self.game.render_scale + self.game.render_scroll[0], mouse_pos[1] / self.game.render_scale + self.game.render_scroll[1])


    def Menu_Mouse_Update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.menu_mouse = (mouse_pos[0] / self.game.render_scale, mouse_pos[1] / self.game.render_scale)


    def Set_Click_Pos(self, pos):
        self.click_pos = pos

    # Reduce inventory clicked time
    def Decrement_Inventory_Clicked(self):
        if self.inventory_clicked:
            self.inventory_clicked -= 1

    # Start a timer if 
    def Set_Inventory_Clicked(self, timer):
        self.inventory_clicked = timer

    # Click collision
    def rect_click(self):
        return pygame.Rect(self.click_pos[0], self.click_pos[1], 1, 1)    
    
    # Mouse movement collision, add offset to adjust
    def rect_pos(self, offset = (0, 0)):
        return pygame.Rect(self.mpos[0] - offset[0], self.mpos[1]  - offset[1], 1, 1)  
    
    # Mouse movement collision, add offset to adjust
    def rect_pos_menu(self, offset = (0, 0)):
        return pygame.Rect(self.menu_mouse[0], self.menu_mouse[1], 1, 1)  
    
