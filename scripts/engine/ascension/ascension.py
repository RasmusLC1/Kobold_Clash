from scripts.engine.keys.keys import keys
from scripts.engine.ascension.Ascension_effects.spawn_enemies import Spawn_Enemies
import random




class Ascension():
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


    def __init__(self, game):
        self.game = game
        self.ascension_dic = {}
        self.spawn_enemies = Spawn_Enemies(game)
        self.Set_Ascension_Level(0)

    def Set_Ascension_Level(self, new_ascension_level):
        self.acension_level = max(0, min(5, new_ascension_level))
        self.Adjust_Difficulty()


    def Adjust_Difficulty(self):
        
        self.spawn_enemies.Adjust_Difficulty(self.acension_level)

        if self.acension_level == 0:
            self.Set_Ascension_0_dict()
        elif self.acension_level == 1:
            self.Set_Ascension_1_dict()
        elif self.acension_level == 2:
            self.Set_Ascension_2_dict()
        elif self.acension_level == 3:
            self.Set_Ascension_3_dict()
        elif self.acension_level == 4:
            self.Set_Ascension_4_dict()
        elif self.acension_level == 5:
            self.Set_Ascension_5_dict()
        else:
            print("ERROR ASCENSION LEVEL NOT FOUND", self.acension_level)

    def Trigger_Ascension_Dic(self):
        effects = random.choices(
                    population=list(self.ascension_dic.keys()),
                    weights=list(self.ascension_dic.values()),
                    k=1
                )[0]
        


    
    def Set_Ascension_0_dict(self):
        self.ascension_dic = {
            NOTHING : 4,
            SPAWN_ENEMY : 0.5,
            INCREASE_ASCENSION : 0.5,
        }

    def Set_Ascension_1_dict(self):
        self.ascension_dic = {
            NOTHING : 5,
            SPAWN_ENEMY : 0.3,
            SPAWN_TRAP : 0.2,
            INCREASE_ASCENSION : 0.1,
        }

    
    def Set_Ascension_2_dict(self):
        self.ascension_dic = {
            NOTHING : 6,
            SPAWN_ENEMY : 0.6,
            SPAWN_TRAP : 0.1,
            PLAYER_DEBUFF : 0.1,
            BUFF_ENEMIES : 0.3,
            INCREASE_ASCENSION : 0.08,
        }

    def Set_Ascension_3_dict(self):
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

    def Set_Ascension_4_dict(self):
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

    def Set_Ascension_5_dict(self):
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