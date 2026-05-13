from scripts.entities.items.weapons.enemy_weapons.claw import Claw
from scripts.engine.keys.keys import keys
from scripts.entities.moving_entities.enemies.crystal_caverns.elementals.elemental import Elemental
from scripts.entities.items.weapons.magic_attacks.poison.poison_explosion import Poison_Explosion



class Poison_Elemental(Elemental):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.poison_elemental, 3, 3, 3)
        self.explosion_strength = 2

    def Increase_Explosion_Strength(self):
        self.explosion_strength += 1

    # Returns true on succesful attack
    def Attack(self, delta_time):
        if self.distance_to_player > self.size[0] * 1.5:
            return False
        
        self.health = 0
        self.Delete(generate_soul = False)
        
        return True
    
    def Set_Attack_Triggered(self):
        pass

    def Improve_Weapon(self, effect, amount):
        return False
    
    def Delete(self, generate_soul=True):
        if not super().Delete(generate_soul):
            return False
        poison_explosion = Poison_Explosion(self.game, self.pos, self.explosion_strength)
        self.game.item_handler.Add_Item(poison_explosion)

        return True