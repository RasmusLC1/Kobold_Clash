from scripts.entities.items.weapons.ranged_weapons.ranged_weapon import Ranged_Weapon
from scripts.engine.keys.keys import keys


class Bow(Ranged_Weapon):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.bow, 3, 8, 10, 50)
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
            self.game.sound_handler.Play_Sound(keys.bow_draw, 1)

        if not self.is_charging:
            return

        if self.is_charging < self.max_charge_time:
            self.Update_Attack_Animation()

            return
        
        self.ready_to_shoot = True
