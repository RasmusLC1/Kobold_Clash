import pygame

from scripts.game.input_update import Input_Update
from scripts.game.state_machine import State_Machine
from scripts.game.save_load_manager import Save_Load_Manager

class Game:
    def __init__(self):
        pygame.init()
        self.save_load_manager = Save_Load_Manager(self, ".data", "save_data")
        
        self.state_machine = State_Machine(self)
        self.input_update = Input_Update(self)
        self.clock = pygame.time.Clock()


        
    def Update_Display(self):
        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
        pygame.display.update()
        

    def run(self):  
        while True:
            self.delta_time = min(self.clock.tick(144) / 1000, 0.1) # Delta time clamped to 0.1 to prevent physics bugs    
            fps = int(self.clock.get_fps())
            pygame.display.set_caption(f'Dungeon Crawler             FPS: {fps}')
            
            self.state_machine.Game_State(self.delta_time)
            self.input_update.Input_Handler()
            self.Update_Display()




Game().run()

