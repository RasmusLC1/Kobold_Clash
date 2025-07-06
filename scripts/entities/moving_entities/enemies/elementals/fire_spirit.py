from scripts.entities.moving_entities.enemies.enemy import Enemy
from scripts.entities.items.weapons.magic_attacks.fire.flame_thrower import Flame_Thrower
from scripts.engine.assets.keys import keys


class Fire_Spirit(Enemy):
    def __init__(self, game, pos, type, health, strength, max_speed, agility, intelligence, stamina):
        super().__init__(game, pos, type, health, strength, max_speed, agility, intelligence, stamina, 100, 'elemental', 20)
        
        self.animation = 'fire_spirit_idle'
        self.path_finding_strategy = 'ignore_lava'
        self.attack_strategy = keys.medium_range
        self.intent_manager.Set_Intent([keys.attack])

        self.look_for_health_cooldown = 0
        self.fire_cooldown = 0
        self.spewing_fire = False

        self.animation_num_max = 3
        self.attack_animation_num_max = 3
        self.attack_animation_num_cooldown_max = 100
        self.animation_num_cooldown_max = 100
        self.flame_thrower = Flame_Thrower(self.game)

    def Update(self, tilemap, movement = (0, 0)):
        
        super().Update(tilemap, movement)

        self.Look_For_Health()

        if self.distance_to_player < 120:
            self.Attack()

        if self.distance_to_player > 150 and self.charge:
            self.charge = 0


        
    
    def Attack(self):
        if not super().Attack():
            return False
        
        # If Player is to close, then archer cannot shoot
        if self.distance_to_player < 30:
            return False

        self.charge += 1
        if self.charge >= self.max_weapon_charge:
            self.spewing_fire = True

        if self.spewing_fire:
            self.Shoot_Fire()

        if self.charge <= 0:
            self.spewing_fire = False
    
    def Shoot_Fire(self):
        self.Set_Target(self.game.player.pos)
        self.Set_Attack_Direction()
        self.charge = self.flame_thrower.Particle_Creation(self, self.charge, 5)


    # TODO: IMPLEMENT
    def Look_For_Health(self):
        if self.look_for_health_cooldown:
            self.look_for_health_cooldown = max(0, self.look_for_health_cooldown - 1)
            return
        

        if self.health < self.max_health / 2:
            self.Set_Locked_On_Target(0)

            self.look_for_health_cooldown = 2000

            nearby_traps = self.game.trap_handler.Find_Nearby_Traps(self, 200)
            for trap in nearby_traps:

                if trap.type == keys.lava_env:
                    self.game.enemy_handler.Add_To_Pathfinding_Queue(self, trap.pos)
                    self.locked_on_target = True
                    break

            self.Set_Locked_On_Target(4000)
        
        return


    def Set_Action(self, movement = None):
        if not movement:
            return
        if movement[1] or movement[0]:
            self.animation_handler.Set_Animation('running')
            return
        
        self.animation_handler.Set_Animation(keys.idle)

    def Set_On_Fire(self, fire_time):
        self.effects.Set_Effect(keys.healing, fire_time)
        return False