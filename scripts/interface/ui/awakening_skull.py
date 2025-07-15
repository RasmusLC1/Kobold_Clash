from scripts.engine.keys.keys import keys

class Awakening_Skull:
    def __init__(self, game):
        self.game = game
        self.pos_x = 20
        self.pos_y = self.game.screen_height / self.game.render_scale - 20
        self.animation = 0
        self.awakening_level = 0
        self.animation_max = 4
        self.animation_cooldown_max = 40
        self.animation_cooldown = 0

        # Use dictionary for easy lookup
        self.awakening_symbols = {
            0: self.game.assets[keys.healthbar_1],
            1: self.game.assets[keys.healthbar_1],
            2: self.game.assets[keys.healthbar_2],
            3: self.game.assets[keys.healthbar_3],
            4: self.game.assets[keys.healthbar_4],
            5: self.game.assets[keys.healthbar_5],
        }

        self.Set_Awakening(0)


    
    def Set_Awakening(self, awakening_level):
        self.current_awakening_symbol = self.awakening_symbols.get(awakening_level)

    def Update(self):
        self.Update_Animation()

    def Update_Animation(self):
        if self.animation_cooldown < self.animation_cooldown_max:
            self.animation_cooldown += 1
            return
        self.animation_cooldown = 0
        self.animation += 1
        if self.animation >= self.animation_max:
            self.animation = 0
        return


    
    def Render(self, surf):
        surf.blit(self.current_awakening_symbol[self.animation], (self.pos_x, self.pos_y))
        self.game.default_font.Render_Word(surf, self.player_health, (self.pos_x - len(self.player_health) * 2, self.pos_y - 20))
        

