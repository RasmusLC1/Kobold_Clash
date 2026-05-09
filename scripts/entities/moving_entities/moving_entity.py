import math
import pygame
from scripts.entities.moving_entities.effects.effects_handler import Status_Effect_Handler
from scripts.entities.moving_entities.animation.animation_handler import Animation_Handler
from scripts.entities.entities import PhysicsEntity
from scripts.engine.keys.keys import keys

# Cooldown in seconds
DAMAGE_COOLDOWN_MAX = 0.2
TRAP_COOLDOWN_MAX = 0.2
ENEMY_COOLDOWN_MAX = 0.4


class Moving_Entity(PhysicsEntity):

    _animation_handler = Animation_Handler
    _effect_handler = Status_Effect_Handler


    def __init__(self, game, type, category, pos, size, health, strength, max_speed, agility, intelligence, stamina, sub_category):
        super().__init__(game, type, category, pos, size, sub_category)
        self.velocity = [0, 0] # Velocity of the player
        
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False} # Check for wall collision in each direction


        self.direction = (0,0)
        self.direction_x = 0
        self.direction_y = 0
        self.direction_x_holder = 0
        self.direction_y_holder = 0
        self.attack_direction = (0,0)
        self.target = (0,0)
        self.active_ability = None
        self.pushed_entities = []
        
        self.damage_cooldown = 0
        
        self.nearby_traps = []
        self.nearby_traps_cooldown = 0
        self.nearby_enemies = []
        self.nearby_enemies_cooldown = 0
        
        self.frame_movement = (0.0)
        self.last_frame_movement = (0.0)

        # Attributes, placeholder should be assigned on creation
        self.strength = strength # Damage and moving items and other entities
        self.strength_holder = strength # Damage and moving items and other entities
        self.agility = agility # max_speed, acceleration, weapon recharge speed, movement speed and lockpicking
        self.intelligence = intelligence # spells and trap detection
        self.stamina = stamina # movement ability recharge and weapon cooldown
        self.health = health
        self.healing_enabled = True
        self.max_health = self.health
        
        # Movement variables
        self.friction = 0.0001 # Friction, set to the renderscale
        self.friction_holder = self.friction # Holder for friction to reset it
        self.acceleration = agility * 1000
        self.acceleration_holder = self.acceleration # accelarition holder to reset it
        self.max_speed = max_speed  * 100  # Max speed of the entity
        self.max_speed_holder = self.max_speed # Max speed holder to reset it

        # Handle Blocking
        self.block_direction = (0,0)

        # Status Effects
        self.effects = self._effect_handler(self)
        self.animation_handler = self._animation_handler(self)

        self.active_weapon_cooldown = 0
        self.Set_Sprite()


    def Save_Data(self):
        super().Save_Data()
        self.saved_data[keys.type] = self.type
        self.saved_data['health'] = self.health
        self.saved_data['max_health'] = self.max_health
        self.saved_data['strength'] = self.strength
        self.saved_data['max_speed'] = self.max_speed
        self.saved_data['agility'] = self.agility
        self.saved_data['intelligence'] = self.intelligence
        self.saved_data['stamina'] = self.stamina
        self.saved_data['target'] = self.target
        self.saved_data['animation'] = self.animation_handler.animation
        self.saved_data['effects'] = self.effects.Save_Data()


    def Load_Data(self, data):
        super().Load_Data(data)
        self.type = data[keys.type]
        self.health = data['health']
        self.max_health = data['max_health']
        self.strength = data['strength']
        self.max_speed = data['max_speed']
        self.agility = data['agility']
        self.intelligence = data['intelligence']
        self.stamina = data['stamina']
        self.target = data['target']
        self.animation_handler.animation = data['animation']
        self.effects.Load_Data(data['effects'])


    # Update the entity 
    def Update(self, tilemap, delta_time, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        self.Update_Movement(movement, delta_time)
        self.animation_handler.Update_Animation(movement, delta_time)
        self.Update_Status_Effects(delta_time)


        # self.Update_Traps(delta_time)
        self.Nearby_Enemies(2, delta_time)
        self.Update_Damage_Cooldown(delta_time)

        self.Movement(tilemap)
        self.Update_Tile(delta_time)
    

    def Update_Movement(self, movement, delta_time):
        # Apply acceleration (units/sec^2 → velocity in units/sec)
        self.velocity[0] += movement[0] * self.acceleration * delta_time
        self.velocity[1] += movement[1] * self.acceleration * delta_time

        # Clamp velocity (velocity is units/sec, so max_speed must also be units/sec)
        self.velocity[0] = max(-self.max_speed, min(self.velocity[0], self.max_speed))
        self.velocity[1] = max(-self.max_speed, min(self.velocity[1], self.max_speed))

        # Apply friction (frame-rate independent)
        if abs(self.velocity[0]) > 0.1:
            self.velocity[0] *= self.friction ** delta_time
        else:
            self.velocity[0] = 0
        if abs(self.velocity[1]) > 0.1:
            self.velocity[1] *= self.friction ** delta_time
        else:
            self.velocity[1] = 0

        self.direction_x = movement[0]
        self.direction_y = movement[1]
        # Apply velocity to movement (distance = velocity * time)
        self.Set_Frame_movement((
            (self.velocity[0] * delta_time) / self.game.render_scale,
            (self.velocity[1] * delta_time) / self.game.render_scale
        ))




    # Movement handling
    def Movement(self, tilemap):
        self.Entity_Collision_Detection()
        self.Apply_Repulsion(tilemap)
        
        self.Tile_Map_Collision_Detection(tilemap)

        self.last_frame_movement = self.frame_movement
    


    def Set_Active(self, duration):
        # use hasattr to check if self.effects exists
        if hasattr(self, "effects"):
            if self.active_ability == keys.invisibility:
                return
        return super().Set_Active(duration)
    

    def Set_Description(self):
        pass
    
    def Attack_Direction_Handler(self):
        self.Set_Attack_Direction()
        self.animation_handler.Attack_Direction_Handler()

    def Tile_Map_Collision_Detection(self, tilemap):
        self.pos[0] += self.frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if self.frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if self.frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x
        
        self.pos[1] += self.frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if self.frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if self.frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y


    def Entity_Collision_Detection(self):
        self.pushed_entities.clear()
        future_pos = (self.pos[0] + self.frame_movement[0], self.pos[1] + self.frame_movement[1])
        for enemy in self.nearby_enemies:
            if enemy != self and enemy.rect().colliderect(self.rect_future(future_pos)):
                self.pushed_entities.append(enemy)
                
        return future_pos

    def Apply_Repulsion(self, tilemap) -> None:
        if not self.pushed_entities:
            return
        
        for entity in self.pushed_entities:
            # Check if entity is stronger than the other, if no then simply return as it cannot push it
            if self.strength < entity.strength:
                return

            # Calculate repulsion strength based on strength
            repulsion_strength = 1 + (self.strength - entity.strength) / 10

            direction_vector = pygame.math.Vector2(self.pos) - pygame.math.Vector2(entity.pos)
            if direction_vector.length() < 0:
                return
            if direction_vector:
                direction_vector.normalize_ip()

            direction_vector *= repulsion_strength

            # Push the other entity backwards
            entity.Push(direction_vector, tilemap)
    

    def rect_future(self, future_pos):
        return pygame.Rect(future_pos[0], future_pos[1], self.size[0], self.size[1])     
    

    # Update only the nearby traps
    def Update_Traps(self, delta_time):
        if not self.Find_Nearby_Traps(3, delta_time):
            return

        for trap in self.nearby_traps:
            trap.Add_Entity_To_Trap(self)

    def Find_Nearby_Traps(self, distance, delta_time) -> bool:
        if self.nearby_traps_cooldown > 0:
            self.nearby_traps_cooldown -= delta_time
            return False
        self.nearby_traps.clear()
        self.nearby_traps = self.game.trap_handler.Find_Nearby_Traps(self, distance)
        self.nearby_traps_cooldown = TRAP_COOLDOWN_MAX
        return True
    

    def Nearby_Enemies(self, max_distance, delta_time) -> None:
        if self.nearby_enemies_cooldown > 0:
            self.nearby_enemies_cooldown -= delta_time
            return
        
        self.nearby_enemies.clear()
        self.nearby_enemies = self.game.enemy_handler.Find_Nearby_Enemies(self, max_distance)
        self.nearby_enemies_cooldown = ENEMY_COOLDOWN_MAX
        return
    

    def Update_Damage_Cooldown(self, delta_time):
        if self.damage_cooldown > 0:
            self.damage_cooldown -= delta_time

            if self.damage_cooldown <= 0:
                self.damage_cooldown = 0
    
    def Set_Damage_Cooldown(self):
        self.damage_cooldown = DAMAGE_COOLDOWN_MAX
        
            
    # Damage = Total damage, effect = (effect, effect strength) 
    def Damage_Taken(self, damage, effect = (keys.slash, 0), direction = (0, 0)):
        # Prevent aditional damage if entity is already dead
        if self.health <= 0:
            return False
        
        if self.active_ability == keys.invulnerable: # Cannot take damage if invulnerable
            return False
        
        if self.Check_Blocking_Direction(direction) or self.damage_cooldown > 0:
            return False
        
        self.game.text_box_handler.Spawn_Damage_Text(self.pos.copy(), effect[0], str(damage))

        self.Set_Health(self.health - damage)

        # Update the entitty description
        self.Set_Description()
        
        # Check if any active effects affect damage
        self.effects.Damage_Taken(damage)
        if direction:
            self.Push(direction, self.game.tilemap, damage)
        
        if effect[1] > 0 and not keys.vampiric in effect[0]:
            effect_strength = max(effect[1] // 10, 1)
            self.effects.Set_Effect(effect[0], effect_strength)

        self.Check_If_Dead()
        return True
    

    
    def Check_If_Dead(self):
        if self.health > 0: # Entity alive
            return False
        if self.tile:
            self.tile.Clear_Entity(self.ID)
        self.game.enemy_handler.Delete_Enemy(self)
        self.effects.Reset_Effects()
        self.Update_Status_Effects(self.game.delta_time)
        self.render = False
        return True

    def Check_Blocking_Direction(self, direction) -> bool:
        # Check if entity is blocking
        if self.block_direction == (0, 0):
            return
        
        # Convert directions to pygame Vector2 for easier manipulation
        attack_vector = pygame.math.Vector2(self.attack_direction)
        block_vector = pygame.math.Vector2(direction)

        # Check for zero-length vectors to avoid division by zero
        if attack_vector.length() == 0 or block_vector.length() == 0:
            return False

        # Normalize the vectors to unit vectors
        attack_vector.normalize_ip()
        block_vector.normalize_ip()

        # Calculate the dot product and determine the angle
        dot_product = attack_vector.dot(block_vector)
        dot_product = max(-1.0, min(1.0, dot_product))  # Clamp value to avoid errors in acos due to floating point precision
        angle = math.acos(dot_product)
        angle_degrees = math.degrees(angle)

        # Determine if the block is successful based on the angle
        if angle_degrees >= 130:
            return True
        
        return False



    def Set_Attack_Direction(self, attack_direction=None):
        attack_direction = self.Check_Attack_Direction(attack_direction)

        if not attack_direction:
            self.Set_Target(self.game.player.pos) # if no attack direction set it to player default
            self.Set_Attack_Direction(self.target)
            print("ATTACK DIRECTION NOT FOUND", self.target, attack_direction, self.pos, self.type)
            return

        self.attack_direction = pygame.math.Vector2(
            attack_direction[0] - self.pos[0],
            attack_direction[1] - self.pos[1]
        )
        if self.attack_direction.length_squared() == 0:
            return
        self.attack_direction.normalize_ip()

    def Check_Attack_Direction(self, attack_direction):
        if not attack_direction:
            if not self.target:
                return
            attack_direction = self.target
        return attack_direction

    def Reset_Attack_Direction(self):
        self.attack_direction = (0, 0)


    def Set_Frame_movement(self, movement):
        self.frame_movement = movement

    def Set_Target(self, pos):
        self.target = pos

    # Returns True if there is no active ability, can only be one active at a time
    def Set_Active_Ability(self, ability):
        if self.active_ability:
            return self.active_ability == ability # Returns true if the active ability is the same as the one being triggered                
        self.active_ability = ability
        return True
    
    def Remove_Active_Ability(self):
        self.active_ability = None

    def Set_Health(self, amount):
        self.health = amount

    def Reduce_Movement(self, factor):
        self.max_speed = self.max_speed // factor

    def Reset_Max_Speed(self):
        self.max_speed = self.max_speed_holder
        
    def Push(self, direction, tilemap, push_strength=-1):
        if direction is None:
            return  # or pick a default direction like (0, 0)
        self.Set_Frame_movement((direction[0] * push_strength, direction[1] * push_strength))
        self.effects.Push(direction)
        self.Tile_Map_Collision_Detection(tilemap)

    def Set_Attack_Triggered(self):
        pass



    # Ice mechanic, lower friction and acceleration to simulate ice
    def On_Ice(self, effect):
        self.friction = max(0.1, self.friction * effect)
        self.acceleration = max(0.3, self.acceleration / effect / 10)

    # Handle status effects
    def Update_Status_Effects(self, delta_time):
        self.friction = self.friction_holder
        self.max_speed = self.max_speed_holder
        self.Set_Strength(self.strength_holder)
        self.effects.Update_Status_Effects(delta_time)

    def Set_Strength(self, strength):
        self.strength = strength
    
    def Set_Effect(self, effect, duration, permanent = False):
        return self.effects.Set_Effect(effect, duration, permanent)
    
    def Remove_Effect(self, effect, permanent = 0):
        return self.effects.Remove_Effect(effect, permanent)

    def Set_Block_Direction(self, direction):
        self.block_direction = direction

    def Set_Healing_Enabled(self, state):
        self.healing_enabled = state

    def Update_Health(self, value):
        self.health = min(self.max_health, self.health + value)
        self.Set_Description()

    def Increase_Max_Health(self, value):
        self.max_health += value

    # Used for animations
    def Set_Action(self, movement = None):
        pass

    def Get_Pushed_Entities(self):
        return self.pushed_entities



    # Render entity
    def Render(self, surf, offset=(0, 0)):
        # Check if entity is in view distance first, if no there's no point computing the rest
        if not self.active:
            return False
        # Don't Render the enemy if their light level is very low
        # Simulates low visibility
        if not self.Update_Light_Level():
            return False
        
        if not self.animation_handler.entity_image:
            return False

        self.Update_Dark_Surface()


        # Render status effects
        #Fire
        self.effects.Render_Effects(surf, offset)

        self.Render_Damage(surf, offset)

        surf.blit(pygame.transform.flip(self.rendered_image, self.animation_handler.flip[0], False), 
                (self.pos[0] - offset[0], self.pos[1] - offset[1]))
        return True
    
    def Render_Damage(self, surf, offset):
        self.Lightup(self.rendered_image)


    def Lightup(self, entity_image):
        if self.damage_cooldown < DAMAGE_COOLDOWN_MAX / 10:
            return
        return super().Lightup(entity_image)


    # Seperate Update Dark surface since the animations are handled by animation handler
    def Update_Dark_Surface(self):
        if not self.render_needs_update:
            return
        if not self.animation_handler.entity_image:
            self.animation_handler.Set_Entity_Image()
            print("SET dark surface for entity: ", self.type, vars(self))
            return
        self.rendered_image = self.animation_handler.entity_image.copy()
        
        self.rendered_image.set_alpha(min(255, self.active))

         # Create a darkening surface that is affected by darkness
        dark_surface = pygame.Surface(self.rendered_image.get_size(), pygame.SRCALPHA).convert_alpha()
        dark_surface.fill((self.light_level, self.light_level, self.light_level, 255))  

        # Apply darkening effect using BLEND_RGBA_MULT
        self.rendered_image.blit(dark_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.render_needs_update = False