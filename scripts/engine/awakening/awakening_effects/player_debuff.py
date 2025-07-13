from scripts.engine.keys.keys import keys

import random

# TODO: Add more curses as they are developed
ASCENSION_TABLE = {
    0: {},  # Empty
    1: {},  # Empty
    2: {
        keys.weakness: 1,
        keys.slow: 1,
    },
    3: {
        keys.weakness: 1,
        keys.slow: 1,
        keys.snare: 0.5,
        keys.frozen: 1,
    },
    4: {
        keys.weakness: 1,
        keys.slow: 1,
        keys.snare: 0.5,
        keys.frozen: 1,
        keys.demonic_bargain: 1,
        keys.black_coin: 1,
        keys.temptress_embrace: 1,
    },
    5: {
        keys.weakness: 1,
        keys.slow: 1,
        keys.snare: 0.5,
        keys.frozen: 1,
        keys.demonic_bargain: 1,
        keys.black_coin: 1,
        keys.temptress_embrace: 1,
        keys.electric: 0.4,
        keys.poison: 0.4,
        keys.fire: 0.1,
    },
}



class Player_Debuff():
    def __init__(self, game):
        self.game = game
        self.awakening_level = 0
        self.effects = {}

    def Set_Awakening_Level(self, awakening_level):
        self.awakening_level = awakening_level

        self.effects = ASCENSION_TABLE.get(self.awakening_level, {})


    def Set_Effect(self):
        if not self.effects:
            return
        
        effect = random.choices(
                    population=list(self.effects.keys()),
                    weights=list(self.effects.values()),
                    k=1
                )[0]
        
        if not effect:
            return

        amount = random.randint(1, max(1, self.awakening_level))
        self.game.player.Set_Effect(effect, amount)
        self.game.sound_handler.Play_Sound(keys.debuff, 0.3)


