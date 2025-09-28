from scripts.entities.items.weapons.enemy_weapons.claw import Claw
from scripts.engine.keys.keys import keys
from scripts.entities.moving_entities.enemies.crystal_caverns.elementals.elemental import Elemental

PLAYER_MAX_ATTACK_DISTANCE = 200

class Electric_Elemental(Elemental):
    def __init__(self, game, pos, health, strength, max_speed, agility, intelligence, stamina):
        super().__init__(game, pos, keys.electric_elemental, health, strength, max_speed, agility, intelligence, stamina, 2, 20)
        self.intent_manager.Set_Intent([keys.attack, keys.attack, keys.attack, keys.attack, keys.short_range])
        self.animation_handler.Set_Animation_Num_Max(3)
        self.animation_handler.Set_Attack_Animation_Num_Max(3)
        self.animation_handler.Set_Attack_Animation_Num_Cooldown_Max(0.3)
        self.animation_handler.Set_Animation_Num_Cooldown_Max(0.7)
        # Equip the weapon
        self.Equip_Weapon(Claw(game, self.pos)) 
        self.active_weapon.Set_Damage(keys.electric, 2)
        self.attack_distance = 250

    def Update(self, tilemap, delta_time, movement=...):
        super().Update(tilemap, delta_time, movement)
        
        if self.effects.electric.effect:
            self.Set_Effect(keys.healing, self.effects.frozen.effect)
            self.Set_Effect(keys.frozen_resistance, 2)
        
        return True



    def Trigger_Attack(self):
        self.Set_Target(self.game.player.pos)
        self.Reset_Charge()
        
        if self.distance_to_player > PLAYER_MAX_ATTACK_DISTANCE:
            return False
        
        self.active_weapon.Entity_Hit(self.game.player)
        self.active_weapon.entity_attack_type.Set_player_Hit_Effect()
        return True

    def Equip_Weapon(self, weapon):
        if not weapon:
            return False

        weapon.Pickup_Reset_Weapon(self)
        weapon.Set_Equip(True, self)
        self.Set_Active_Weapon(weapon)

        self.active_weapon.render = False
        del(weapon)
        return True
    
        