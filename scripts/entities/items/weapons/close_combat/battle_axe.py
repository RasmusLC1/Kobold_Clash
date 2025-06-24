from scripts.entities.items.weapons.weapon import Weapon
import math
from scripts.engine.assets.keys import keys


class Battle_Axe(Weapon):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.battle_axe, 1, 2, 3, 70, 'two_handed_melee')
        self.max_animation = 4
        self.attack_animation_max = 14
        self.special_attack_effect_animation_max = 8
        self.spin_index = 0
        self.spin_countdown = 0
        self.spin_attack_directions = [[1, 0], [0, 1], [-1, 0], [0, -1]] # Attack direction for the entity



    def Special_Attack(self):
        if not self.special_attack_active or not self.equipped:
            return
        
        if self.special_attack <= 0:
            self.Reset_Special_Attack()
            
            return

        if not self.spin_countdown:
            self.spin_index = min(self.spin_index + 1, 3)

        self.spin_countdown -= 1
        self.rotate += 10
        self.Spin_Attack()
        self.special_attack -= 1
        self.Spin_Attack_Effect()
    
    def Spin_Attack(self):
        self.entity.Set_Attack_Direction(self.spin_attack_directions[self.spin_index])
        for enemy in self.nearby_enemies:
            distance = math.sqrt((self.entity.pos[0] - enemy.pos[0]) ** 2 + (self.entity.pos[1] - enemy.pos[1]) ** 2)
            if distance <= 40:
                self.Entity_Hit(enemy)
            

    def Set_Special_Attack(self, offset=...):
        self.attack_type = 'spin'
        super().Set_Special_Attack(offset)
        self.attack_effect_handler.Set_Special_Attack_Effect_Animation_Time()
        self.nearby_enemies = self.game.enemy_handler.Find_Nearby_Enemies(self.entity, 4)
    
    def Reset_Special_Attack(self):
        self.attack_type = keys.cut
        self.spin_countdown = 0
        
        return super().Reset_Special_Attack()

    def Spin_Attack_Effect(self):
        self.attack_effect_handler.Update_Special_Attack_Effect_Animation()
        effect_type = self.Get_Dominant_Effect() + '_' + self.attack_type + '_effect'
        attack_effect = self.game.assets[effect_type][self.attack_effect_handler.attack_effect_animation]
        pos_x = self.entity.pos[0] - self.game.render_scroll[0] - 10
        pos_y = self.entity.pos[1] - self.game.render_scroll[1] - 10
        self.game.display.blit(attack_effect, (pos_x, pos_y))


   
