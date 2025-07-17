from scripts.entities.decoration.decoration import Decoration
import random
from scripts.engine.keys.keys import keys
from enum import Enum

class RewardType(Enum):
    BAD = 1
    MID = 2
    GOOD = 3


class Sacrifice_Shrine(Decoration):
    def __init__(self, game, pos) -> None:
        super().__init__(game, keys.sacrifice_shrine, pos, (64, 64))
        self.description = "Sacrifice loot\nfor reward"
        self.max_animation = 3
        self.treasures = []
        self.animation_cooldown = 0
        self.distance_to_player = 0
        self.max_animation = 3
        self.Add_Light()


        

    def Update(self):
        self.Update_Animation()
        return super().Update()
    
    def Add_Light(self):
        self.light_source = self.game.light_handler.Add_Light(self.pos, 10, self.tile)
        self.light_level = self.game.light_handler.Initialise_Light_Level(self.tile)

    # TODO: Add sprite for shrine with animation
    def Update_Animation(self):
        if not self.animation_cooldown_Handler():
            return
        
        if self.animation >= self.max_animation:
            self.Set_Animation(0)
        else:
            self.Set_Animation(self.animation + 1)
        spawn_particles = random.randint(0, 2)
        if spawn_particles == 0:
            self.game.particle_handler.Activate_Particles(random.randint(2, 4), keys.soul_particle, self.rect().center, time = random.uniform(1.5, 2))

    def animation_cooldown_Handler(self):
        if self.animation_cooldown <= 0:
            self.animation_cooldown = random.randint(30, 45)
            return True
        
        self.animation_cooldown -= 1
        return False


    def Spawn_Reward(self, item):
        print(item.type)
        value = self.Calculate_Reward(item)

        if value == RewardType.BAD:
            self.Get_Bad_Reward()
        elif value == RewardType.MID:
            self.Get_Mid_Reward()
        elif value == RewardType.GOOD:
            self.Get_Good_Reward()

        self.game.item_handler.Remove_Item(item, True)
        self.game.clatter.Generate_Clatter(self.pos, 200) # Generate clatter to alert nearby enemies
        return True
    
    def Calculate_Reward(self, item):
        value = item.amount * item.value

        # At 100 gold or more, guaranteed GOOD reward
        if value >= 100:
            return RewardType.GOOD
        
        # At 50 gold or more, no BAD rewards
        elif value >= 50:
            # Linearly increase chance of GOOD reward from 50 to 100
            norm = (value - 50) / 50  # 0 at 50, 1 at 100
            good_chance = 0.5 + 0.5 * norm  # From 0.5 to 1.0
            mid_chance = 1.0 - good_chance  # From 0.5 to 0.0
            r = random.random()
            if r < mid_chance:
                return RewardType.MID
            else:
                return RewardType.GOOD
        
        # Below 50 gold, bad possible
        else:
            norm = value / 50  # 0 to 1
            bad_chance = 0.8 - 0.8 * norm  # From 0.8 to 0
            mid_chance = 0.2 - 0.1 * norm  # From 0.2 to 0.1
            good_chance = 0.0 + 0.9 * norm  # From 0 to 0.9

            total = bad_chance + mid_chance + good_chance
            bad_chance /= total
            mid_chance /= total
            good_chance /= total

            r = random.random()
            if r < bad_chance:
                return RewardType.BAD
            elif r < bad_chance + mid_chance:
                return RewardType.MID
            else:
                return RewardType.GOOD

    
    # Bad rewards are temporary bad effects
    def Get_Bad_Reward(self):
        self.rewards = {
            keys.poison : 4,
            keys.fire : 4,
            keys.frozen : 4,
            keys.electric : 4,
            keys.slow : 5,
            keys.snare : 5,
            keys.poison : 4,
            keys.weakness : 5,
        }

        self.game.sound_handler.Play_Sound('bad_reward', 0.4)

        reward, amount = random.choice(list(self.rewards.items()))
        self.game.player.Set_Effect(reward, amount)
        return

    # Mid rewards are not permanent
    def Get_Mid_Reward(self):
        self.rewards = {
            keys.healing: 20,
            keys.vampiric: 5,
            keys.regen: 3,
            keys.thorns: 5,
            keys.speed: 4,
            keys.arcane_hunger: 5,
            keys.arcane_conduit: 4,
            keys.resistance: 4,
        }

        self.game.sound_handler.Play_Sound('mid_reward', 0.4)
        
        reward, amount = random.choice(list(self.rewards.items()))
        self.game.player.Set_Effect(reward, amount)
        return
    
    # Good rewards are permanent but lower
    def Get_Good_Reward(self):
        self.rewards = {
            keys.vampiric: 3,
            keys.regen: 1,
            keys.thorns: 3,
            keys.anchor: 3,
            keys.speed: 2,
            keys.power: 1,
            keys.arcane_hunger: 3,
            keys.arcane_conduit: 1,
            keys.resistance: 1,
            keys.frozen_resistance: 3,
            keys.fire_resistance: 3,
            keys.electric_resistance: 3,
            keys.poison_resistance: 3,
        }

        self.game.sound_handler.Play_Sound('good_reward', 0.4)
        
        reward, amount = random.choice(list(self.rewards.items()))
        self.game.player.Set_Effect(reward, amount, True)
        return
