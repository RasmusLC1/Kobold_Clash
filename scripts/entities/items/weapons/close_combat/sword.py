from scripts.entities.items.weapons.weapon import Weapon
import random
from scripts.engine.keys.keys import keys

class Sword(Weapon):
    def __init__(self, game, pos, effect = keys.slash):
        super().__init__(game, pos, keys.sword, 3, 6, 5, 50, 'one_handed_melee', effect)


        
    def Update_Attack(self, delta_time):
        if not super().Update_Attack(delta_time):
            return False
        self.Set_Block_Direction()


    # Handle special attack charge
    def Special_Attack(self):
        if not self.entity:
            return
        

        if self.special_attack <= 0 or not self.equipped:
            self.Reset_Special_Attack()
            return
        self.Initialise_Charge()
        

    # Initialise the charge logic
    def Initialise_Charge(self):
        self.stored_rotation = self.rotate
        self.entity.Set_Charge(self.special_attack)
        self.nearby_enemies = self.game.enemy_handler.Find_Nearby_Enemies(self.entity, 8 * 32) # Find nearby enemies to attack
        self.special_attack = 0
