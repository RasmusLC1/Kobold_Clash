from scripts.entities.decoration.shared.shrine.shrine import Cycling_Shrine
from scripts.engine.keys.keys import keys
from scripts.entities.decoration.shared.shared_registry import Register_Decoration
from scripts.entities.decoration.shared.shrine.shrine_registry import Register_Shrine
import random

Register_Shrine(keys.soul_well)
@Register_Decoration(keys.soul_well)
class Soul_Well(Cycling_Shrine):
    def __init__(self, game, pos) -> None:
        super().__init__(game, keys.soul_well, pos, (64, 64),
                           particle_type=keys.soul_particle,
                          particle_chance=4, max_animation=3, animation_cooldown_max=0.8)
        self.description = "sacrifice gold\nfor souls"

    def Spawn_Reward(self, item):
        self.Activate_Shrine()
        self.game.player.Increase_Souls(item.amount * item.value * 2)
        self.game.item_handler.Remove_Item(item, True)
        self.game.particle_handler.Activate_Particles(random.randint(8, 12), keys.soul_particle, self.rect().center, time=random.uniform(1.5, 2))
        self.Generate_Sound(keys.soul_well_sound, 0.6, 1000)
        return True