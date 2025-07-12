from scripts.engine.keys.keys import keys
from scripts.engine.ascension.Ascension_effects.spawn_enemies import Spawn_Enemies
from scripts.engine.ascension.Ascension_effects.block_doors import Block_Doors
from scripts.engine.ascension.Ascension_effects.buff_enemies import Buff_Enemies
from scripts.engine.ascension.Ascension_effects.player_debuff import Player_Debuff
from scripts.engine.ascension.Ascension_effects.spawn_elite import Spawn_Elite
from scripts.engine.ascension.Ascension_effects.replace_chest import Replace_Chests
import random

NOTHING = 0
SPAWN_ENEMY = 1
SPAWN_TRAP = 2
PLAYER_DEBUFF = 3
BUFF_ENEMIES = 4
BLOCK_DOORS = 5
REPLACE_CHESTS = 6
SPAWN_ELITE = 8
INCREASE_ASCENSION = 9

# Probability table for ascension levels
ASCENSION_TABLE = {
    0: {
        NOTHING : 4,
        SPAWN_ENEMY : 0.5,
        INCREASE_ASCENSION : 0.5,
    },
    1: {
        NOTHING : 5,
        SPAWN_ENEMY : 0.3,
        SPAWN_TRAP : 0.2,
        INCREASE_ASCENSION : 0.1,
    },
    2: {
        NOTHING : 6,
        SPAWN_ENEMY : 0.6,
        SPAWN_TRAP : 0.1,
        PLAYER_DEBUFF : 0.1,
        BUFF_ENEMIES : 0.3,
        INCREASE_ASCENSION : 0.08,
    },
    4: {
        NOTHING : 7,
        SPAWN_ENEMY : 0.7,
        SPAWN_TRAP : 0.1,
        PLAYER_DEBUFF : 0.1,
        BUFF_ENEMIES : 0.5,
        BLOCK_DOORS : 0.1,
        REPLACE_CHESTS : 0.1,
        INCREASE_ASCENSION : 0.05,
    },
    3: {
        NOTHING : 8,
        SPAWN_ENEMY : 1,
        PLAYER_DEBUFF : 0.2,
        BUFF_ENEMIES : 0.6,
        BLOCK_DOORS : 0.2,
        REPLACE_CHESTS : 0.1,
        SPAWN_ELITE : 0.1,
        INCREASE_ASCENSION : 0.03,
    },
    5: {
        NOTHING : 9,
        SPAWN_ENEMY : 1.1,
        PLAYER_DEBUFF : 0.2,
        BUFF_ENEMIES : 0.6,
        BLOCK_DOORS : 0.2,
        REPLACE_CHESTS : 0.2,
        SPAWN_ELITE : 0.3
    }
}

class Ascension():
    def __init__(self, game):
        self.game = game
        
        self.ascension_dic = {} # contains the Enum effect and probability adjusted for each ascension level

        self.max_ascension_level = 5

        self.spawn_enemies = Spawn_Enemies(game)
        self.block_doors = Block_Doors(game)
        self.buff_enemies = Buff_Enemies(game)
        self.player_debuff = Player_Debuff(game)
        self.spawn_elite = Spawn_Elite(game)
        self.replace_chests = Replace_Chests(game)

        self.ascension_functions = {
            NOTHING : None,
            SPAWN_ENEMY : self.spawn_enemies.Spawn_Enemy,
            SPAWN_TRAP : None, # Waiting for trap rework
            PLAYER_DEBUFF : self.player_debuff.Set_Effect,
            BUFF_ENEMIES : self.buff_enemies.Buff_Enemies,
            BLOCK_DOORS : self.block_doors.Block_Door,
            REPLACE_CHESTS : self.replace_chests.Replace_Chest,
            SPAWN_ELITE : self.spawn_elite.Spawn_Enemy,
            INCREASE_ASCENSION : self.Set_Ascension_Level(self.ascension_level + 1),
        }
        self.Set_Ascension_Level(0)

    def Set_Ascension_Level(self, new_ascension_level):
        if self.ascension_level == self.max_ascension_level:
            return
        self.ascension_level = max(0, min(self.max_ascension_level, new_ascension_level))
        self.Adjust_Difficulty()


    def Adjust_Difficulty(self):
        
        self.spawn_enemies.Set_Ascension_Level(self.ascension_level)
        self.buff_enemies.Set_Ascension_Level(self.ascension_level)
        self.player_debuff.Set_Ascension_Level(self.ascension_level)


        if self.ascension_level in ASCENSION_TABLE:
            self.ascension_dic = ASCENSION_TABLE.get(self.ascension_level)
        

    def Trigger_Ascension_Dic(self):
        effects = random.choices(
                    population=list(self.ascension_dic.keys()),
                    weights=list(self.ascension_dic.values()),
                    k=1
                )[0]
        
        ascension_function = self.ascension_functions.get(effects)

        if not ascension_function:
            return False
        
        ascension_function()
        return True
        

