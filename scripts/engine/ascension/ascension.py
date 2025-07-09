from scripts.engine.keys.keys import keys
import random

NOTHING = 0
SPAWN_ENEMY = 1
SPAWN_TRAP = 2
PLAYER_DEBUFF = 3
BUFF_ENEMIES = 4
BLOCK_DOORS = 5
REPLACE_CHESTS = 6
REDUCE_LIGHT = 7
SPAWN_ELITE = 8
INCREASE_ASCENSION = 9


class Ascension():
    def __init__(self, game):
        self.game = game
        self.ascension_dic = {}
    
    def Ascension_0_dict(self):
        self.ascension_dic = {
            NOTHING : 4,
            SPAWN_ENEMY : 0.5,
            INCREASE_ASCENSION : 0.5,
        }

    def Ascension_1_dict(self):
        self.ascension_dic = {
            NOTHING : 5,
            SPAWN_ENEMY : 0.3,
            SPAWN_TRAP : 0.2,
            INCREASE_ASCENSION : 0.1,
        }

    
    def Ascension_2_dict(self):
        self.ascension_dic = {
            NOTHING : 6,
            SPAWN_ENEMY : 0.6,
            SPAWN_TRAP : 0.1,
            PLAYER_DEBUFF : 0.1,
            BUFF_ENEMIES : 0.3,
            INCREASE_ASCENSION : 0.08,
        }

    def Ascension_3_dict(self):
        self.ascension_dic = {
            NOTHING : 7,
            SPAWN_ENEMY : 0.7,
            SPAWN_TRAP : 0.1,
            PLAYER_DEBUFF : 0.1,
            BUFF_ENEMIES : 0.5,
            BLOCK_DOORS : 0.1,
            REPLACE_CHESTS : 0.1,
            INCREASE_ASCENSION : 0.05,
        }

    def Ascension_4_dict(self):
        self.ascension_dic = {
            NOTHING : 8,
            SPAWN_ENEMY : 1,
            PLAYER_DEBUFF : 0.2,
            BUFF_ENEMIES : 0.6,
            BLOCK_DOORS : 0.2,
            REPLACE_CHESTS : 0.1,
            REDUCE_LIGHT : 0.07,
            SPAWN_ELITE : 0.1,
            INCREASE_ASCENSION : 0.03,
        }

    def Ascension_5_dict(self):
        self.ascension_dic = {
            NOTHING : 9,
            SPAWN_ENEMY : 1.1,
            PLAYER_DEBUFF : 0.2,
            BUFF_ENEMIES : 0.6,
            BLOCK_DOORS : 0.2,
            REPLACE_CHESTS : 0.2,
            REDUCE_LIGHT : 0.2,
            SPAWN_ELITE : 0.3
        }