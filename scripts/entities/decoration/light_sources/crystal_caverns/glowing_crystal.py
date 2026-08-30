from scripts.entities.decoration.light_sources.light_sources.light_source import Light_Source
import random
from scripts.engine.keys.keys import keys
from scripts.entities.decoration.light_sources.crystal_caverns.light_sources_registry import Register_Light_Source
from scripts.entities.decoration.shared.loot_container.loot_component import LootComponent


@Register_Light_Source(keys.glowing_crystal, 0.5)
class Glowing_Crystal(Light_Source):
    def __init__(self, game, pos) -> None:
        version = random.randint(1, 5)
        super().__init__(game, pos, keys.glowing_crystal, version,
                         light_strength=8,
                         max_animation=5, animation_cooldown_max=2.0,
                         destructable=True, health=40, destruction_sound='vase_shatter')

        self.updated_light_strength = self.light_strength
        # Configurable per-entity without modifying a global dictionary
        self.loot_component = LootComponent(
            game=game, 
            entity_type=keys.glowing_crystal, 
            min_rarity=1, 
            max_rarity=15, 
            loot_weights={keys.gem: 100}
        )
    

    def Update(self, delta_time):
        self.Update_Light_Level()
        
        return super().Update(delta_time)

    def Open(self, generate_clatter=False):
        self.updated_light_strength = self.light_strength + 4
        self.light_source.Update_Light_Level(self.updated_light_strength)

    def Destroyed(self):
        if not super().Destroyed():
            return False
            
        spawn_pos = (
            self.pos[0] + random.randint(-10, 10) / 10,
            self.pos[1] + random.randint(-10, 10) / 10
        )
        self.loot_component.Drop_Loot(spawn_pos)
        return True
        
    def Update_Animation(self, delta_time, movement=(0, 0)):
        super().Update_Animation(delta_time, movement)
        self.Handle_Updated_Lightlevel()
    
    def Handle_Updated_Lightlevel(self):
        if self.updated_light_strength <= self.light_strength:
            return
        self.light_source.Update_Light_Level(self.updated_light_strength)
        self.updated_light_strength -= 1

