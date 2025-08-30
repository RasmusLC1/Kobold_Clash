from scripts.entities.moving_entities.enemies.crystal_caverns.elementals.elemental import Elemental
from scripts.entities.items.weapons.magic_attacks.fire.flame_thrower import Flame_Thrower
from scripts.engine.keys.keys import keys

FIRE_PROJECTILE_NUM = 2 * 20

class Fire_Spirit(Elemental):
    def __init__(self, game, pos, health, strength, max_speed, agility, intelligence, stamina):
        super().__init__(game, pos, keys.fire_spirit, health, strength, max_speed, agility, intelligence, stamina, 1.2, 20)
        self.animation_handler.Set_Animation_Num_Max(3)
        self.animation_handler.Set_Attack_Animation_Num_Max(3)
        self.animation_handler.Set_Attack_Animation_Num_Cooldown_Max(0.3)
        self.animation_handler.Set_Animation_Num_Cooldown_Max(0.7)
        self.path_finding_strategy = 'ignore_lava'
        self.attack_strategy = keys.medium_range
        self.intent_manager.Set_Intent([keys.attack])
        self.attack_distance  = 120
        self.minimum_distance = 30

        self.look_for_health_cooldown = 0
        self.fire_cooldown = 0
        self.shooting_fire = 0
        self.fire_damage = 3

        self.active_weapon = Flame_Thrower(self.game)

    def Update(self, tilemap, delta_time, movement = (0, 0)):
        if not super().Update(tilemap, delta_time, movement):
            return False
        if self.effects.fire.effect:
            self.Set_Effect(keys.healing, self.effects.frozen.effect)
            self.Set_Effect(keys.fire_resistance, 2)



        
    
    def Attack(self, delta_time):
        if not super().Attack(delta_time):
            return

        self.charge += delta_time

        if self.distance_to_player < self.minimum_distance:
            return False
        
        if self.charge >= self.max_weapon_charge and not self.shooting_fire:
            self.shooting_fire = FIRE_PROJECTILE_NUM

        if self.shooting_fire:
            self.Shoot_Fire_Particle()

    
    
    def Shoot_Fire_Particle(self):
        self.Set_Target(self.game.player.pos)
        self.Set_Attack_Direction()
        self.shooting_fire = self.active_weapon.Particle_Creation(self, self.shooting_fire, self.fire_damage)
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



    def Render_Weapons(self, surf, offset):
        pass