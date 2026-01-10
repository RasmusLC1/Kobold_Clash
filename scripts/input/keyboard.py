import pygame
from scripts.engine.keys.keys import keys

class Keyboard_Handler:
    def __init__(self, game) -> None:
        self.game = game
        
        self.key_states = {
            pygame.K_a: False,
            pygame.K_w: False,
            pygame.K_s: False,
            pygame.K_d: False,
            pygame.K_e: False,
            pygame.K_z: False,
            pygame.K_x: False,
            pygame.K_c: False,
            pygame.K_p: False,
            pygame.K_SPACE: False,
            pygame.K_LALT: False,
            pygame.K_ESCAPE: False,
            # Number keys (k_1 through k_9)
            pygame.K_1: False,
            pygame.K_2: False,
            pygame.K_3: False,
            pygame.K_4: False,
            pygame.K_5: False,
            pygame.K_6: False,
            pygame.K_7: False,
            pygame.K_8: False, 
            pygame.K_9: False,
        }

    # Handler function
    def keyboard_Input(self, key_press, offset=(0, 0)):
        if key_press.type == pygame.KEYDOWN:
            self.Key_Down(key_press)

        if key_press.type == pygame.KEYUP:
            self.Key_Up(key_press)
            
    def Key_Down(self, key_press):
        key = key_press.key
        
        # Optimization: Set the state directly in the dictionary if the key is monitored.
        if key in self.key_states:
            self.key_states[key] = True


    def Key_Up(self, key_press):
        key = key_press.key
        
        # Set the state directly in the dictionary if the key is monitored.
        if key in self.key_states:
            self.key_states[key] = False


    
    # Key press lookup
    def is_key_pressed(self, key_constant):
        return self.key_states.get(key_constant, False)


    def Set_E_Key(self, state):
        self.key_states[pygame.K_e] = state

    def Set_Escape_Key(self, state):
        self.key_states[pygame.K_ESCAPE] = state


    def Check_If_Movement_Enabled(self):
        return (
            self.is_key_pressed(pygame.K_w) or 
            self.is_key_pressed(pygame.K_a) or 
            self.is_key_pressed(pygame.K_s) or 
            self.is_key_pressed(pygame.K_d)
        )