from scripts.entities.moving_entities.enemies.enemy import Enemy
from scripts.entities.items.weapons.enemy_weapons.claw import Claw
from scripts.entities.moving_entities.enemies.crystal_caverns.mythicals.minotaur.minotaur_intent_manager import Minotaur_Intent_Manager
from scripts.engine.keys.keys import keys

ICE_PROJECTILE_NUM = 3 * 20
CRYSTAL_SCALE_HEALTH_COOLDOWN_MAX = 1 # heals 1 health every second

class Minotaur(Enemy):
    intent_manager_class = Minotaur_Intent_Manager

    def __init__(self, game, pos, health, strength, max_speed, agility, intelligence, stamina):
        super().__init__(game, pos, keys.minotaur, health, strength, max_speed, agility, intelligence, stamina, 0.9, keys.mythical, 100, size = (64, 64))
        self.animation_handler.Set_Animation_Num_Max(3)
        self.animation_handler.Set_Attack_Animation_Num_Max(5)
        self.intent_manager.Set_Intent([keys.keep_position, keys.direct, 'dash', keys.attack, keys.attack, keys.attack, keys.medium_range,])
        self.intent_manager.Set_Intent_Cooldown_Max(120)
        self.last_health_index = self.Calculate_Health_Index(self.health)
        # Equip the weapon
        self.Equip_Weapon(Claw(game, self.pos)) 
        self.active_weapon.Set_Damage(keys.slash, 5)


    def Update(self, tilemap, delta_time, movement=...):
        self.Enrage()
        return super().Update(tilemap, delta_time, movement)


    def Enrage(self):
        current_index = self.Calculate_Health_Index(self.health)
        if current_index < self.last_health_index:
            # Lost a bucket → enrage once
            self.Set_Strength(self.strength + 1)
            self.last_health_index = current_index

    # Cap the strength gain to +5
    def Calculate_Health_Index(self, health):
        health_fraction = health / self.max_health
        health_index = max(-1, min(int((1 - health_fraction) * 5), 5))  # Invert fraction and scale to index range
        return health_index
    
    def Equip_Weapon(self, weapon):
        if not weapon:
            return False

        weapon.Pickup_Reset_Weapon(self)
        weapon.Set_Equip(True, self)
        self.Set_Active_Weapon(weapon)
        

        self.active_weapon.render = False
        del(weapon)
        return True