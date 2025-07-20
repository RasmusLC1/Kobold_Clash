from scripts.entities.items.weapons.weapon import Weapon
import random
from scripts.engine.keys.keys import keys

class Sword(Weapon):
    def __init__(self, game, pos, effect = keys.slash):
        super().__init__(game, pos, keys.sword, 3, 6, 5, 50, 'one_handed_melee', effect)
        self.max_animation = 3
        self.attack_animation_max = 3 

        
    def Update_Attack(self, delta_time):
        if not super().Update_Attack(delta_time):
            return False
        self.Set_Block_Direction()
        self.Set_Attack_Type()
        
        
    def Set_Attack_Type(self):
        if self.attack_type == keys.cut: # Handle Slashing
            self.Slash_Attack()
        else: # Handle Stabbing
            self.Stabbing_Attack() 


    def Set_Attack(self):
        self.attack_type = random.choice([keys.cut, keys.stab]) # Set either cut or stab
        return super().Set_Attack()


    # Handle special attack charge
    def Special_Attack(self):
        if not self.entity:
            return
        
        if self.Charge():
            return
        
        if self.special_attack <= 0 or not self.equipped:
            self.Reset_Special_Attack()
            return
        self.Initialise_Charge()
        


        
    # Handle charging logic, return True if successful else False
    def Charge(self):
        if not self.entity.charging:
            return False
        self.rotate = self.stored_rotation
        new_x_pos = self.entity.pos[0] + self.entity.attack_direction[0] * 20
        new_y_pos = self.entity.pos[1] + self.entity.attack_direction[1] * 20
        self.Move((new_x_pos, new_y_pos))
        # self.Player_Attack_Collision_Check()
        return True
    
    # Initialise the charge logic
    def Initialise_Charge(self):
        self.stored_rotation = self.rotate
        self.entity.Set_Charge(self.special_attack)
        self.nearby_enemies = self.game.enemy_handler.Find_Nearby_Enemies(self.entity, 8 * 32) # Find nearby enemies to attack
        self.special_attack = 0
