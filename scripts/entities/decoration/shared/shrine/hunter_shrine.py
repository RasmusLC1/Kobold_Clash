from scripts.entities.decoration.decoration import Decoration
import random
from scripts.engine.keys.keys import keys
import math

activation_radius = 200

class Hunter_Shrine(Decoration):
    def __init__(self, game, pos) -> None:
        super().__init__(game, keys.hunter_shrine, pos, (64, 64))
        self.description = "Return the\ntreasure for\nreward"
        self.max_animation = 2
        self.treasures = []

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


    
    def Open(self, generate_clatter=False):
        if self.empty:
            return False
        self.empty = True
        self.Set_Animation(1)
        self.Set_Sprite()
        self.Spawn_Treasure()
        self.game.player.Set_Last_Shrine(self)
        return True

    
    def Spawn_Treasure(self):
        self.game.sound_handler.Play_Sound(keys.hunter_shrine_activation, 0.4)
        fail = 0
        for i in range(3):
            tile = self.game.tilemap.Get_Random_Tile_With_Path_To_Player()
            if not tile:
                print("TILE NOT FOUND, HUNTER SHRINE")
                fail += 1
                if fail > 10:
                    return
                continue
            treasure = self.game.item_handler.loot_handler.Spawn_Loot_Type(keys.valuable, tile.scaled_pos, None, keys.hunter_treasure)
            if not treasure:
                print("Treasure not spawned, HUNTER SHRINE")
                return
            
            self.treasures.append(treasure)


    def Spawn_Reward(self, item):
        if not self.animation == 1:
            return False
        if item.type != keys.hunter_treasure:
            return False
        
        self.game.player.Set_Last_Shrine(self)

        self.Set_Animation(2)
        self.game.item_handler.Remove_Item(item, True)
        reward, amount = random.choice(list(self.rewards.items()))
        
        self.game.player.Set_Effect(reward, amount, True)
        self.game.sound_handler.Play_Sound(keys.collapse, 0.4)
        self.game.clatter.Generate_Clatter(self.pos, 1000) # Generate clatter to alert nearby enemies

        for treasure in list(self.treasures):
            self.treasures.remove(treasure)
            self.game.item_handler.Remove_Item(treasure, True)

        return True