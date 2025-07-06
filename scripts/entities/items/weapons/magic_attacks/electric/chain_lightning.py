from scripts.entities.items.weapons.magic_attacks.electric.electric_particle import Electric_Particle
from scripts.engine.keys.keys import keys

class Chain_Lightning(Electric_Particle):
    def __init__(self, game, pos, entity, damage, speed, shoot_distance, special_attack, direction, effect):
        super().__init__(game, pos, shoot_distance)
        self.shots_left = min (20, effect * 3)
        self.reset_shot = False
        self.Set_Enabled(pos, speed, special_attack, direction, entity, 100)


    def Shoot(self):
        entity = super().Shoot()
        if entity:
            self.Electrocute_Nearby_Enemies()
            self.Reset_Shot()

    
    def Electrocute_Nearby_Enemies(self):
        self.nearby_enemies = self.game.enemy_handler.Find_Nearby_Enemies(self, 4)
        for enemy in self.nearby_enemies:
            enemy.Set_Effect(keys.electric, 3)
