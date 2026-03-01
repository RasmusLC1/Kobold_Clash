from scripts.entities.moving_entities.enemies.crystal_caverns.elementals.elemental import Elemental
from scripts.entities.items.weapons.magic_attacks.ice.ice_shooter import Ice_Shooter
from scripts.engine.keys.keys import keys

ICE_PROJECTILE_NUM = 3

class Ice_Spirit(Elemental):
    def __init__(self, game, pos, health, strength, max_speed, agility, intelligence, stamina):
        super().__init__(game, pos, keys.ice_spirit, health, strength, max_speed, agility, intelligence, stamina, 1.6, 20, 3, 3, 3)
        self.path_finding_strategy = 'standard'
        self.intent_manager.Set_Movement_Intent([keys.long_range])
        self.attack_distance  = 250
        self.shooting_ice = False
        self.ice_damage = 5
        self.minimum_distance = 50
        self.attack_cooldown = 0
        self.active_weapon = Ice_Shooter(self.game)

    def Update(self, tilemap, delta_time, movement = (0, 0)):
        super().Update(tilemap, delta_time, movement)

        self.active_weapon.Update(delta_time)

        
        return True

    def Attack(self, delta_time):
        # If Player is to close, then ice spirit cannot shoot
        if self.distance_to_player < self.minimum_distance:
            self.charge = 0
            return False
        if self.attack_cooldown > 0:
            self.attack_cooldown -= delta_time
            return False
        
        return super().Attack(delta_time)
    
    def Trigger_Attack(self):
        self.Set_Target(self.game.player.pos)
        self.Set_Attack_Direction()
        self.active_weapon.Initialise_Shooting(self, 2, self.ice_damage)
        self.attack_cooldown = 1

    def Handle_Frozen(self):
        frozen = self.effects.Get_Effect_Strength(keys.frozen)
        if not self.effects.Get_Effect_Strength(keys.frozen):
            return
        
        self.Set_Effect(keys.healing, frozen)
        self.Set_Effect(keys.frozen_resistance, frozen)
        
