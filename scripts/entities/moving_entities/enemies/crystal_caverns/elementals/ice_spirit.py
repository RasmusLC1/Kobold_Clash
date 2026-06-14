from scripts.entities.moving_entities.enemies.crystal_caverns.elementals.elemental import Elemental
from scripts.entities.items.weapons.magic_attacks.ice.ice_shooter import Ice_Shooter
from scripts.engine.keys.keys import keys

ICE_PROJECTILE_NUM = 3

class Ice_Spirit(Elemental):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.ice_spirit)
        # self.shooting_ice = False
        self.ice_damage = 5
        self.active_weapon = Ice_Shooter(self.game, self)

    def Update(self, tilemap, delta_time, movement = (0, 0)):
        super().Update(tilemap, delta_time, movement)

        self.active_weapon.Update(delta_time)

        
        return True


    def Handle_Frozen(self):
        frozen = self.effects.Get_Effect_Strength(keys.frozen)
        if not self.effects.Get_Effect_Strength(keys.frozen):
            return
        
        self.Set_Effect(keys.healing, frozen)
        self.Set_Effect(keys.frozen_resistance, frozen)
        
