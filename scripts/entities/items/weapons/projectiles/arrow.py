from scripts.entities.items.weapons.projectiles.projectile import Projectile
from scripts.engine.keys.keys import keys


class Arrow(Projectile):
    def __init__(self, game, pos, amount = 1, direction = (0,0), damage_type = 'slash'):
        super().__init__(game, pos, keys.arrow, 3, 6, 8, 10, keys.arrow,  damage_type, 50)
        self.max_animation = 0
        self.direction = direction  # Store the direction vector
        self.max_amount = 20
        self.amount = amount


    
    def Set_Speed(self, speed):
        self.speed = speed

    def Update_Flip(self):
        pass

    def Shooting_Setup(self, entity, direction):
        self.attack_animation_max = 0
        self.distance_from_player = 0
        self.entity = entity
        self.equipped = True
        self.in_inventory = True
        self.picked_up = False
        self.attacking = 10
        self.special_attack = 100
        self.direction = direction
        self.shoot_distance = self.special_attack



    
    def Shoot(self):
        if not self.shoot_speed:
            self.Initialise_Shooting(self.speed)
        # Use the stored direction to move the particle
        self.pos = list((
            self.pos[0] + self.direction[0] * self.shoot_speed,
            self.pos[1] + self.direction[1] * self.shoot_speed
        ))
        entity = super().Shoot()
        if entity:
            self.Set_Special_Attack(0)
        

    def Send_To_Inventory(self, inventory_slot, sending_inventory, receiving_inventory):
        if not self.Arrow_Inventory_Check(inventory_slot):
            return False
        return super().Send_To_Inventory(inventory_slot, sending_inventory, receiving_inventory)

    def Equip(self):
        self.game.player.Set_Active_Weapon(self, self.inventory_type)
        
        
    def Arrow_Inventory_Check(self, inventory_slot):
        if not 'arrow' in self.weapon_class:
            return True
        
        if not inventory_slot.inventory_type:
            return True
        if 'arrow' in inventory_slot.inventory_type:
            return True
        else:
            return False