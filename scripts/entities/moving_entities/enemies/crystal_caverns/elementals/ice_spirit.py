from scripts.entities.moving_entities.enemies.enemy import Enemy
from scripts.entities.items.weapons.magic_attacks.ice.ice_shooter import Ice_Shooter
from scripts.engine.keys.keys import keys

ICE_PROJECTILE_NUM = 3 * 20

class Ice_Spirit(Enemy):
    def __init__(self, game, pos, type, health, strength, max_speed, agility, intelligence, stamina):
        super().__init__(game, pos, type, health, strength, max_speed, agility, intelligence, stamina, 1.4, 'elemental', 20)
        self.animation_handler.Set_Animation_Num_Max(3)
        self.animation_handler.Set_Attack_Animation_Num_Max(3)
        self.animation_handler.Set_Attack_Animation_Num_Cooldown_Max(0.3)
        self.animation_handler.Set_Animation_Num_Cooldown_Max(0.7)
        self.path_finding_strategy = 'standard'
        self.attack_strategy = keys.long_range
        self.intent_manager.Set_Intent([keys.attack])
        self.attack_distance  = 250
        self.shooting_ice = False
        self.ice_damage = 5
        self.minimum_distance = 50
        self.active_weapon = Ice_Shooter(self.game)

    def Update(self, tilemap, delta_time, movement = (0, 0)):
        super().Update(tilemap, delta_time, movement)
        if self.effects.frozen.effect:
            self.Set_Effect(keys.healing, self.effects.frozen.effect)
            self.Set_Effect(keys.frozen_resistance, 2)



    def Attack(self, delta_time):
        if not super().Attack(delta_time):
            return
        
        if self.game.player.effects.invisibility.effect:
            return False
        
        # If Player is to close, then ice spirit cannot shoot
        if self.distance_to_player < self.minimum_distance:
            return False
        
        self.charge += delta_time

        if self.charge >= self.max_weapon_charge and not self.shooting_ice:
            self.shooting_ice = ICE_PROJECTILE_NUM

        if self.shooting_ice:
            self.Shoot_Ice_Particle()

    
    
    def Shoot_Ice_Particle(self):
        self.Set_Target(self.game.player.pos)
        self.Set_Attack_Direction()
        self.shooting_ice = self.active_weapon.Particle_Creation(self, self.shooting_ice, self.ice_damage)
        if not self.shooting_ice:
            self.charge = 0




    def Render_Weapons(self, surf, offset):
        pass