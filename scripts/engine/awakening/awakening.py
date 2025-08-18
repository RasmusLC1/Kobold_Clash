from scripts.engine.keys.keys import keys
from scripts.engine.awakening.awakening_effects.spawn_enemies import Spawn_Enemies
from scripts.engine.awakening.awakening_effects.block_doors import Block_Doors
from scripts.engine.awakening.awakening_effects.buff_enemies import Buff_Enemies
from scripts.engine.awakening.awakening_effects.player_debuff import Player_Debuff
from scripts.engine.awakening.awakening_effects.spawn_elite import Spawn_Elite
from scripts.engine.awakening.awakening_effects.replace_chest import Replace_Chests
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

BASE_MAX_ENEMIES = 12
BASE_MIN_ENEMIES = 5

# Probability table for awakening levels
ASCENSION_TABLE = {
    0: {
        NOTHING : 1.2,
        SPAWN_ENEMY : 0.5,
        INCREASE_ASCENSION : 1,
    },
    1: {
        NOTHING : 1,
        SPAWN_ENEMY : 0.3,
        SPAWN_TRAP : 0.2,
        INCREASE_ASCENSION : 0.2,
    },
    2: {
        NOTHING : 1,
        SPAWN_ENEMY : 0.6,
        SPAWN_TRAP : 0.1,
        PLAYER_DEBUFF : 0.1,
        BUFF_ENEMIES : 0.5,
        INCREASE_ASCENSION : 0.2,
    },
    3: {
        NOTHING : 1,
        SPAWN_ENEMY : 0.7,
        SPAWN_TRAP : 0.1,
        PLAYER_DEBUFF : 0.2,
        BUFF_ENEMIES : 0.5,
        BLOCK_DOORS : 0.2,
        REPLACE_CHESTS : 0.2,
        INCREASE_ASCENSION : 0.2,
    },
    4: {
        NOTHING : 1,
        SPAWN_ENEMY : 1,
        PLAYER_DEBUFF : 0.2,
        BUFF_ENEMIES : 0.6,
        BLOCK_DOORS : 0.2,
        REPLACE_CHESTS : 0.2,
        SPAWN_ELITE : 0.1,
        INCREASE_ASCENSION : 0.2,
    },
    5: {
        NOTHING : 1,
        SPAWN_ENEMY : 1.1,
        PLAYER_DEBUFF : 0.2,
        BUFF_ENEMIES : 0.6,
        BLOCK_DOORS : 0.2,
        REPLACE_CHESTS : 0.2,
        SPAWN_ELITE : 0.3
    }
}

class Awakening():
    def __init__(self, game):
        self.game = game
        

        self.max_awakening_level = 5
        self.awakening_cooldown = 0
        self.awakening_level = 0
        self.awakening_dic = ASCENSION_TABLE.get(self.awakening_level)
        self.max_enemies = BASE_MIN_ENEMIES 

        self.spawn_enemies = Spawn_Enemies(game)
        self.block_doors = Block_Doors(game)
        self.buff_enemies = Buff_Enemies(game)
        self.player_debuff = Player_Debuff(game)
        self.spawn_elite = Spawn_Elite(game)
        self.replace_chests = Replace_Chests(game)

        self.awakening_functions = {
            NOTHING : None,
            SPAWN_ENEMY : self.spawn_enemies.Add_To_Spawn_Queue,
            SPAWN_TRAP : None, # Waiting for trap rework
            PLAYER_DEBUFF : self.player_debuff.Set_Effect,
            BUFF_ENEMIES : self.buff_enemies.Buff_Enemies,
            BLOCK_DOORS : self.block_doors.Block_Door,
            REPLACE_CHESTS : self.replace_chests.Replace_Chest,
            SPAWN_ELITE : self.spawn_elite.Spawn_Enemy,
            INCREASE_ASCENSION : self.Set_Awakening_Level,
        }

    def Update(self):
        self.spawn_enemies.Update_Enemy_Queue()

    def Set_Awakening_Level(self, new_awakening_level):
        if self.awakening_cooldown > 0:
            return
        
        if self.awakening_level == self.max_awakening_level:
            return
        
        self.awakening_level = max(0, min(self.max_awakening_level, new_awakening_level))
        self.Adjust_Difficulty()

        self.awakening_cooldown = random.randint(self.awakening_level, self.awakening_level * 3)
        self.Set_Max_Enemies()
        self.game.sound_handler.Set_HeartBeat_Sound(self.awakening_level)
        self.game.ui_handler.Set_Awakening_Level(self.awakening_level)


    def Set_Max_Enemies(self):
        # Max enemies by Awakening Level:
        # Level 0: 5
        # Level 1: 7
        # Level 2: 12
        # Level 3: 18
        # Level 4: 28
        # Level 5: 44
        self.max_enemies = int(BASE_MIN_ENEMIES * (1.55 ** self.awakening_level))

    def Adjust_Difficulty(self):
        
        self.spawn_enemies.Set_Awakening_Level(self.awakening_level)
        self.buff_enemies.Set_Awakening_Level(self.awakening_level)
        self.player_debuff.Set_Awakening_Level(self.awakening_level)


        if self.awakening_level in ASCENSION_TABLE:
            self.awakening_dic = ASCENSION_TABLE.get(self.awakening_level)
        

    def Trigger_Awakening(self):
        awakening_copy = self.Adjust_Awakening_Dic()

        effects = random.choices(
                    population=list(awakening_copy.keys()),
                    weights=list(awakening_copy.values()),
                    k=1
                )[0]
        
        awakening_function = self.awakening_functions.get(effects)
        self.awakening_cooldown = max(0, self.awakening_cooldown - 1)

        if not awakening_function:
            return False
        
        screen_shake = 2
        screen_shake_duration = 20
        if effects == INCREASE_ASCENSION:
            screen_shake *= 2
            screen_shake_duration *= 2
            awakening_function(min(self.max_awakening_level, self.awakening_level + 1))
            self.game.sound_handler.Play_Sound(keys.awakening_increase, 0.6)
        else:
            awakening_function()

        self.game.camera_update.Set_Screen_Shake(screen_shake_duration, screen_shake)
        return True
    
    def Adjust_Awakening_Dic(self):
        awakening_copy = self.awakening_dic.copy()

        enemy_num = self.game.enemy_handler.Get_Number_Of_Enemies()

        min_enemy = BASE_MIN_ENEMIES * self.awakening_level

        if enemy_num < min_enemy:
            awakening_copy[SPAWN_ENEMY] *= 2
        elif enemy_num > self.max_enemies:
            awakening_copy[SPAWN_ENEMY] = 0
            awakening_copy[SPAWN_ELITE] = 0
        elif enemy_num > min_enemy and enemy_num < self.max_enemies and self.awakening_level >= 4:
            awakening_copy[SPAWN_ELITE] *= 2 # Increase chance to spawn elites when there are many enemies in dungeon

        if self.awakening_cooldown:
            awakening_copy[INCREASE_ASCENSION] = 0

        return awakening_copy
