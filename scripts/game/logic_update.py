from scripts.engine.keys.keys import keys

class Logic_Update():
    def __init__(self, game) -> None:
        self.game = game
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


          self.game.rune_handler.Update(delta_time)


          keyboard = self.game.keyboard_handler
          movement = (keyboard.d_pressed - keyboard.a_pressed, keyboard.s_pressed - keyboard.w_pressed)
          self.game.player.Update(self.game.tilemap, delta_time, movement, self.game.render_scroll)
          
          self.game.ray_caster.Update()
          self.game.clatter.Update()

          self.game.mouse.Mouse_Update()
          self.game.text_box_handler.Update(delta_time)
          self.game.noise_handler.Update()

          self.game.ui_handler.Update(delta_time)


    def Update_Freeze_Frame(self):
         if not self.freeze_frame:
              return True
         self.freeze_frame = max(0, self.freeze_frame - 1)
         return False


    def Set_Freeze_Frame(self, duration):
         self.freeze_frame = duration

            
    def Check_Keyboard_Input(self):
         if self.game.keyboard_handler.escape_pressed:
            self.game.keyboard_handler.Set_Escape_Key(False)
            self.game.state_machine.Set_State('pause_menu')