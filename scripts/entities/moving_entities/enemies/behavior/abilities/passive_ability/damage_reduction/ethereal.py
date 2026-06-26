from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.passive_ability import Passive_Ability
from scripts.engine.keys.keys import keys

class Ethereal(Passive_Ability):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name)
        self.entity.Set_Ethereal(True)


    def Damage_Taken(self, damage, effect, direction, attacker):
        if effect[0] == keys.slash or effect[0] == keys.blunt:
            damage = 0
        
        return damage
    