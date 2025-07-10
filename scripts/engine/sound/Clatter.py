
class Clatter():
    def __init__(self, game) -> None:
        self.game = game
        self.temp_disable_clatter = False # Used to temporarily disable clatter


    def Generate_Clatter(self, center, clatter_range):
        if self.temp_disable_clatter:
            self.temp_disable_clatter = False
            return

        clatter_range = self.Calculate_Silence_Modifier(clatter_range)
        
        # find nearby enemies and prefilter them 
        nearby_enemies = [
            enemy for enemy in self.game.enemy_handler.Find_Nearby_Enemies(self.game.player, clatter_range)
            if enemy and not enemy.locked_on_target
        ]
            
        for enemy in nearby_enemies:
            # Add enemy to pathfinding queue
            self.game.enemy_handler.Add_To_Pathfinding_Queue(enemy, center)
        


    def Calculate_Silence_Modifier(self, clatter_range):
        if self.game.player.effects.silence.effect:
            clatter_range = max(1, clatter_range - self.game.player.effects.silence.effect * 100)

        return clatter_range
    
    def Disable_Clatter(self):
        self.temp_disable_clatter = True