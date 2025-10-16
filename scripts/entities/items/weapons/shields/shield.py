from scripts.entities.items.weapons.weapon import Weapon
from scripts.engine.keys.keys import keys


class Shield(Weapon):
    def __init__(self, game, pos, damage_type = 'block'):
        super().__init__(game, pos, keys.shield, 2, 5, 2, keys.shield, damage_type)
        # self.charging = 0 # Charging value will be alligned with the entity's
        self.blocking = 0

    

    def Set_Attack(self):
        pass
      

    def Set_Weapon_Charge(self, offset = (0, 0)):
        try:
            # Check that the weapon is in a weapon inventory
            if not self.inventory_type:
                return
            self.Set_Charging_Player()
            self.Player_Blocking()
        except TypeError as e:
            print(f"Shield blocking error{e}")
        
        if not self.inventory_type:
            return

        self.Set_Charging_Player()

    
    def Player_Blocking(self):
        if self.is_charging:
            self.entity.Attack_Direction_Handler()
            self.entity.Set_Block_Direction(self.entity.target)
            self.blocking = 4
            return
        
        if self.blocking:
            self.entity.Set_Block_Direction((0,0))
            self.blocking = 0
            return




    def Set_Equipped_Position(self, direction_y):
        offset_x = 0
        if self.entity.animation_handler.flip[0] and not self.attacking:
            self.flip_image = True
        else:
            self.flip_image = False
        if 'left' in self.inventory_type:
            if self.entity.direction_y < 0:
                self.Move((self.entity.pos[0] + offset_x , self.entity.pos[1] - self.blocking))
            else:
                if not self.attacking:
                    offset_x = self.Rotate_Left()
                self.Move((self.entity.pos[0] + offset_x , self.entity.pos[1] + 5 - self.blocking))
        elif 'right' in self.inventory_type:
            if  self.entity.direction_y < 0:
                self.Move((self.entity.pos[0] + offset_x , self.entity.pos[1] - self.blocking))
            else:
                if not self.attacking:
                    offset_x = self.Rotate_Right()
                self.Move((self.entity.pos[0] + offset_x, self.entity.pos[1] + 5 - self.blocking))
        else:
            print("DIRECTION NOT FOUND", self.inventory_type)




    def Rotate_Left(self):
        if self.flip_image:
            offset_x = 2
        else:
            offset_x = 4
        return offset_x
        
    def Rotate_Right(self):
        if self.flip_image:
            offset_x = -4
        else:
            offset_x = -2
        return offset_x

    def Update_Flip(self):
        pass