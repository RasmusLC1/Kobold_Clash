from scripts.entities.items.weapons.weapon import Weapon
import random
from scripts.engine.keys.keys import keys

class Halberd(Weapon):
    def __init__(self, game, pos, damage_type = 'slash'):
        super().__init__(game, pos, keys.halberd, 5, 2, 8, 50, 'two_handed_melee', damage_type)

        
    def Update_Attack(self, delta_time):
        if not super().Update_Attack(delta_time):
            return False
        self.Set_Block_Direction()
        self.Set_Attack_Type()
        

    # Handle special attack charge
    def Special_Attack(self):
        if not self.entity:
            return

        if self.special_attack <= 0 or not self.equipped:
            # self.Reset_Special_Attack()
            return
        self.Initialise_Charge()
        
        

    # Initialise the charge logic
    def Initialise_Charge(self):
        self.entity.Charge(self.game.render_scroll)
        self.special_attack = 0
