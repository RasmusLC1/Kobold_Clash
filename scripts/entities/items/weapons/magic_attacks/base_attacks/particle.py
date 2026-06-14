from scripts.entities.items.weapons.projectiles.projectile import Projectile
from scripts.engine.keys.keys import keys

class Particle(Projectile):
    def __init__(self, game, pos, type, damage, speed, range, max_charge_time, damage_type, shoot_distance):
        # Pass the values up clean
        super().__init__(game, pos, type, damage, speed, range, max_charge_time, keys.particle, damage_type, shoot_distance=shoot_distance, attack_types=keys.cut, size=(4, 4), add_to_tile=False, max_animation=3)
        self.disabled = True
        self.animation = 0
        self.pickup_allowed = False
        self.damage_type = damage_type
        self.temp_damage = 0

    def Save_Data(self):
        pass

    def Update(self, delta_time, offset=(0, 0)):
        if self.disabled:
            return
        
        entity = self.Shoot(delta_time)
        print(vars(self))
        # 2. Let the base items engine manage rendering setup 
        return super().Update(offset)
    
    def Shoot(self, delta_time):
        # First shot setup
        if not self.shoot_speed:
            self.Initialise_Shooting(self.speed)
        
        # Run standard parent Projectile logic (handles self.Move, tile checks, and damage)
        return super().Shoot(delta_time)

    def Reset_Shot(self):
        # Intercept the parent reset to disable it cleanly back into your pool
        self.Set_Disabled()

    def Set_Direction(self, direction):
        # FIX: Projectile uses attack_direction! Update both to stay perfectly safe.
        self.direction = direction
        self.attack_direction = direction

    def Delete_Item(self):
        self.Set_Disabled()

    def Set_special_attack(self, special_attack):
        self.special_attack = special_attack

    def Set_Speed(self, speed):
        self.speed = speed

    def Set_Disabled(self):
        self.disabled = True
        self.delete_countdown = 0
        self.Set_Position((-999, -999))
        self.special_attack = 0
        self.attack_direction = (0, 0)
        self.direction = (0, 0)
        self.shoot_speed = 0
        self.shoot_distance = 0
        self.Set_Entity(None)
        self.game.item_handler.Remove_Item(self)
        self.Set_Damage(self.damage_type, -1 * self.temp_damage)
        self.temp_damage = 0

    def Set_Enabled(self, pos, speed, special_attack, direction, entity, delete_countdown, damage):
        self.disabled = False
        self.game.item_handler.Add_Item(self)
        self.delete_countdown = delete_countdown
        
        # Feed the base positions
        if hasattr(pos, 'x'):  # Safe check if an actual Rect object gets delivered
            self.Set_Position((pos.x, pos.y))
        else:
            self.Set_Position(pos)
            
        self.Set_Speed(speed)
        self.Set_Direction(direction)
        self.Set_Entity(entity)
        self.Set_special_attack(special_attack)
        self.Set_Damage(self.damage_type, damage)
        self.temp_damage = damage

    def Update_Text_Box(self, hitbox_1, hitbox_2):
        pass
    
    def Render(self, surf, offset=(0, 0)):
        if self.disabled or not self.entity_image:
            return
        
        weapon_image = self.entity_image.convert_alpha()
        surf.blit(weapon_image, (self.pos[0] - offset[0], self.pos[1] - offset[1]))