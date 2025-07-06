from scripts.entities.items.weapons.projectiles.projectile import Projectile

from scripts.entities.items.weapons.magic_attacks.fire.fire_explosion import Fire_Explosion
from scripts.entities.items.weapons.magic_attacks.ice.ice_explosion import Ice_Explosion
from scripts.entities.items.weapons.magic_attacks.poison.poison_explosion import Poison_Explosion
from scripts.entities.items.weapons.magic_attacks.vampiric.soul_pit import Soul_Pit
from scripts.entities.items.weapons.magic_attacks.electric.electric_explosion import Electric_Explosion
import math
from scripts.engine.keys.keys import keys

class Bomb(Projectile):
    def __init__(self, game, pos, shoot_distance):
        super().__init__(game, pos, keys.fire_bomb, 1, 2, 2, 40, keys.bomb, keys.blunt, shoot_distance, keys.cut, (20, 20), False)
        self.target = None
        self.distance_to_target = 99999
        self.disabled = True


        self.explosions = {
            keys.fire_bomb : Fire_Explosion,
            keys.frozen_bomb : Ice_Explosion,
            keys.electric_bomb :  Electric_Explosion,
            keys.poison_bomb :  Poison_Explosion,
            keys.vampiric_bomb : Soul_Pit,
        }

    def Set_Type(self, type):
        self.type = type

    def Save_Data(self):
        pass

    def Update(self, offset=...):
        if self.disabled:
            return
        return super().Update(offset)

    def Shoot(self):
        if not self.shoot_speed:
            self.Initialise_Shooting(self.speed)
        self.Calculate_Distance_To_Target()

        if self.distance_to_target < 5:
            self.Reset_Shot()
            return

        super().Shoot()


    def Calculate_Distance_To_Target(self):
        self.distance_to_target =  math.sqrt((self.pos[0] - self.target[0]) ** 2 + (self.pos[1] - self.target[1]) ** 2)

    def Reset_Shot(self):
        self.Set_Disabled()
        super().Reset_Shot()

    def Spawn_Explosion(self):
        explosion_type = self.explosions.get(self.type)
        explosion = explosion_type(self.game, self.pos, 4)
        self.game.item_handler.Add_Item(explosion)

    def Set_Direction(self, direction):
        self.attack_direction = direction
    
    def Set_Speed(self, speed):
        self.speed = speed

    def Set_Disabled(self):
        self.Spawn_Explosion()
        self.disabled = True
        self.Set_Position((-999, -999))
        self.Set_Special_Attack(0)
        self.Set_Direction((0,0))
        self.Set_Entity(None)
        self.Set_Speed(0)
        self.game.item_handler.Remove_Item(self)


    def Set_Enabled(self, pos, speed, special_attack, direction, target, entity, bomb_type, delete_countdown):
        self.disabled = False
        self.game.item_handler.Add_Item(self)
        self.delete_countdown = delete_countdown
        self.type = bomb_type
        self.sub_type = bomb_type
        self.target = target
        self.Set_Sprite()
        self.Set_Position(pos)
        self.Set_Speed(speed)
        self.Set_Direction(direction)
        self.Set_Entity(entity)
        self.Set_Special_Attack(special_attack)

    
    def Update_Text_Box(self, hitbox_1, hitbox_2):
        pass

    # Own render function since we don't need to compute light
    def Render(self, surf, offset=(0, 0)):
        if self.disabled:
            return
        
        weapon_image = self.entity_image.convert_alpha()

        surf.blit(weapon_image, (self.pos[0] - offset[0], self.pos[1] - offset[1]))

