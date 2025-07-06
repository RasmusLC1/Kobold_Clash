import pygame
from scripts.engine.keys.keys import keys

class Keyboard_Handler:
    def __init__(self, game) -> None:
        self.game = game
        self.a_pressed = False
        self.w_pressed = False
        self.s_pressed = False
        self.d_pressed = False
        self.e_pressed = False
        self.z_pressed = False
        self.x_pressed = False
        self.c_pressed = False
        self.space_pressed = False
        self.alt_pressed = False
        self.escape_pressed = False
        self._1_pressed = False
        self._2_pressed = False
        self._3_pressed = False
        self._4_pressed = False
        self._5_pressed = False
        self._6_pressed = False
        self._7_pressed = False
        self._8_pressed = False
        self._9_pressed = False

    def keyboard_Input(self, key_press, offset=(0, 0)):
        if key_press.type == pygame.KEYDOWN:
            self.Key_Down(key_press)


        if key_press.type == pygame.KEYUP:
            self.Key_Up(key_press)
            
    def Key_Down(self, key_press):
        if key_press.key == pygame.K_a:
            self.game.movement[0] = True
        if key_press.key == pygame.K_d:
            self.game.movement[1] = True
        if key_press.key == pygame.K_w:
            self.game.movement[2] = True
        if key_press.key == pygame.K_s:
            self.game.movement[3] = True
        if key_press.key == pygame.K_1:
            self._1_pressed = True
        if key_press.key == pygame.K_2:
            self._2_pressed = True
        if key_press.key == pygame.K_3:
            self._3_pressed = True
        if key_press.key == pygame.K_4:
            self._4_pressed = True
        if key_press.key == pygame.K_5:
            self._5_pressed = True
        if key_press.key == pygame.K_6:
            self._6_pressed = True
        if key_press.key == pygame.K_7:
            self._7_pressed = True
        if key_press.key == pygame.K_e:
            self.e_pressed = True

        if key_press.key == pygame.K_p:
            self.game.tilemap.Render_All_Tiles()

        if key_press.key == pygame.K_SPACE:
            self.space_pressed = True
        if key_press.key == pygame.K_LALT:
            self.alt_pressed = True
        if key_press.key == pygame.K_z:
            self.z_pressed = True
        if key_press.key == pygame.K_x:
            self.x_pressed = True
        if key_press.key == pygame.K_c:
            self.c_pressed = True
        if key_press.key == pygame.K_ESCAPE:
            self.escape_pressed = True

    def Key_Up(self, key_press):
        if key_press.key == pygame.K_a:
            self.game.movement[0] = False
        if key_press.key == pygame.K_d:
            self.game.movement[1] = False
        if key_press.key == pygame.K_w:
            self.game.movement[2] = False
        if key_press.key == pygame.K_s:
            self.game.movement[3] = False
        if key_press.key == pygame.K_e:
            self.e_pressed = False
        if key_press.key == pygame.K_1:
            self._1_pressed = False
        if key_press.key == pygame.K_2:
            self._2_pressed = False
        if key_press.key == pygame.K_3:
            self._3_pressed = False
        if key_press.key == pygame.K_4:
            self._4_pressed = False
        if key_press.key == pygame.K_5:
            self._5_pressed = False
        if key_press.key == pygame.K_6:
            self._6_pressed = False
        if key_press.key == pygame.K_7:
            self._7_pressed = False
        if key_press.key == pygame.K_z:
            self.z_pressed = False
        if key_press.key == pygame.K_x:
            self.x_pressed = False
        if key_press.key == pygame.K_c:
            self.c_pressed = False
        if key_press.key == pygame.K_SPACE:
            self.space_pressed = False
        if key_press.key == pygame.K_LALT:
            self.alt_pressed = False
        if key_press.key == pygame.K_ESCAPE:
            self.escape_pressed = False


    def Set_E_Key(self, state):
        self.e_pressed = state

    def Set_Escape_Key(self, state):
        self.escape_pressed = state
