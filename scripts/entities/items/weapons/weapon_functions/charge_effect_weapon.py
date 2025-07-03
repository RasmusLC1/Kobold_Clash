from scripts.engine.assets.keys import keys

# Responsible for showing the special attack charge of the weapon
class Charge_Effect_Weapon():
    def __init__(self, game, weapon):
        self.game = game
        self.weapon = weapon
        self.Set_Charge_Effect()
        self.charge_effect_animation = 0
        self.charge_effect_animation_max = 5
        self.charge_effect_cooldown = 0
        self.charge_effect_cooldown_max = (weapon.max_charge_time // self.charge_effect_animation_max) - (weapon.max_charge_time // 20)

    def Set_Charge_Effect(self):
        dominant_effect = self.weapon.Get_Dominant_Effect()
        if not dominant_effect:
            self.charge_effect = ''
            return
        self.charge_effect = dominant_effect  + '_charge_effect'


    def Reset_Charge_Effect(self):
        if not self.charge_effect_animation:
            return
        self.charge_effect_cooldown = 0
        self.charge_effect_animation = 0

    
    def Charge_Effect_Update(self):
        if self.charge_effect_cooldown < self.charge_effect_cooldown_max:
            self.charge_effect_cooldown += 1
            return
        
        self.charge_effect_cooldown = 0
        self.charge_effect_animation = min(self.charge_effect_animation_max, self.charge_effect_animation + 1)

    # Handle the charging effect when using special attacks
    def Render_Charge_Effect(self, surf, offset):
        entity = self.weapon.entity
        if self.weapon.charge_time <= 20 and entity:
            self.Reset_Charge_Effect()

            return
        if not entity:
            return
        if not entity.type == keys.player:
            return
        self.Charge_Effect_Update()
        charge_effect_animation = self.game.assets[self.charge_effect][self.charge_effect_animation].convert_alpha()

        charge_effect_animation.set_alpha(self.charge_effect_animation * 50)
        surf.blit(charge_effect_animation, (self.weapon.pos[0] - offset[0], self.weapon.pos[1] - offset[1]))
