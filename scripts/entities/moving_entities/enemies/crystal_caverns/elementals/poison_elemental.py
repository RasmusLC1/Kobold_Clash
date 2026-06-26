from scripts.entities.moving_entities.enemies.crystal_caverns.elementals.elemental import Elemental
from scripts.entities.items.weapons.magic_attacks.poison.poison_explosion import Poison_Explosion
from scripts.engine.keys.keys import keys

class Poison_Elemental(Elemental):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.poison_elemental)
        self.explosion_strength = 2
        
        # Equip the new passive ability
        self.Set_Ability(keys.explode_on_impact)

    def Increase_Explosion_Strength(self):
        self.explosion_strength += 1

    def Delete(self, generate_soul=True):
        if not super().Delete(generate_soul):
            return False
            
        # The explosion spawning stays linked to the death lifecycle hook
        poison_explosion = Poison_Explosion(self.game, self.pos, self.explosion_strength)
        self.game.item_handler.Add_Item(poison_explosion)

        return True