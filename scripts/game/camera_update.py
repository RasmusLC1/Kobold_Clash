import pygame
import random

class Camera_Update():
    def __init__(self, game) -> None:
        self.game = game
        self.camera_speed = 10 # Adjusts the scroll speed
        self.shake_duration = 0
        self.shake_magnitude = 0

    def Camera_Scroll(self):
        self.game.scroll[0] += (self.game.player.rect().centerx - self.game.display.get_width() / 2 - self.game.scroll[0]) / self.camera_speed
        self.game.scroll[1] += (self.game.player.rect().centery - self.game.display.get_height() / 2 - self.game.scroll[1]) / self.camera_speed
        shake_x, shake_y = self.Set_Screen_Shake()
        self.game.render_scroll = (int(self.game.scroll[0]) + shake_x, int(self.game.scroll[1]) + shake_y)

    def Set_Camera_Position(self, pos):
        self.game.render_scroll = pos

    def Enable_Full_Screen(self, event):
        self.game.render_scale = max(event.w, event.h) / 1000

        self.game.screen_width = event.w
        self.game.screen_height = event.h
        
        
        self.game.screen = pygame.display.set_mode((self.game.screen_width, self.game.screen_height), pygame.FULLSCREEN)
        self.game.display = pygame.Surface((self.game.screen_width/self.game.render_scale, self.game.screen_height/self.game.render_scale))
        self.game.renderer.Update_Background_Image()

        self.Update_Inventories()
        self.game.menu_handler.Resize_Menus()

    def Update_Inventories(self):
        if self.game.state_machine.game_state == 'main_menu':
             return
        self.game.inventory.Update_Inventory_Slot_Pos()

    def Trigger_Shake(self, duration, magnitude):
        self.shake_duration = duration
        self.shake_magnitude = magnitude

    def Set_Screen_Shake(self):
        shake_x = shake_y = 0
        if self.shake_duration > 0:
            shake_x = random.randint(-self.shake_magnitude, self.shake_magnitude)
            shake_y = random.randint(-self.shake_magnitude, self.shake_magnitude)
            self.shake_duration = max(0, self.shake_duration - 1)
        
        if not self.shake_duration:
            self.shake_magnitude = 0

        return shake_x, shake_y