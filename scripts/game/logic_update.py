from scripts.engine.assets.keys import keys

class Logic_Update():
    def __init__(self, game) -> None:
        self.game = game
        self.freeze_frame = 0 # Used to freeze the game temporarily during attacks


    def Update(self):
            
            if not self.Update_Freeze_Frame():
                 return
            
            self.Check_Keyboard_Input()
            
            self.game.particle_handler.Particle_Update()
            self.game.trap_handler.Update()
            self.game.item_handler.Update(self.game.render_scroll)
            self.game.decoration_handler.Update()
            self.game.enemy_handler.Update()
            self.game.entities_render.Update()


            self.game.inventory.Update(self.game.render_scroll)
            self.game.souls_interface.Update()
            self.game.rune_handler.Update(self.game.render_scroll)
            self.game.player.Update(self.game.tilemap, (self.game.movement[1] - self.game.movement[0], self.game.movement[3] - self.game.movement[2]), self.game.render_scroll)
            self.game.ray_caster.Update()

            self.game.mouse.Mouse_Update()
            self.game.text_box_handler.Update()

            self.game.health_bar.Update_Health()


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