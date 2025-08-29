from scripts.entities.moving_entities.enemies.enemy import Enemy
from scripts.entities.items.weapons.magic_attacks.fire.flame_thrower import Flame_Thrower
from scripts.engine.keys.keys import keys

FIRE_PROJECTILE_NUM = 1 * 20

class Fire_Spirit(Enemy):
    def __init__(self, game, pos, type, health, strength, max_speed, agility, intelligence, stamina):
        super().__init__(game, pos, type, health, strength, max_speed, agility, intelligence, stamina, 1.8, 'elemental', 20)
        
        self.animation = 'fire_spirit_idle'
        self.path_finding_strategy = 'ignore_lava'
        self.attack_strategy = keys.medium_range
        self.intent_manager.Set_Intent([keys.attack])

        self.look_for_health_cooldown = 0
        self.fire_cooldown = 0
        self.shooting_fire = 0
        self.attack_distance  = 100

        self.animation_num_max = 3
        self.attack_animation_num_max = 3
        self.attack_animation_num_cooldown_max = 100
        self.animation_num_cooldown_max = 100
        self.flame_thrower = Flame_Thrower(self.game)

    def Update(self, tilemap, delta_time, movement = (0, 0)):
        super().Update(tilemap, delta_time, movement)
        if self.effects.fire.effect:
            self.Set_Effect(keys.healing, self.effects.frozen.effect)
            self.Set_Effect(keys.fire_resistance, 2)



        
    
    def Attack(self, delta_time):
        if not super().Attack(delta_time):
            return
        
        if self.game.player.effects.invisibility.effect:
            return False
        
        # If Player is to close, then ice spirit cannot shoot
        if self.distance_to_player < 50:
            return False
        
        self.charge += delta_time

        if self.charge >= self.max_weapon_charge and not self.shooting_fire:
            self.shooting_fire = FIRE_PROJECTILE_NUM

        if self.shooting_fire:
            self.Shoot_Fire_Particle()

    
    
    def Shoot_Fire_Particle(self):
        self.Set_Target(self.game.player.pos)
        self.Set_Attack_Direction()
        self.shooting_fire = self.active_weapon.Particle_Creation(self, self.shooting_fire, 10)
        if not self.shooting_fire:
            self.charge = 0


    # TODO: IMPLEMENT
    def Look_For_Health(self, delta_time):
        if self.look_for_health_cooldown:
            self.look_for_health_cooldown = max(0, self.look_for_health_cooldown - delta_time)
            return
        

        if self.health < self.max_health / 2:
            self.Set_Locked_On_Target(0)

            self.look_for_health_cooldown = 30

            nearby_traps = self.game.trap_handler.Find_Nearby_Traps(self, 1000)
            for trap in nearby_traps:

                if trap.type == keys.lava_env:
                    self.game.enemy_handler.Add_To_Pathfinding_Queue(self, trap.pos)
                    self.locked_on_target = True
                    break

            self.Set_Locked_On_Target(50)
        
        return

