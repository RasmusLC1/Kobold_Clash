from scripts.entities.items.weapons.weapon import Weapon
from scripts.engine.keys.keys import keys

class Sceptre(Weapon):
    def __init__(self, game, pos, damage_type = 'blunt'):
        super().__init__(game, pos, keys.sceptre, 3, 2, 3, 100, 'one_handed_melee', damage_type)
        self.max_animation = 6
        self.attack_animation_max = 8
        self.heal_cooldown = 0

    def Update(self, offset=...):
        self.Update_Heal_Cooldown()
        return super().Update(offset)

    # Handle special attack charge
    def Special_Attack(self):
        if not self.entity:
            return
        
        if self.special_attack <= 0 or not self.equipped or self.heal_cooldown:
            # self.Reset_Special_Attack()
            return
        self.Heal_Entity()
        

    def Update_Heal_Cooldown(self):
        if not self.heal_cooldown:
            return
        self.heal_cooldown = max(0, self.heal_cooldown - 1)
    
    # Initialise the charge logic
    def Heal_Entity(self):
        self.entity.effects.Set_Effect(keys.healing, 5)
        self.heal_cooldown = 2000
        self.special_attack = 0
