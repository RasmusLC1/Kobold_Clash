from scripts.menu.button import Button
from scripts.engine.keys.keys import keys

class Portal_Button(Button):
    def __init__(self, game, pos, size, effect, text, color = (0, 0, 0)) -> None:
        self.effect = effect
        if effect == 'unlock':
            self.unlock_cost = 50 + (game.level - 1) * 30
            text = text + ': ' + str(self.unlock_cost)
        super().__init__(game, pos, size, text, 'None', False, color)


    def Update(self):
        self.game.mouse.Menu_Mouse_Update()
        if self.rect().colliderect(self.game.mouse.rect_pos_menu()):
            self.Handle_Button_Color()

            # Check if player can afford cost when clicking
            if self.rect().colliderect(self.game.mouse.rect_click()):
                if self.effect == 'unlock':
                    if self.Handle_Unlock():
                        return True
                elif self.effect == 'enter':
                    self.Handle_Enter()
                    return True
                
            
            return False
        
        self.Reset_Color()
        return False
    
    def Handle_Unlock(self):
        if self.game.player.Get_Total_Available_Souls() >= self.unlock_cost:
            self.game.player.Decrease_Souls(self.unlock_cost)
            self.game.state_machine.Set_State('run_game')
            return True
        return False
    
    def Handle_Enter(self):
        self.game.state_machine.Set_State('new_level')



    def Render(self, surf):
        super().Render(surf)
        if self.effect == 'enter':
            return
        self.game.symbols.Render_Symbol(surf, 'soul',  (round(self.pos[0] + self.size[0] - 40), self.pos[1] + self.size[1] // 2 - 8))


