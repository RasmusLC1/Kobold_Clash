from scripts.entities.items.weapons.enemy_weapons.claw import Claw
from scripts.engine.keys.keys import keys
from scripts.entities.moving_entities.enemies.crystal_caverns.elementals.elemental import Elemental
from scripts.entities.items.weapons.magic_attacks.poison.poison_explosion import Poison_Explosion



class Poison_Elemental(Elemental):
    def __init__(self, game, pos, health, strength, max_speed, agility, intelligence, stamina):
        super().__init__(game, pos, keys.poison_elemental, health, strength, max_speed, agility, intelligence, stamina, 0.1, 20, (32, 32))
        self.path_finding_strategy = keys.void_spawn
        self.intent_manager.Set_Intent([keys.direct, keys.attack])




    # Returns true on succesful attack
    def Attack(self, delta_time):
        if self.distance_to_player > 64:
            return False
        
        if not self.rect().colliderect(self.game.player.rect()):
            return
        
        self.Explode()
        
        return True

    def Explode(self):
        poison_explosion = Poison_Explosion(self.game, self.pos, 2)
        self.game.item_handler.Add_Item(poison_explosion)
        self.Delete(generate_soul = False)

    def Improve_Weapon(self, effect, amount):
        return False