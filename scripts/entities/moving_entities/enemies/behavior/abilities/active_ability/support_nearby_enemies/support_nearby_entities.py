from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.active_ability import Active_Ability

COOLDOWN_TIME = 10
# Base class ability for buffing nearby enemies 
class Support_Nearby_Entities(Active_Ability):
    def __init__(self, game, entity, name, effect_name, particle_name, radius):
        super().__init__(game, entity, name, can_attack_while_triggered=True)
        self.effect_name = effect_name
        self.particle_name = particle_name
        self.radius = radius
        self.effect_strength = self.entity.intelligence // 2
        self.particle_amount = self.effect_strength * 3
        
    # Returns the cooldown time before another special attack 
    def Activate(self):
        nearby_enemies = self.game.enemy_handler.Find_Nearby_Enemies(self.entity, self.radius)
        if not nearby_enemies: # If no nearby entities just return
            return True
        try:
            self.game.particle_handler.Activate_Particles(self.particle_amount, self.particle_name , self.entity.rect().center)
            for enemy in nearby_enemies:
                enemy.effects.Set_Effect(self.effect_name, self.effect_strength)
        except Exception as e:
            print("ACTIVATION OF SUPPORT ABILITY FAILED", e, self.effect_name, self.effect_strength, self.particle_amount, self.particle_name , self.entity.rect().center)


        return True
        
    # Returns true if entity is damaged 30% of health
    def Check_If_Trigger(self):
        return self.entity.player_spotted
