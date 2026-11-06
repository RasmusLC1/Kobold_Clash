from scripts.entities.decoration.shared.shrine.shrine import Cycling_Shrine
from scripts.entities.decoration.shared.shrine.shrine_reward_pools import BAD_REWARDS, MID_REWARDS, GOOD_REWARDS
from scripts.engine.keys.keys import keys
from scripts.entities.decoration.shared.shrine.shrine_registry import Register_Shrine
from scripts.entities.decoration.ancient_tomb.ancient_tomb_registry import Register_Decoration
import random
from enum import Enum


class RewardType(Enum):
    BAD = 1
    MID = 2
    GOOD = 3


Register_Shrine(keys.sacrifice_shrine)
@Register_Decoration(keys.sacrifice_shrine)
class Sacrifice_Shrine(Cycling_Shrine):
    def __init__(self, game, pos) -> None:
        super().__init__(game, keys.sacrifice_shrine, pos, (64, 64),
                          particle_type=keys.soul_particle,
                          particle_chance=2, max_animation=3, animation_cooldown_max=0.5)
        self.description = "Sacrifice loot\nfor reward"
        self.Add_Light()

    def Add_Light(self):
        self.light_source = self.game.light_handler.Add_Light(self.pos, 10, self.tile)
        self.light_level = self.game.light_handler.Initialise_Light_Level(self.tile)

    def Spawn_Reward(self, item):
        value = self.Calculate_Reward(item)

        if value == RewardType.BAD:
            self.Grant_Reward(BAD_REWARDS, keys.bad_reward)
        elif value == RewardType.MID:
            self.Grant_Reward(MID_REWARDS, keys.mid_reward)
        else:
            self.Grant_Reward(GOOD_REWARDS, keys.good_reward, permanent=True)

        self.game.item_handler.Remove_Item(item, True)
        self.game.clatter.Generate_Clatter(self.pos, 200)
        return True

    def Grant_Reward(self, pool, sound, permanent=False):
        self.game.sound_handler.Play_Sound(sound, 0.4)
        reward, amount = random.choice(list(pool.items()))
        self.game.player.Set_Effect(reward, amount, permanent)

    def Calculate_Reward(self, item):
        value = item.amount * item.value

        if value >= 100:
            return RewardType.GOOD
        elif value >= 50:
            norm = (value - 50) / 50
            good_chance = 0.5 + 0.5 * norm
            mid_chance = 1.0 - good_chance
            return RewardType.MID if random.random() < mid_chance else RewardType.GOOD
        else:
            norm = value / 50
            bad_chance = 0.8 - 0.8 * norm
            mid_chance = 0.2 - 0.1 * norm
            good_chance = 0.9 * norm
            total = bad_chance + mid_chance + good_chance
            bad_chance /= total
            mid_chance /= total

            r = random.random()
            if r < bad_chance:
                return RewardType.BAD
            elif r < bad_chance + mid_chance:
                return RewardType.MID
            return RewardType.GOOD