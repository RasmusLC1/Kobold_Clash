from scripts.entities.items.weapons.magic_attacks.base_attacks.elemental_ball import Elemental_Ball
from scripts.entities.items.weapons.magic_attacks.electric.electric_explosion import Electric_Explosion
from scripts.engine.keys.keys import keys

class Electric_Ball(Elemental_Ball):
    def __init__(self, game, pos, entity, damage, speed, special_attack, direction):
        super().__init__(game, pos, entity, keys.electric_ball, damage, speed, 2, keys.electric, 200, special_attack, direction)
        
        self.light_source = self.game.light_handler.Add_Light(self.pos, 3, self.tile)
        self.light_level = self.game.light_handler.Initialise_Light_Level(self.tile)
        self.update_light_cooldown = 0


    def Update_Light(self):
        if self.update_light_cooldown >= 30:
            self.light_source.Move_Light(self.pos, self.tile)
            self.update_light_cooldown = 0
            return
        
        self.update_light_cooldown += 1


    def Shoot(self):
        super().Shoot()
        self.Update_Light()

    def Reset_Shot(self):
        electric_explosion = Electric_Explosion(self.game, self.pos, self.damage)
        self.game.item_handler.Add_Item(electric_explosion)
        if self.light_source:
            self.game.light_handler.Remove_Light(self.light_source)
            del(self.light_source)
            self.light_source = None
        return super().Reset_Shot()

