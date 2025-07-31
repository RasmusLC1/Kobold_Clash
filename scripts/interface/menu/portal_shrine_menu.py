from scripts.interface.menu.portal_button import Portal_Button
from scripts.interface.menu.menu import Menu
from scripts.engine.keys.keys import keys


class Portal_Shrine_Menu(Menu):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.button_size_x *= 1.5
        self.button_size_y *= 1.5
        self.rect_surface.set_alpha(255)
        self.shrine = None
        self.unlock_portal_button = None
        self.enter_portal_button = None
        self.Generate_Button((self.width - self.button_size_x // 2, self.button_size_y * 4.5), (self.button_size_x, self.button_size_y), 'resume Game', 'run_game')




    def Update(self):
        super().Update()
        self.game.ui_handler.souls_interface.Update(self.game.delta_time)
        if self.unlock_portal_button:
            # If not purchased simply return
            if self.unlock_portal_button.Update():
                self.shrine.Activate()
                self.enter_portal_button = Portal_Button(self.game, (self.width - self.button_size_x // 2, self.button_size_y * 2.5), (self.button_size_x, self.button_size_y), 'enter', 'Enter Portal')
                self.unlock_portal_button = None
                return
            
            
        if self.enter_portal_button:
            self.enter_portal_button.Update()


    def Initialise_Shrine(self, shrine):
        self.shrine = shrine
        self.enter_portal_button = None
        self.unlock_portal_button = Portal_Button(self.game, (self.width - self.button_size_x // 2, self.button_size_y * 2.5), (self.button_size_x, self.button_size_y), 'unlock', 'Unlock Portal')

    def Check_Keyboard_Input(self):
         if self.game.keyboard_handler.escape_pressed:
            self.game.keyboard_handler.Set_Escape_Key(False)
            self.game.state_machine.Set_State('run_game')

    def Reset(self):
        self.unlock_portal_button = None
        self.enter_portal_button = None
        self.shrine = None

    def Render(self, surf):
        super().Render(surf)
        self.game.ui_handler.souls_interface.Render(self.game.display)
        self.Render_Buttons(surf)
    
    def Render_Buttons(self, surf):
        if self.unlock_portal_button:
            self.unlock_portal_button.Render(surf)
            return
        
        if self.enter_portal_button:
            self.enter_portal_button.Render(surf)

        