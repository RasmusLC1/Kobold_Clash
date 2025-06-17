from scripts.entities.items.weapons.ranged_weapons.ranged_weapon import Ranged_Weapon
from scripts.entities.items.weapons.magic_attacks.electric.electric_shooter import Electric_Shooter
from scripts.entities.items.weapons.magic_attacks.fire.flame_thrower import Flame_Thrower
from scripts.entities.items.weapons.magic_attacks.ice.ice_shooter import Ice_Shooter
from scripts.entities.items.weapons.magic_attacks.vampiric.soul_reap_shooter import Soul_Reap_Shooter 
from scripts.engine.assets.keys import keys
import random

class Magic_Staff(Ranged_Weapon):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.magic_staff, 3, 8, 10, 50)
        self.max_animation = 0
        self.attack_animation_max = 2
        self.attack_animation_counter = 0

    # Charging the crossbow
    def Set_Weapon_Charge(self, offset):
        if not self.entity:
            return
        if self.entity.category == keys.enemy:
            self.Enemy_Shooting()
            return


        self.is_charging = self.game.mouse.hold_down_left

        if not self.is_charging and self.ready_to_shoot:
            self.Set_Attack()
            self.ready_to_shoot = False
            return

        
        if self.is_charging == 10:
            self.game.sound_handler.Play_Sound('bow_draw', 1)

        if not self.is_charging:
            return

        if self.is_charging < self.max_charge_time:
            self.Update_Attack_Animation()

            return
        
        self.ready_to_shoot = True


    def Set_Type(self):
        types = {
                keys.magic_staff_electric : Electric_Shooter,
                keys.magic_staff_fire : Flame_Thrower,
                keys.magic_staff_frozen : Ice_Shooter,
                keys.magic_staff_vampiric : Soul_Reap_Shooter,
                # keys.magic_staff_electric : Electric_Shooter,
                 }
        self.sub_type = random.choice(types)
        