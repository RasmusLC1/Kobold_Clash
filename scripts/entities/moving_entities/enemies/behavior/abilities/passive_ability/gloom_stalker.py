from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.passive_ability import Passive_Ability
from scripts.engine.keys.keys import keys

class Gloom_Stalker(Passive_Ability):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name)
        # Dwellers get increased strength in dark
        self.light_level_holder = 999
        self.light_strength = self.entity.strength
        self.dark_strength = self.entity.strength * 2

        self.light_speed = self.entity.max_speed_holder
        self.dark_speed = self.entity.max_speed_holder * 2


    def Update(self, delta_time):
        self.Darkness_Buff()

    def Darkness_Buff(self):
        threshold = 150
        entity_light_level = self.entity.light_level
        
        is_dark = entity_light_level < threshold
        was_dark = self.light_level_holder < threshold
        
        self.light_level_holder = entity_light_level

        # Only run if the state actually changed
        if is_dark == was_dark:
            return
        
        if is_dark:
            self.entity.Set_Strength(self.dark_strength)
            self.entity.Set_Max_Speed(self.dark_speed)
        else:
            self.entity.Set_Strength(self.light_strength)
            self.entity.Set_Max_Speed(self.light_speed)

        self.entity.Set_Description()