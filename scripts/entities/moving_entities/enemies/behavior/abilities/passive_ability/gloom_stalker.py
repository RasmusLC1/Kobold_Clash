from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.passive_ability import Passive_Ability
from scripts.engine.keys.keys import keys

class Gloom_Stalker(Passive_Ability):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name)
        # Dwellers get increased strength in dark
        self.light_level_holder = 999


    def Update(self, delta_time):
        self.Darkness_Buff()
        return super().Update(delta_time)


    def Darkness_Buff(self):
        threshold = 150
        entity_light_level = self.entity.light_level
        
        is_dark = entity_light_level < threshold
        was_dark = self.light_level_holder < threshold
        
        self.light_level_holder = entity_light_level

        if is_dark == was_dark:
            return
        
        # Calculate relative to whatever the entity's strength currently is
        if is_dark:
            # If entering dark, double its current baseline stats
            self.entity.Set_Strength(self.entity.strength * 2)
            self.entity.Set_Max_Speed(self.entity.max_speed_holder * 2)
        else:
            # If entering light, reduce them back down safely
            self.entity.Set_Strength(int(self.entity.strength / 2))
            self.entity.Set_Max_Speed(int(self.entity.max_speed_holder / 2))

        self.entity.Set_Description()