from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.passive_ability import Passive_Ability
from scripts.engine.keys.keys import keys

class Healing_From_Damage_Type(Passive_Ability):
    def __init__(self, game, entity, name, effect_name):
        super().__init__(game, entity, name)
        self.effect_name = effect_name


    def Damage_Taken(self, damage, effect, direction, attacker):
        # If there's no effect or the effect doesn't match our specialty, take standard damage
        if not effect[0] or effect[0] != self.effect_name:
            return damage
        
        self.entity.Set_Effect(keys.healing, damage // 2)
        self.entity.Set_Effect(self.effect_name + '_resistance', 2)
        return 0