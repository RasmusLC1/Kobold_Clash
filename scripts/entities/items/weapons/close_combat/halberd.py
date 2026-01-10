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
        
        if self.Charge():
            return
        
        if self.special_attack <= 0 or not self.equipped:
            # self.Reset_Special_Attack()
            return
        self.Initialise_Charge()
        
        
    # Handle charging logic, return True if successful else False
    def Charge(self):
        if not self.entity.charging:
            return False
        self.rotate = self.stored_rotation
        new_x_pos = self.entity.pos[0] + self.entity.attack_direction[0] * 10
        new_y_pos = self.entity.pos[1] + self.entity.attack_direction[1] * 10
        self.Move((new_x_pos, new_y_pos))
        # self.Player_Attack_Collision_Check()
        return True
    
    # Initialise the charge logic
    def Initialise_Charge(self):
        self.stored_rotation = self.rotate
        self.entity.Set_Charge(self.special_attack // 4)
        self.nearby_enemies = self.game.enemy_handler.Find_Nearby_Enemies(self.entity, 8 * 32) # Find nearby enemies to attack
        self.special_attack = 0
