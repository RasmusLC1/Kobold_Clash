from scripts.entities.moving_entities.enemies.behavior.abilities.ability import Ability

COOLDOWN_TIME = 0

class Passive_Ability(Ability):
    def __init__(self, game, entity, name, can_attack_while_triggered = True):
        super().__init__(game, entity, name, can_attack_while_triggered, is_passive = True)

    