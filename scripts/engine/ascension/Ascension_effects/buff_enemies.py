from scripts.engine.keys.keys import keys

import random

ASCENSION_TABLE = {
    0: {},  # Empty
    1: {},  # Empty
    2: {
        keys.fire_resistance: 1,
        keys.frozen_resistance: 1,
        keys.electric_resistance: 1,
        keys.poison_resistance: 1,
        keys.speed: 1,
        keys.increase_strength: 1,
        keys.healing: 0.5,
        keys.improve_weapon : 0.5
    },
    3: {
        keys.fire_resistance: 1,
        keys.frozen_resistance: 1,
        keys.electric_resistance: 1,
        keys.poison_resistance: 1,
        keys.speed: 1,
        keys.increase_strength: 2,
        keys.healing: 1,
        keys.increase_max_health : 1,
        keys.resistance: 0.5,
        keys.improve_weapon : 1.5
    },
    4: {
        keys.fire_resistance: 0.5,
        keys.frozen_resistance: 0.5,
        keys.electric_resistance: 0.5,
        keys.poison_resistance: 0.5,
        keys.speed: 1.5,
        keys.increase_strength: 3,
        keys.healing: 1.2,
        keys.regen: 1.2,
        keys.vampiric: 1,
        keys.increase_max_health : 2,
        keys.resistance: 2.5,
        keys.improve_weapon : 2.5
    },
    5: {
        keys.speed: 2,
        keys.increase_strength: 3,
        keys.healing: 2,
        keys.vampiric: 2,
        keys.regen: 3,
        keys.soul_stealer: 1,
        keys.increase_max_health : 3,
        keys.resistance: 3.5,
        keys.improve_weapon : 3.5
    },
}



class Buff_Enemies():
    def __init__(self, game):
        self.game = game 
        self.ascension_level = 0
        self.effects = {}

    def Set_Ascension_Level(self, ascension_level):
        self.ascension_level = ascension_level

        self.effects = ASCENSION_TABLE.get(self.ascension_level)


    def Buff_Enemies(self):
        if not self.effects:
            return
        
        enemies = self.game.enemy_handler.Find_Nearby_Enemies(self.game.player, 300)

        effect = random.choices(
                    population=list(self.effects.keys()),
                    weights=list(self.effects.values()),
                    k=1
                )[0]
        
        if not effect:
            return
        
        if effect == keys.improve_weapon:
            self.Improve_Weapons(enemies)
        else:
            self.Apply_Effects(effect, enemies)

    
    def Apply_Effects(self, effect, enemies):
        effect_modifier = 1
        if effect in (keys.increase_max_health, keys.healing):
            effect_modifier = 5


        for enemy in enemies:
            amount = random.randint(self.ascension_level, self.ascension_level * 2) * effect_modifier
            enemy.Set_Effect(effect, amount)
        

    def Improve_Weapons(self, enemies):
        effects = {
            keys.electric : 0.4,
            keys.fire : 0.5,
            keys.frozen : 0.5,
            keys.poison : 0.4,
            keys.slash : 1,
            keys.blunt : 1,
            keys.speed : 0.3,
            keys.strength : 0.3,
            keys.vampiric : 0.2,
            keys.vulnerable : 0.1,
            keys.weakness : 0.1,
            keys.wet : 0.4,
        }
        for enemy in enemies:
            amount = random.randint(1, self.ascension_level)
            effect = random.choices(
                    population=list(effects.keys()),
                    weights=list(effects.values()),
                    k=1
                )[0]
            enemy.Improve_Weapon(effect, amount)