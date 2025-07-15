from scripts.engine.keys.keys import keys

class Health_Bar:
    def __init__(self, game):
        self.game = game
        self.pos_x = 20
        self.pos_y = self.game.screen_height / self.game.render_scale - 70
        self.animation = 0
        self.animation_max = 4
        self.animation_cooldown_max = 40
        self.animation_cooldown = 0

        # Use dictionary for easy lookup
        self.health_bars = {
            1: self.game.assets[keys.healthbar_1],
            2: self.game.assets[keys.healthbar_2],
            3: self.game.assets[keys.healthbar_3],
            4: self.game.assets[keys.healthbar_4],
            5: self.game.assets[keys.healthbar_5],
            6: self.game.assets[keys.healthbar_6],
            7: self.game.assets[keys.healthbar_7],
            8: self.game.assets[keys.healthbar_8],
            9: self.game.assets[keys.healthbar_9],
            10: self.game.assets[keys.healthbar_10],
        }

        self.current_health = -999 # Set the player's initial health to -999 to trigger an update 
        self.normalised_health = 1
        self.current_health_bar = self.health_bars[self.normalised_health] # Healthbar sprite
        self.player_health = '' # Text displayed above healthbar

    
    def Update(self):
        self.Update_Animation()
        if self.current_health == self.game.player.health:
            return
        
        self.current_health = self.game.player.health
        self.Normalise_Health()
        self.current_health_bar = self.health_bars[self.normalised_health]

    def Update_Animation(self):
        if self.animation_cooldown < self.animation_cooldown_max:
            self.animation_cooldown += 1
            return
        self.animation_cooldown = 0
        self.animation += 1
        if self.animation >= self.animation_max:
            self.animation = 0
        return

    def Normalise_Health(self):
        min_health, max_health = 1, self.game.player.max_health
        current_health = max(self.game.player.health, min_health)

        # Invert scaling: 10 (worst) → 1 (best)
        self.normalised_health = max(1, min(10, round(10 * (1 - (current_health - min_health) / (max_health - min_health)))))

        self.player_health = f"{self.current_health}/{self.game.player.max_health}"

    
    def Render(self, surf):
        surf.blit(self.current_health_bar[self.animation], (self.pos_x, self.pos_y))
        self.game.default_font.Render_Word(surf, self.player_health, (self.pos_x - len(self.player_health) * 2, self.pos_y - 20))
        

