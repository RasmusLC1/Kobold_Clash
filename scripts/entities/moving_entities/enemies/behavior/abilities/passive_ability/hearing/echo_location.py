from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.passive_ability import Passive_Ability

class Echo_Location(Passive_Ability):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name)
        self.entity.intent_manager.behavior_manager.ability_handler.Set_Player_Distance(self.name)

    # Always registrer noises and path towards them
    def Update(self, delta_time):
        if self.entity.locked_on_target:
            return
        
        clatter_pos = self.game.clatter.Check_If_Noise_Generated()
        
        # Only act on the precise frame the noise is created
        if clatter_pos:
            self.game.enemy_handler.Add_To_Pathfinding_Queue(
                self.entity, 
                clatter_pos
            )
        
        # Ensure the underlying base tick updates execute smoothly every frame
        super().Update(delta_time)
