from scripts.entities.items.weapons.weapon import Weapon
from scripts.engine.assets.keys import keys

class Claw(Weapon):
    def __init__(self, game, pos, damage_type = keys.slash):
        super().__init__(game, pos, keys.claw, 1, 1, 3, 50, 'one_handed_melee', damage_type)
        self.max_animation = 7
        self.attack_animation_max = 8

    def Set_Description(self):
        pass

    def Set_Sprite(self):
        pass

    def Set_Entity_Image(self):
        pass

    def Update_Dark_Surface_Enemy(self, alpha_value):
        pass

    
    def Render(self, surf, offset=...):
        pass

    def Render_Equipped(self, surf, offset=(0, 0)):
        pass

    def Render_Equipped_Enemy(self, surf, offset=...):
        pass