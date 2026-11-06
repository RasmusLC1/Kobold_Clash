from scripts.entities.items.weapons.weapon import Weapon
from scripts.entities.items.weapons.projectiles.arrow import Arrow
from scripts.entities.items.weapons.ranged_weapons.ranged_weapon import Ranged_Weapon
from scripts.engine.keys.keys import keys



class Crossbow(Ranged_Weapon):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.crossbow, 5, 8, 10, 80, max_animation = 8)
        self.attack_animation_max = 2
        self.attack_animation_counter = 0
        self.attack_animation_time = self.max_charge_time / self.attack_animation_max
        

    # Charging the crossbow
    def Set_Weapon_Charge(self, offset):
        if not self.entity:
            return
        
        if self.entity.category == keys.enemy:
            self.Enemy_Shooting()
            return

        self.is_charging = self.game.mouse.hold_down_left
        
        if self.is_charging == 10:
            self.game.sound_handler.Play_Sound(keys.bow_draw, 1)

        if not self.is_charging or self.is_charging > self.max_charge_time:
            return
        if self.ready_to_shoot:
            self.Set_Attack()
            return
        

        if self.is_charging < self.max_charge_time:
            self.Update_Attack_Animation()

            return
        
        self.ready_to_shoot = True



    


