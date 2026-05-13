from scripts.entities.moving_entities.enemies.crystal_caverns.elementals.elemental import Elemental
from scripts.entities.items.weapons.magic_attacks.fire.flame_thrower import Flame_Thrower
from scripts.engine.keys.keys import keys

class Fire_Spirit(Elemental):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.fire_spirit, 3, 3, 3, attack_speed = (2, 2.5), path_finding_strategy = 'ignore_lava', default_range = keys.short_range)
        self.look_for_health_cooldown = 0
        self.fire_damage = 1

        self.active_weapon = Flame_Thrower(self.game, self)

    def Update(self, tilemap, delta_time, movement = (0, 0)):
        super().Update(tilemap, delta_time, movement)

        self.Check_If_On_Fire()
        
        self.active_weapon.Update(delta_time)

        
    def Check_If_On_Fire(self):
        fire = self.effects.Get_Effect_Strength(keys.fire)
        if not fire:
            return False
        
        self.Set_Effect(keys.healing, self.effects.frozen.effect)
        self.Set_Effect(keys.fire_resistance, 2)
        return True
    
    def Attack(self, delta_time):
        # If Player is to close, then ice spirit cannot shoot
        if self.distance_to_player < self.minimum_distance:
            self.charge = 0
            return False
        return super().Attack(delta_time)
    
    def Set_Attack_Triggered(self):
        self.Set_Target(self.game.player.pos)
        self.Set_Attack_Direction()
        self.active_weapon.Initialise_Shooting(self, 2, self.fire_damage)
    
    
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

