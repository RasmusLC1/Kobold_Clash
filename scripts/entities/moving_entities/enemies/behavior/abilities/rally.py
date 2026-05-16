from scripts.entities.moving_entities.enemies.behavior.abilities.ability import Ability
from scripts.engine.keys.keys import keys

COOLDOWN_TIME = 10
# Increases strength of nearby enemies
class Rally(Ability):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name)
        
    # Returns the cooldown time before another special attack 
    def Activate(self):
        nearby_enemies = self.game.enemy_handler.Find_Nearby_Enemies(self.entity, 150)
        if not nearby_enemies:
            return
        self.game.particle_handler.Activate_Particles(10, keys.strength_particle, self.entity.rect().center)
        for enemy in nearby_enemies:
            enemy.effects.Set_Effect(keys.increase_strength, 2)


        return True
        
    # Returns true if entity is damaged 30% of health
    def Check_If_Trigger(self):
        return self.entity.player_spotted
