import pygame

class Movement:
    def __init__(self, entity, max_speed, agility):
        self.entity = entity  # Keep reference to the master entity object
        
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        self.direction = (0, 0)
        self.direction_x = 0
        self.direction_y = 0
        self.direction_x_holder = 0
        self.direction_y_holder = 0
        
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
            self.velocity[0] = 0
            
        if abs(self.velocity[1]) > 0.1:
            self.velocity[1] *= self.friction ** delta_time
        else:
            self.velocity[1] = 0

        self.direction_x = movement[0]
        self.direction_y = movement[1]
        
        # Apply velocity to movement calculations
        self.frame_movement = (
            (self.velocity[0] * delta_time) / self.entity.game.render_scale,
            (self.velocity[1] * delta_time) / self.entity.game.render_scale
        )

    def Reset_Velocity(self):
        self.velocity = [0, 0]

    def Resolve_Movement(self, tilemap):
        self.Entity_Collision_Detection()
        self.Apply_Repulsion(tilemap)
        self.Tile_Map_Collision_Detection(tilemap)
        self.last_frame_movement = self.frame_movement

    def Tile_Map_Collision_Detection(self, tilemap):
        self.entity.pos[0] += self.frame_movement[0]
        entity_rect = self.entity.rect()
        for rect in tilemap.physics_rects_around(self.entity.pos):
            if entity_rect.colliderect(rect):
                if self.frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if self.frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.entity.pos[0] = entity_rect.x
        
        self.entity.pos[1] += self.frame_movement[1]
        entity_rect = self.entity.rect()
        for rect in tilemap.physics_rects_around(self.entity.pos):
            if entity_rect.colliderect(rect):
                if self.frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if self.frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.entity.pos[1] = entity_rect.y

    def Entity_Collision_Detection(self):
        self.pushed_entities.clear()
        future_pos = (self.entity.pos[0] + self.frame_movement[0], self.entity.pos[1] + self.frame_movement[1])
        for enemy in self.entity.nearby_enemies:
            if enemy != self.entity and enemy.rect().colliderect(self.Rect_Future(future_pos)):
                self.pushed_entities.add(enemy)
                
        return future_pos

    def Apply_Repulsion(self, tilemap) -> None:
        if not self.pushed_entities:
            return
        
        for entity in self.pushed_entities:
            if self.entity.strength < entity.strength:
                return

            repulsion_strength = 1 + (self.entity.strength - entity.strength) / 10
            direction_vector = pygame.math.Vector2(self.entity.pos) - pygame.math.Vector2(entity.pos)
            
            if direction_vector.length() < 0:
                return
            if direction_vector:
                direction_vector.normalize_ip()

            direction_vector *= repulsion_strength
            entity.Push(direction_vector, tilemap)

    def Rect_Future(self, future_pos):
        return pygame.Rect(future_pos[0], future_pos[1], self.entity.size[0], self.entity.size[1])     

    def Push(self, direction, tilemap, push_strength=-1):
        if direction is None:
            return  
        self.frame_movement = (direction[0] * push_strength, direction[1] * push_strength)
        self.entity.effects.Push(direction)
        self.Tile_Map_Collision_Detection(tilemap)

    def Reduce_Movement(self, factor):
        self.max_speed = self.max_speed // factor

    def Increase_Max_Speed(self, factor):
        self.max_speed *= factor

    def Reset_Max_Speed(self):
        self.max_speed = self.max_speed_holder

    def On_Ice(self, effect):
        self.friction = max(0.1, self.friction * effect)
        self.acceleration = max(0.3, self.acceleration / effect / 10)


    def Set_Direction(self, direction):
        if direction.length() > 0:
            direction.normalize_ip()
        self.direction = direction

    def Set_Direction_Holder(self):
        if self.direction_x or self.direction_y:
            self.direction_x_holder = self.direction_x
            self.direction_y_holder = self.direction_y