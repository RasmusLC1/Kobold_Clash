import pygame

class Movement:
    def __init__(self, entity, max_speed, agility, ethereal=False):
        self.entity = entity  # Keep reference to the master entity object
        self.ethereal = ethereal  # If True, bypasses tilemap solid collisions entirely
        
        self.velocity = [0.0, 0.0]

        # Consolidated direction handling
        self.direction = pygame.math.Vector2(0, 0)
        self.direction_holder = pygame.math.Vector2(0, 0)
        
        self.frame_movement = (0.0, 0.0)
        self.last_frame_movement = (0.0, 0.0)

        # Physics variables Setup
        self.friction = 0.0001 
        self.friction_holder = self.friction 
        self.acceleration = agility * 1000
        self.acceleration_holder = self.acceleration 
        self.max_speed = max_speed * 100  
        self.max_speed_holder = self.max_speed 

        self.pushed_entities = set()

    def Update_Movement(self, movement, delta_time):
        # Apply acceleration (units/sec^2 -> velocity in units/sec)
        self.velocity[0] += movement[0] * self.acceleration * delta_time
        self.velocity[1] += movement[1] * self.acceleration * delta_time
        
        # Clamp velocity
        self.velocity[0] = max(-self.max_speed, min(self.velocity[0], self.max_speed))
        self.velocity[1] = max(-self.max_speed, min(self.velocity[1], self.max_speed))

        # Apply friction
        if abs(self.velocity[0]) > 0.1:
            self.velocity[0] *= self.friction ** delta_time
        else:
            self.velocity[0] = 0.0
            
        if abs(self.velocity[1]) > 0.1:
            self.velocity[1] *= self.friction ** delta_time
        else:
            self.velocity[1] = 0.0

        # Sync the unified direction vector with current movement input
        self.direction.update(movement[0], movement[1])
        
        # Apply velocity to movement calculations
        self.frame_movement = (
            (self.velocity[0] * delta_time) / self.entity.game.render_scale,
            (self.velocity[1] * delta_time) / self.entity.game.render_scale
        )

    def Reset_Velocity(self):
        self.velocity = [0.0, 0.0]

    def Resolve_Movement(self, tilemap):
        self.Entity_Collision_Detection()
        
        if self.Apply_Repulsion(tilemap):
            self.last_frame_movement = self.frame_movement
            return  
            
        self.Tile_Map_Collision_Detection(tilemap)
        self.last_frame_movement = self.frame_movement

    def Tile_Map_Collision_Detection(self, tilemap):

        # Early out for ethereal entities — move smoothly without scanning tiles
        if self._Resolve_Ethereal_Movement():
            return

        # Fetch nearby tile rects once to minimize method-call overhead
        self.Update_X_Axis(tilemap)

        self.Update_Y_Axis(tilemap)
        

    def Update_X_Axis(self, tilemap):

        if self.frame_movement[0] == 0:
            return
        
        # Move entity
        self.entity.pos[0] += self.frame_movement[0]
        
        nearby_rects = tilemap.physics_rects_around(self.entity.pos)
        entity_rect = self.entity.rect()
        
        for rect in nearby_rects:
            if entity_rect.colliderect(rect):
                if self.frame_movement[0] > 0:
                    # Snap the rect, then calculate the precise float position shift
                    offset = rect.left - entity_rect.right
                    self.entity.pos[0] += offset
                elif self.frame_movement[0] < 0:
                    offset = rect.right - entity_rect.left
                    self.entity.pos[0] += offset
                break  # Axis collision resolved, skip remaining X checks

        return

    def Update_Y_Axis(self, tilemap):
        if self.frame_movement[1] == 0:
            return
        
        self.entity.pos[1] += self.frame_movement[1]
        
        nearby_rects = tilemap.physics_rects_around(self.entity.pos)
        entity_rect = self.entity.rect()
        
        for rect in nearby_rects:
            if entity_rect.colliderect(rect):
                if self.frame_movement[1] > 0:
                    offset = rect.top - entity_rect.bottom
                    self.entity.pos[1] += offset
                elif self.frame_movement[1] < 0:
                    offset = rect.bottom - entity_rect.top
                    self.entity.pos[1] += offset
                break  # Axis collision resolved, skip remaining Y checks
                
        return


    def _Resolve_Ethereal_Movement(self):
        if not self.ethereal:
            return False
        
        self.entity.pos[0] += self.frame_movement[0]
        self.entity.pos[1] += self.frame_movement[1]
        return True

    def Entity_Collision_Detection(self):
        self.pushed_entities.clear()
        future_pos = (self.entity.pos[0] + self.frame_movement[0], self.entity.pos[1] + self.frame_movement[1])
        
        for enemy in self.entity.nearby_enemies:
            if enemy != self.entity and enemy.rect().colliderect(self.Rect_Future(future_pos)):
                self.pushed_entities.add(enemy)
                
        # Also check collision with the player explicitly if this isn't the player
        if self.entity.type != 'player' and self.entity.game.player.rect().colliderect(self.Rect_Future(future_pos)):
            self.pushed_entities.add(self.entity.game.player)
                
        return self.pushed_entities

    def Apply_Repulsion(self, tilemap) -> bool:
        if not self.pushed_entities:
            return False
        
        collided = False
        for entity in list(self.pushed_entities):
            if self.entity.strength <= entity.strength:
                continue

            collided = True
            repulsion_strength = 1 + (self.entity.strength - entity.strength) / 10
            
            # Point vector from PUSHER -> PUSHED entity
            direction_vector = pygame.math.Vector2(entity.pos) - pygame.math.Vector2(self.entity.pos)
            
            if direction_vector.length_squared() == 0:
                continue
                
            direction_vector.normalize_ip()

            # Pass positive strength value explicitly
            entity.Push(direction_vector, tilemap, push_strength=repulsion_strength)
            
        return collided

    def Rect_Future(self, future_pos):
        return pygame.Rect(future_pos[0], future_pos[1], self.entity.size[0], self.entity.size[1])     

    def Push(self, direction, tilemap, push_strength=1.0):
        if direction is None:
            return  
        
        # Ensure push_strength behaves as a positive force multiplier
        push_strength = abs(push_strength)
        
        # Modify the internal component velocity directly
        self.velocity[0] += direction[0] * push_strength * 500
        self.velocity[1] += direction[1] * push_strength * 500

        self.entity.effects.Push(direction)

    def Reduce_Movement(self, factor):
        self.max_speed = self.max_speed // factor

    def Increase_Max_Speed(self, factor):
        self.max_speed *= factor

    def Reset_Max_Speed(self):
        self.max_speed = self.max_speed_holder

    def Set_Ethereal(self, state):
        self.ethereal = state

    def On_Ice(self, effect):
        self.friction = max(0.1, self.friction * effect)
        self.acceleration = max(0.3, self.acceleration / effect / 10)

    def Set_Direction(self, direction):
        if not isinstance(direction, pygame.math.Vector2):
            direction = pygame.math.Vector2(direction)
            
        if direction.length_squared() > 0:
            direction.normalize_ip()
        self.direction = direction

    def Set_Direction_Holder(self):
        if self.direction.length_squared() > 0:
            self.direction_holder.update(self.direction.x, self.direction.y)