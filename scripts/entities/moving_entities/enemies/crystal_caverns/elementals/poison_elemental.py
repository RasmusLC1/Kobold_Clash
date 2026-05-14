from scripts.entities.items.weapons.enemy_weapons.claw import Claw
from scripts.engine.keys.keys import keys
from scripts.entities.moving_entities.enemies.crystal_caverns.elementals.elemental import Elemental
from scripts.entities.items.weapons.magic_attacks.poison.poison_explosion import Poison_Explosion



class Poison_Elemental(Elemental):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.poison_elemental)
        self.explosion_strength = 2

    def Increase_Explosion_Strength(self):
        self.explosion_strength += 1

    def Update(self, tilemap, delta_time, movement=...):
        self.Explode_On_Impact()
        return super().Update(tilemap, delta_time, movement)

    # Returns true on succesful attack
    def Explode_On_Impact(self):
        # Skips the rest of the logic if not near the player
        if self.distance_to_player > 60:
            return False
        
        # Returns false if no entities have been pushed
        if not self.pushed_entities:
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