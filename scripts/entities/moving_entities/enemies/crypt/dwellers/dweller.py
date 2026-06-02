from scripts.entities.moving_entities.enemies.enemy import Enemy
from scripts.entities.items.weapons.enemy_weapons.claw import Claw
from scripts.engine.keys.keys import keys

class Dweller(Enemy):
    def __init__(self, game, pos, type):
        super().__init__(game, pos, type)
        self.Equip_Weapon(Claw(game, self.pos)) 
        self.Set_Ability(keys.gloom_stalker)

    

    def Spawn_Damaged_Particles(self):
        self.game.particle_handler.Activate_Particles(10, keys.bone_particle, self.rect().center)
