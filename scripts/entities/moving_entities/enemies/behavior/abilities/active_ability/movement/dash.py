from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.active_ability import Active_Ability
from scripts.entities.moving_entities.enemies.behavior.abilities.registry import register_ability
from scripts.engine.keys.keys import keys
import pygame
import math


@register_ability(keys.dash) # add ability to registry

class Dash(Active_Ability):
    def __init__(self, game, entity, name, min_distance = 70, max_distance = 250, speed_factor = 10):
        super().__init__(game, entity, name, can_attack_while_triggered=True)
        self.target_pos = None
        self.dash_velocity = pygame.math.Vector2(0, 0)
        self.stored_distance = 9999
        self.min_distance = min_distance
        self.max_distance = max_distance
        self.speed_factor = speed_factor 
        self.pushed_entities = set()
        self.Set_Cooldown_Time()

    def Save_Data(self):
        super().Save_Data()
        self.entity.saved_data['dash_velocity'] = self.dash_velocity
        self.entity.saved_data['target_pos'] = self.target_pos

    def Load_Data(self, data):
        self.dash_velocity = data['dash_velocity']
        self.target_pos = data['target_pos']
        super().Load_Data(data)


    def Activate(self):
        self.entity.Set_Active_Ability(self.name)
        self.Calculate_Direction()
        return True

    def Calculate_Direction(self):
        self.target_pos = list(self.game.player.pos)
        
        direction = pygame.math.Vector2(
            self.target_pos[0] - self.entity.pos[0],
            self.target_pos[1] - self.entity.pos[1]
        )
        
        if direction.length() > 0:
            self.dash_velocity = direction.normalize() * self.speed_factor # The 'Force' of the dash
        

    def Update(self, delta_time):
        # Check pushed entities first to prevent duplicate damage as
        # update_charge can reset pushed_entities
        self.Check_Pushed_Entities() 
        self.entity.Increase_Max_Speed(self.speed_factor)
        self.Update_Charge(delta_time)
        return 

    def Set_Cooldown_Time(self):
        self.COOLDOWN_TIME = 10 - self.entity.agility # Enemy agility dictates the cooldown time
    
    def Update_Charge(self, delta_time):
        if not self.target_pos:
            return
         
        self.entity.velocity[0] = self.dash_velocity.x * delta_time * self.entity.max_speed
        self.entity.velocity[1] = self.dash_velocity.y * delta_time * self.entity.max_speed
        
        # Check for arrival
        distance = self._Check_Distance(self.target_pos)
        if  distance > self.stored_distance:
            self._Reset_Attack()

        self.stored_distance = distance

    
    def Check_Pushed_Entities(self):
        current_frame_pushed = self.entity.Get_Pushed_Entities()
        # Convert to sets and find the difference
        new_hits = set(current_frame_pushed) - set(self.pushed_entities)

        for entity in new_hits:
            self.pushed_entities.add(entity)
            self.Set_Damage(entity)
            
    def Set_Damage(self, entity):
        damage = (self.entity.strength * abs(self.entity.velocity[0] + self.entity.velocity[1]) // 100) // 4 # Average velicty and strength
        entity.Damage_Taken(damage, (keys.blunt, 0), self.entity.attack_direction)
        

    def _Reset_Attack(self):
        self.target_pos = None
        self.entity.Remove_Active_Ability() 
        self.entity.Reset_Behavior()
        self.stored_distance = 9999
        self.entity.Reset_Max_Speed()
        self.pushed_entities.clear()
        
        self._Set_Cooldown()
        
        
    # Returns true if player is between min and max distance
    def Check_If_Trigger(self):
        distance_to_target = self.entity.distance_to_player
        return  distance_to_target > self.min_distance and distance_to_target < self.max_distance

    def _Check_Distance(self, target):
        distance = math.sqrt((self.entity.pos[0] - target[0]) ** 2 + (self.entity.pos[1] - target[1]) ** 2)
        return distance
            
