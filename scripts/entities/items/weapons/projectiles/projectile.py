from scripts.entities.items.weapons.weapon import Weapon
from scripts.entities.items.weapons.weapon_functions.ranged_damage_handler_weapon import Ranged_Damage_Handler_Weapon
from scripts.engine.keys.keys import keys


class Projectile(Weapon):
    def __init__(self, game, pos, type, damage, speed, range, max_charge_time, weapon_class, effect, shoot_distance, attack_types = ['cut'], size = (32, 32), add_to_tile = True, max_animation = 5, amount=1, max_amount = 20):
        super().__init__(game, pos, type, damage, speed, range, max_charge_time=max_charge_time, weapon_class=weapon_class, effect=effect, attack_types=attack_types, size=size, add_to_tile=add_to_tile, max_animation=max_animation, amount=amount, max_amount=max_amount)
        self.speed = speed
        self.shoot_speed = 0
        self.shoot_distance = shoot_distance
        self.pickup_allowed = True
        self.shoot_distance_holder = shoot_distance
        self.entity_strength = 0
        self.attack_direction = (0, 0)
        self.is_projectile = True
        self.damage_handler = Ranged_Damage_Handler_Weapon(self, effect, damage)


    def Save_Data(self):
        super().Save_Data()
        self.saved_data['shoot_speed'] = self.shoot_speed
        self.saved_data['shoot_distance'] = self.shoot_distance
        self.saved_data['shoot_distance_holder'] = self.shoot_distance_holder


    def Load_Data(self, data):
        
        super().Load_Data(data)
        self.shoot_distance = data['shoot_distance'] 
        self.shoot_distance_holder = data['shoot_distance_holder'] 
        self.shoot_speed = data['shoot_speed']


    def Set_Special_Attack(self, offset= (0,0)):
        super().Set_Special_Attack(offset)
        if not self.entity:
            return
        
        if self.entity.category == keys.player:
            self.Point_Towards_Mouse_Player()
        else:
            self.Point_Towards_Mouse_Enemy()

    # Run once to setup the shooting
    def Initialise_Shooting(self, speed):
        if not self.shoot_speed:
            # Set the tile, so projectile can interact with environment
            self.Set_Tile()
            # Initialise the rendering
            self.active = 255
            self.render = True
            self.render_needs_update = True
            self.Update_Dark_Surface()

            self.shoot_distance = self.shoot_distance_holder
            self.shoot_speed = speed * 2
            self.damage_handler.Find_Nearby_Enemies()

            return True
        return False


    # Continously updated shooting effect
    def Shoot(self, delta_time):
        if not self.Update_Shoot_Distance():
            self.Reset_Shot()
            return

        if not self.entity:
            print("ENTIY NOT FOUND", self.type)
            return

        dir_x = self.pos[0] + self.attack_direction[0] * self.shoot_speed
        dir_y = self.pos[1] + self.attack_direction[1] * self.shoot_speed

        self.Update_Tile(self.pos)
        if not self.Check_Tile((dir_x, dir_y)):
            self.Reset_Shot()
            return None
        self.Move((dir_x, dir_y))
        entity_hit = None
        # Check for collision with enemy
        entity_hit = self.damage_handler.Attack_Collision_Check_Projectile()
        if entity_hit:
            self.Reset_Shot()
            return entity_hit
        return None
    
    # Reset the weapon after the maximum distance has been rached
    def Reset_Shot(self):
        self.entity = None
        self.shoot_speed = 0
        self.shoot_distance = 0
        self.special_attack = 0
        self.shoot_speed = 0
        self.picked_up = False
        self.equipped = False
        self.Set_Entity(None)
        return True



    def Update_Shoot_Distance(self):
        if not self.shoot_distance:
            return False
        
        self.shoot_distance = max(0, self.shoot_distance - 1)
        return True

    def Drop_Weapon_After_Shot(self):
        # Set the attack attributes
        entity = self.entity
        self.attack_direction = entity.attack_direction
        self.entity_strength = entity.strength


        if entity.category == keys.player:
            entity.Remove_Active_Weapon()
            self.entity = entity
            self.game.inventory.Remove_Item(self)
            self.game.item_handler.Add_Item(self)
        self.picked_up = False

    def Pick_Up(self):
        if self.delete_countdown or not self.pickup_allowed:
            return False
        return super().Pick_Up()
