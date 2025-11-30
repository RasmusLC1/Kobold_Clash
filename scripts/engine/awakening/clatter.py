from scripts.engine.awakening.awakening import Awakening

class Clatter():
    def __init__(self, game) -> None:
        self.game = game
        self.temp_disable_clatter = False # Used to temporarily disable clatter
        self.awakening = Awakening(game)

    def Update(self):
        self.awakening.Update()

    def Generate_Clatter(self, center, clatter_range):
        if self.temp_disable_clatter:
            self.temp_disable_clatter = False
            return

        clatter_range = self.Calculate_Silence_Modifier(clatter_range)
        print(clatter_range)
        self.awakening.Trigger_Awakening()
        # find nearby enemies and prefilter them 
        nearby_enemies = [
            enemy for enemy in self.game.enemy_handler.Find_Nearby_Enemies(self.game.player, clatter_range)
            if enemy and not enemy.locked_on_target
        ]
            
        for enemy in nearby_enemies:
            # Add enemy to pathfinding queue
            self.game.enemy_handler.Add_To_Pathfinding_Queue(enemy, center)
        

    def Increase_Awakening(self):
        self.awakening.Set_Awakening_Level(self.awakening.awakening_level + 1)

    def Get_Awakening_Level(self):
        return self.awakening.awakening_level

    def Calculate_Silence_Modifier(self, clatter_range):
        if self.game.player.effects.silence.effect:
            clatter_range = max(1, clatter_range - self.game.player.effects.silence.effect * 100)

        return clatter_range
    
    def Disable_Clatter(self):
        self.temp_disable_clatter = True

    # Sets awakening level to 0
    def Reset_Awakening_Level(self):
        self.awakening.awakening_cooldown = 0
        self.awakening.Set_Awakening_Level(0)

