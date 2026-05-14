from scripts.entities.moving_entities.enemies.enemy import Enemy
from scripts.entities.items.weapons.enemy_weapons.claw import Claw
import random
from scripts.engine.keys.keys import keys

class Void_Spawn(Enemy):
    def __init__(self, game, pos, type):
        super().__init__(game, pos, type)
        self.Equip_Weapon(Claw(game, self.pos)) 
        self.touching_ground = False


    def Tile_Map_Collision_Detection(self, tilemap):
        self.pos[0] += self.frame_movement[0]
        self.pos[1] += self.frame_movement[1]


    # Void spawn cannot be damaged by material damage
    def Damage_Taken(self, damage, effect= (keys.slash, 0), direction = (0, 0)):
        if effect[0] == keys.slash or effect[0] == keys.blunt:
            damage = 0
        
        return super().Damage_Taken(damage, effect, direction)


    
    def Spawn_Damaged_Particles(self):
        self.game.particle_handler.Activate_Particles(10, keys.bone_particle, self.rect().center)

    def Spawn_Bones(self):
        pass

