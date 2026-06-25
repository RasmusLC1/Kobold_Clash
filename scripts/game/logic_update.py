from scripts.engine.keys.keys import keys
import pygame

class Logic_Update():
    def __init__(self, game) -> None:
        self.game = game
        self.game.total_time = 0

        self.freeze_frame = 0 # Used to freeze the game temporarily during attacks


    def Update(self, delta_time):
            
          if not self.Update_Freeze_Frame():
               return
          
          self.Check_Keyboard_Input()
          
          self.game.particle_handler.Particle_Update(delta_time)
          self.game.enemy_handler.Update(delta_time)
          self.game.item_handler.Update(delta_time)
          self.game.inventory.Update(delta_time, self.game.render_scroll)
          self.game.decoration_handler.Update(delta_time)
          self.game.entities_render.Update()
          self.game.trap_handler.Update(delta_time)

          keyboard = self.game.keyboard_handler
          movement = (
          keyboard.is_key_pressed(pygame.K_d) - keyboard.is_key_pressed(pygame.K_a),
          keyboard.is_key_pressed(pygame.K_s) - keyboard.is_key_pressed(pygame.K_w)
          )
          self.game.player.Update(self.game.tilemap, delta_time, movement, self.game.render_scroll)
          
          self.game.ray_caster.Update(delta_time)
          self.game.clatter.Update(delta_time)

          self.game.mouse.Mouse_Update()
          self.game.text_box_handler.Update(delta_time)
          self.game.noise_handler.Update()

          self.game.ui_handler.Update(delta_time)

          self.game.total_time += delta_time # Track total time


    def Update_Freeze_Frame(self):
         if not self.freeze_frame:
              return True
         self.freeze_frame = max(0, self.freeze_frame - 1)
         return False


    def Set_Freeze_Frame(self, duration):
         self.freeze_frame = duration

            
    def Check_Keyboard_Input(self):
         if self.game.keyboard_handler.is_key_pressed(pygame.K_ESCAPE):
            self.game.keyboard_handler.Set_Escape_Key(False)
            self.game.state_machine.Set_State('pause_menu')