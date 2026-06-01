import random
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.passive_ability import Passive_Ability
from scripts.engine.keys.keys import keys

class Bone_Seeker(Passive_Ability):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name)
        self.bones_search_cooldown = 0
        self.target_bones_collision_cooldown = 0
        self.target_bones = None
        
        # Consistent scale for cooldowns using delta_time (in seconds)
        self.COLLISION_CHECK_DELAY = 0.83  # Roughly equivalent to 50 frames at 60FPS

    def Save_Data(self):
        super().Save_Data()
        self.entity.saved_data['bones_search_cooldown'] = self.bones_search_cooldown
        self.entity.saved_data['target_bones_collision_cooldown'] = self.target_bones_collision_cooldown

    def Load_Data(self, data):
        self.bones_search_cooldown = data.get('bones_search_cooldown', 0)
        self.target_bones_collision_cooldown = data.get('target_bones_collision_cooldown', 0)
        return super().Load_Data(data)

    def Update(self, delta_time):
        self.Update_Bones_Timers(delta_time)
        self.Search_For_Bones()
        self.Bones_Collision_Check()

    def Update_Bones_Timers(self, delta_time):
        if self.bones_search_cooldown > 0:
            self.bones_search_cooldown = max(0, self.bones_search_cooldown - delta_time)
        if self.target_bones_collision_cooldown > 0:
            self.target_bones_collision_cooldown = max(0, self.target_bones_collision_cooldown - delta_time)

    def Search_For_Bones(self):
        if self.bones_search_cooldown > 0:
            return
            
        self.bones_search_cooldown = random.randint(2, 4)
        
        # Optimization: If we already have a target, don't spam the pathfinding queue with a new request
        if self.target_bones:
            return

        nearby_bones = self.game.tilemap.Search_Nearby_Tiles_For_Type(5, self.entity.pos, keys.bones, self.entity.ID)
        
        if not nearby_bones:
            return
            
        self.entity.locked_on_target = False
        self.game.enemy_handler.Add_To_Pathfinding_Queue(self.entity, nearby_bones[0].pos)
        self.entity.intent_manager.Set_Movement_Strategy(keys.medium_range)
        self.target_bones = nearby_bones[0]

    def Bones_Collision_Check(self):
        if not self.target_bones:
            return
            
        # Delta-time based throttle for collision processing performance
        if self.target_bones_collision_cooldown > 0:
            return
        
        self.target_bones_collision_cooldown = self.COLLISION_CHECK_DELAY
        
        # Edge Case Safety: Check if the bone target was cleaned up or destroyed by something else
        if hasattr(self.target_bones, 'is_destroyed') and self.target_bones.is_destroyed:
            self.target_bones = None
            return

        # Verify physical contact before triggering the effect
        if self.entity.rect().colliderect(self.target_bones.rect()):
            self.Consume_Bones()

    def Consume_Bones(self):
        """Hook method: To be overridden by child classes."""
        pass