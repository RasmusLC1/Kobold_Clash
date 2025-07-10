import math
import pygame
from scripts.entities.moving_entities.effects.effects_handler import Status_Effect_Handler
from scripts.entities.moving_entities.animation.animation_handler import Animation_Handler
from scripts.entities.entities import PhysicsEntity
from scripts.engine.keys.keys import keys

class Moving_Entity(PhysicsEntity):

    _animation_handler = Animation_Handler
    _effect_handler = Status_Effect_Handler


    
    def __init__(self, game, type, category, pos, size, health, strength, max_speed, agility, intelligence, stamina, sub_category):
        super().__init__(game, type, category, pos, size, sub_category)
        self.velocity = [0, 0] # Velocity of the player
        
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False} # Check for wall collision in each direction
        self.update_tile_cooldown = 0


        self.animation_state = 'up'
        self.idle_count = 0

        self.charging = 0

        self.direction = (0,0)
        self.direction_x = 0
        self.direction_y = 0
        self.direction_x_holder = 0
        self.direction_y_holder = 0
        self.attack_direction = (0,0)
        self.target = (0,0)
        

        self.damage_cooldown = 0
        self.damage_cooldown_max = 40
        
        self.nearby_traps = []
        self.nearby_traps_cooldown = 0
        self.nearby_enemies = []
        self.nearby_enemies_cooldown = 0
        
        self.action = ''
        self.anim_offset = (0, 0)
        self.flip = [False, False]
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
        self.friction = 0.8 # Friction, set to the renderscale
        self.friction_holder = self.friction # Holder for friction to reset it
        self.acceleration = agility / 5 * self.game.render_scale
        self.acceleration_holder = self.acceleration # accelarition holder to reset it
        self.max_speed = max_speed * self.game.render_scale + agility # Max speed of the entity
        self.max_speed_holder = self.max_speed # Max speed holder to reset it


        # Determined by the entities agility
        self.left_weapon_cooldown = 0 
        self.right_weapon_cooldown = 0


        # Handle attack animations
        self.attacking = 0

        # Handle Blocking
        self.block_direction = (0,0)

        # Status Effects
        self.effects = self._effect_handler(self)
        self.animation_handler = self._animation_handler(self)
        
        

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
        self.saved_data.update(self.effects.Save_Data())


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
        self.effects.Load_Data(data)
    


    # Update the entity 
    def Update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        self.Update_Movement(movement)
        self.Update_Status_Effects()


        self.Update_Traps()
        self.Nearby_Enemies(2)
        self.Update_Damage_Cooldown()
        self.Charge_Update()

        self.Movement(movement, tilemap)
        self.Update_Tile()
    

    def Update_Movement(self, movement):
        # Apply acceleration to velocity based on input
        self.velocity[0] += movement[0] * self.acceleration
        self.velocity[1] += movement[1] * self.acceleration

        # Clamp the velocity to max speed
        self.velocity[0] = max(-self.max_speed, min(self.velocity[0], self.max_speed))
        self.velocity[1] = max(-self.max_speed, min(self.velocity[1], self.max_speed))
        
        # Apply friction and elimnates fricting
        if abs(self.velocity[0]) > 0.1:
            self.velocity[0] *= self.friction
        else:
            self.velocity[0] = 0
        if abs(self.velocity[1]) > 0.1:
            self.velocity[1] *= self.friction
        else:
            self.velocity[1] = 0

        self.direction_x = movement[0]
        self.direction_y = movement[1]

        # Calculate frame movement based on updated velocity
        self.Set_Frame_movement((
            self.velocity[0] / self.game.render_scale,
            self.velocity[1] / self.game.render_scale
        ))


    # Movement handling
    def Movement(self, movement, tilemap):
        if self.Entity_Collision_Detection(tilemap):
            return

        self.Tile_Map_Collision_Detection(tilemap)
        if self.attacking:
            return
        
        self.Set_Action(movement)

        if self.idle_count > 60:
            self.animation_handler.Set_Idle()
        else:
            self.idle_count += 1

        if keys.attack in self.animation_handler.animation:
            self.animation_handler.Update_Attack_Animation()
        elif 'jumping' in self.animation_handler.animation:
            self.animation_handler.Update_Jumping_Animation()
        else:
            self.animation_handler.Update_Animation()

        self.last_frame_movement = self.frame_movement
    
    def Update_Tile(self):
        if self.update_tile_cooldown:
            self.update_tile_cooldown -= 1

        self.update_tile_cooldown = 10

        # Error handling, if no tile is found teleport
        if not self.tile:
            new_tile = self.game.tilemap.Get_Random_Tile_With_Path_To_Player()
            self.game.tilemap.Add_Entity_To_Tile(new_tile, self)
            self.tile = new_tile
            self.pos = list((self.tile.pos[0] * 32, self.tile.pos[1] * 32))

            print("ERROR TILE NOT FOUND", self.type, self.pos, self.tile)
            return
        
        new_tile_key = str(int(self.pos[0] // self.game.tilemap.tile_size)) + ';' + str(int(self.pos[1] // self.game.tilemap.tile_size))
        if new_tile_key != self.tile.pos:
            new_tile = self.game.tilemap.Current_Tile(new_tile_key)
            if not new_tile:
                return
            self.game.tilemap.Remove_Entity_From_Tile(self.tile, self.ID)
            self.game.tilemap.Add_Entity_To_Tile(new_tile, self)
            self.tile = new_tile
            

    def Set_Active(self, duration):
        # use hasattr to check if self.effects exists
        if hasattr(self, "effects"):
            if self.effects.invisibility.effect:
                return
        return super().Set_Active(duration)
    

    def Set_Description(self):
        pass
        

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


    def Entity_Collision_Detection(self, tilemap):
        future_pos = (self.pos[0] + self.frame_movement[0], self.pos[1] + self.frame_movement[1])
        for enemy in self.nearby_enemies:
            if enemy != self and enemy.rect().colliderect(self.rect_future(future_pos)):
                self.Apply_Repulsion(enemy, tilemap)
                return enemy
        
        # Handle collision with the player
        if self.type != 'player' and self.game.player.rect().colliderect(self.rect_future(future_pos)):
            self.Apply_Repulsion(self.game.player, tilemap)
            return self.game.player
                
        return None

    def Apply_Repulsion(self, other_entity, tilemap) -> None:
        if not other_entity:
            return
        # Check if entity is stronger than the other, if no then simply return as it cannot push it
        if self.strength < other_entity.strength:
            return

        # Calculate repulsion strength based on strength
        repulsion_strength = 1 + (self.strength - other_entity.strength) / 10

        direction_vector = pygame.math.Vector2(self.pos) - pygame.math.Vector2(other_entity.pos)
        if direction_vector.length() < 0:
            return
        if direction_vector:
            direction_vector.normalize_ip()

        direction_vector *= repulsion_strength

        # Push the other entity backwards
        other_entity.Push(direction_vector, tilemap)
    

    def rect_future(self, future_pos):
        return pygame.Rect(future_pos[0], future_pos[1], self.size[0], self.size[1])     
    

    # Update only the nearby traps
    def Update_Traps(self):
        if not self.nearby_traps_cooldown:
            self.Find_Nearby_Traps(3)
            self.nearby_traps_cooldown = 10
        else:
            self.nearby_traps_cooldown -= 1
        for trap in self.nearby_traps:
            trap.Add_Entity_To_Trap(self)

    def Find_Nearby_Traps(self, distance) -> None:
        if self.nearby_traps_cooldown:
            self.nearby_traps_cooldown = max(0, self.nearby_traps_cooldown - 1)
            return
        self.nearby_traps = self.game.trap_handler.Find_Nearby_Traps(self, distance)
        self.nearby_traps_cooldown = 20
        return
    

    def Nearby_Enemies(self, max_distance) -> None:
        if self.nearby_enemies_cooldown:
            self.nearby_enemies_cooldown = max(0, self.nearby_enemies_cooldown - 1)
            return
        self.nearby_enemies.clear()
        self.nearby_enemies = self.game.enemy_handler.Find_Nearby_Enemies(self, max_distance)
        self.nearby_enemies_cooldown = 20
        return
    

    def Update_Damage_Cooldown(self):
        if self.damage_cooldown:
            self.damage_cooldown -= 1
            
            
    # Damage = Total damage, effect = (effect, effect strength) 
    def Damage_Taken(self, damage, effect = (keys.slash, 0), direction = (0, 0)):
        if self.Check_Blocking_Direction(direction):
            return False
        self.game.text_box_handler.Spawn_Damage_Text(self.pos.copy(), effect[0], str(damage))

        self.damage_cooldown = self.damage_cooldown_max
        self.Set_Health(self.health - damage)

        # Update the entitty description
        self.Set_Description()
        
        # Check if any active effects affect damage
        self.effects.Damage_Taken(damage)
        if direction:
            self.Push(direction, self.game.tilemap, damage)
        
        if effect[1] > 0 and not keys.vampiric in effect[0]:
            self.effects.Set_Effect(effect[0], effect[1])

        self.Check_If_Dead()

        
        return True
    

    
    def Check_If_Dead(self):
        if self.health > 0: # Entity alive
            return False
        if self.tile:
            self.tile.Clear_Entity(self.ID)
        self.game.enemy_handler.Delete_Enemy(self)
        self.effects.Reset_Effects()
        self.Update_Status_Effects()
        self.text_box = None
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


    def Attack_Direction_Handler(self):
        self.Set_Attack_Direction()
        
        if self.attack_direction[0] < 0:
            self.flip[0] = True
            self.animation_handler.Set_Animation(keys.attack)

        else:
            self.flip[0] = False
            self.animation_handler.Set_Animation(keys.attack)

        if self.attack_direction[1] < -0.5:
            # TODO: UPDATE to attack up when that has been animated
            self.animation_handler.Set_Animation(keys.attack)


    def Set_Attack_Direction(self, attack_direction=None):
        if not attack_direction:
            attack_direction = self.target
        self.attack_direction = pygame.math.Vector2(
            attack_direction[0] - self.pos[0],
            attack_direction[1] - self.pos[1]
        )
        if self.attack_direction.length_squared() == 0:
            return
        self.attack_direction.normalize_ip()

    def Reset_Attack_Direction(self):
        self.attack_direction = (0, 0)

    def Set_Charge(self, charge_speed, offset=(0, 0)):
        if not self.charging:
            self.charging = min(12, charge_speed)


    # Handle Charging Updates
    def Charge_Update(self):
        if self.charging <= 0:
            return
        self.max_speed = 40  # Adjust max speed speed for dashing distance
        self.charging = max(0, self.charging - 1)
        

        self.velocity[0] = self.attack_direction[0] * 100
        self.velocity[1] = self.attack_direction[1] * 100


    def Set_Frame_movement(self, movement):
        self.frame_movement = movement

    def Set_Target(self, pos):
        self.target = pos

    def Set_Health(self, amount):
        self.health = amount

    def Reduce_Movement(self, factor):
        self.max_speed = self.max_speed // factor

    def Reset_Max_Speed(self):
        self.max_speed = self.max_speed_holder
        
    # Push the entity in the given direction
    def Push(self, direction, tilemap, push_strength = -1):
        self.Set_Frame_movement((direction[0] * push_strength, direction[1] * push_strength))
        self.effects.Push(direction)
        self.Tile_Map_Collision_Detection(tilemap)


    # Ice mechanic, lower friction and acceleration to simulate ice
    def On_Ice(self, effect):
        self.friction = max(0.1, self.friction / effect)
        self.acceleration = max(0.3, self.acceleration / effect)

    # Handle status effects
    def Update_Status_Effects(self):
        self.friction = self.friction_holder
        self.max_speed = self.max_speed_holder
        self.Set_Strength(self.strength_holder)
        self.effects.Update_Status_Effects()

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

    def Set_Action(self, movement = None):
        if not movement:
            return
        if not movement[0] and not movement[1]:
            if self.direction_y_holder < 0:
                self.animation_handler.Set_Animation('standing_still_up')
            else:
                self.animation_handler.Set_Animation('standing_still_down')
            return

        self.idle_count = 0

        # Determine animation and flip based on movement
        if movement[0] > 0:
            self.flip[0] = False
        elif movement[0] < 0:
            self.flip[0] = True

        if movement[1] < 0:
            self.animation_handler.Set_Animation('running_up')
        else:
            self.animation_handler.Set_Animation('running_down')


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

        surf.blit(pygame.transform.flip(self.rendered_image, self.flip[0], False), 
                (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))
        return True
    
    def Render_Damage(self, surf, offset):
        self.Lightup(self.rendered_image)


    def Lightup(self, entity_image):
        if self.damage_cooldown < self.damage_cooldown_max - 10:
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