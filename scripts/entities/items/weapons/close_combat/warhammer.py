from scripts.entities.items.weapons.weapon import Weapon
from scripts.engine.assets.keys import keys

# TODO: Add particle effect on hammer

class Warhammer(Weapon):
    def __init__(self, game, pos, damage_type = keys.blunt):
        super().__init__(game, pos, keys.warhammer, 9, 2, 6, 80, 'two_handed_melee', damage_type)
        self.max_animation = 5
        self.attack_animation_max = 5
        self.special_attack_effect_animation_max = 5



    def Special_Attack(self):
        if not self.special_attack_active or not self.equipped:
            return
        
        if self.special_attack <= 0:
            self.Reset_Special_Attack()
            return
        
        self.special_attack -= 1
        self.Smash_Attack_Effect()
        self.Smash_Attack()

        
    def Smash_Attack(self):
        if self.special_attack != self.max_charge_time // 2:
            return
        damage_holder = self.damage
        self.damage = 1 # quarter damage on stun
        # Stun nearby enemies
        self.nearby_enemies = self.game.enemy_handler.Find_Nearby_Enemies(self.entity, 3)
        for enemy in self.nearby_enemies:
            enemy.Set_Effect(keys.snare, self.max_charge_time * 2)
            self.Entity_Hit(enemy)

        self.damage = damage_holder # Reset Damage
        self.game.clatter.Generate_Clatter(self.pos, 500) # Generate clatter to alert nearby enemies
        return
    
        
    def Smash_Attack_Effect(self):
        self.attack_effect_handler.Update_Special_Attack_Effect_Animation()
        effect_type = self.Get_Dominant_Effect() + '_' + self.attack_type + '_' + keys.effect
        attack_effect = self.game.assets[effect_type][self.attack_effect_animation]
        pos_x = self.entity.pos[0] - self.game.render_scroll[0] - 10
        pos_y = self.entity.pos[1] - self.game.render_scroll[1] - 10
        self.game.display.blit(attack_effect, (pos_x, pos_y))



    def Set_Special_Attack(self, offset=...):
        self.attack_type = keys.smash
        super().Set_Special_Attack(offset)
        self.attack_effect_handler.Set_Special_Attack_Effect_Animation_Time()
    
    def Reset_Special_Attack(self):
        self.attack_type = keys.cut
        return super().Reset_Special_Attack()
