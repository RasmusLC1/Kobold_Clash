from scripts.entities.moving_entities.enemies.behavior.abilities.ability import Ability
from scripts.engine.keys.keys import keys
import pygame
import math

class Dash(Ability):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name)
        self.target_pos = None
        self.dash_velocity = pygame.math.Vector2(0, 0)
        self.stored_distance = 9999
        self.pushed_entities = set()
        self.Set_Cooldown_Time()

    def Activate(self):
        
        self.target_pos = list(self.game.player.pos)
        
        direction = pygame.math.Vector2(
            self.target_pos[0] - self.entity.pos[0],
            self.target_pos[1] - self.entity.pos[1]
        )
        
        if direction.length() > 0:
            self.dash_velocity = direction.normalize() * 10 # The 'Force' of the dash
        
        self.entity.Set_Active_Ability(keys.dash)
        return True

    def Update(self, delta_time):
        # Check pushed entities first to prevent duplicate damage as
        # update_charge can reset pushed_entities
        self.Check_Pushed_Entities() 
        self.entity.Increase_Max_Speed(10)
        self.Update_Charge(delta_time)

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
            entity.Damage_Taken(self.entity.strength, (keys.blunt, 0))

        

    def _Reset_Attack(self):
        self.target_pos = None
        self.entity.Remove_Active_Ability() 
        self.entity.Reset_Behavior()
        self.stored_distance = 9999
        self.entity.Reset_Max_Speed()
        self.pushed_entities.clear()
        
        self._Set_Cooldown()
        
        
    # Returns true if player is between 150 and 250 after
    def Check_If_Trigger(self):
        distance_to_player = self._Check_Distance(self.game.player.pos)
        return  distance_to_player > 80 and distance_to_player < 250

    def _Check_Distance(self, target):
        distance = math.sqrt((self.entity.pos[0] - target[0]) ** 2 + (self.entity.pos[1] - target[1]) ** 2)
        return distance
            
