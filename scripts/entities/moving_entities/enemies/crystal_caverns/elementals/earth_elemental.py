from scripts.entities.items.weapons.enemy_weapons.claw import Claw
from scripts.engine.keys.keys import keys
from scripts.entities.moving_entities.enemies.crystal_caverns.elementals.elemental import Elemental


class Earth_Elemental(Elemental):
    def __init__(self, game, pos, health, strength, max_speed, agility, intelligence, stamina):
        super().__init__(game, pos, keys.earth_elemental, health, strength, max_speed, agility, intelligence, stamina, 1.5, 20, (48, 48))
        self.intent_manager.Set_Intent([keys.direct, keys.attack, keys.attack, keys.attack, keys.attack, keys.short_range])


        # Equip the weapon
        self.Equip_Weapon(Claw(game, self.pos)) 
        self.active_weapon.Set_Damage(keys.blunt, 5)



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
        self.active_weapon.Set_Attack()
        self.Reset_Charge()
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