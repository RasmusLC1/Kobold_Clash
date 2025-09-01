from scripts.entities.items.weapons.enemy_weapons.claw import Claw
from scripts.engine.keys.keys import keys
from scripts.entities.moving_entities.enemies.crystal_caverns.elementals.elemental import Elemental

PLAYER_MAX_ATTACK_DISTANCE = 200

class Electric_Elemental(Elemental):
    def __init__(self, game, pos, health, strength, max_speed, agility, intelligence, stamina):
        super().__init__(game, pos, keys.electric_elemental, health, strength, max_speed, agility, intelligence, stamina, 2, 20)
        self.intent_manager.Set_Intent([keys.attack, keys.attack, keys.attack, keys.attack, keys.short_range])

        # Equip the weapon
        self.Equip_Weapon(Claw(game, self.pos)) 
        self.active_weapon.Set_Damage(keys.electric, 2)
        self.attack_distance = 250



    # Returns true on succesful attack
    def Attack(self, delta_time):
        if not super().Attack(delta_time):
            return False
        if not self.active_weapon:
            return False
        self.charge = min(self.max_weapon_charge, self.charge + delta_time)
        if self.charge < self.max_weapon_charge:
            return False
        
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
    
        
    def Update_Active_Weapon(self, delta_time):
        if not self.active_weapon:
            return

        self.active_weapon.Set_Equipped_Position(self.direction_y_holder)
        if not self.active_weapon:
            return
        
        self.active_weapon.Update_Attack(delta_time)

        return