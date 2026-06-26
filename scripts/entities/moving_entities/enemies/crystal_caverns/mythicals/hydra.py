from scripts.entities.moving_entities.enemies.enemy import Enemy
from scripts.entities.items.weapons.enemy_weapons.claw import Claw
from scripts.engine.keys.keys import keys

class Hydra(Enemy):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.hydra)
        # Equip the weapon
        self.Equip_Weapon(Claw(game, self.pos)) 
        self.active_weapon.Set_Damage(keys.slash, 7)
        self.Set_Effect(effect=keys.regen, duration=3, permanent=True)
        self.Set_Ability(keys.adaptability)
