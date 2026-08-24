from scripts.entities.traps.trap import Trap
from scripts.engine.keys.keys import keys

class Spider_Web(Trap):
    def __init__(self, game, pos, speed = 0, direction = (0, 0), duration = 0, entity = None):
        super().__init__(game, pos, keys.spider_web)
        self.duration = duration
        self.active = False
        self.animation_max = 3
        self.delete = False
        self.frame_movement = (0, 0)
        self.direction = direction
        self.speed = speed
        self.entity = entity



        self.Determine_If_Shot_By_Spider()


    def Update(self, entity, delta_time):
        if self.Cooldown > 0:
            self.Cooldown -= 1
            return

        if self.delete:
            self.game.trap_handler.Remove_Trap(self)
            return
        
        self.entity_hit(entity)

    
    def entity_hit(self, entity):
        if entity.category == keys.item:
            return
        if entity == self.entity:
            return
        if self.rect().colliderect(entity.rect()) and self.Cooldown == 0:
            if entity.type == 'player':
                if entity.dashing:
                    return
            self.animation = self.animation_max
            entity.Set_Effect(keys.snare, 100)
            self.Cooldown = 100
            self.delete = True
            self.active = False

    def Determine_If_Shot_By_Spider(self):
        if self.duration:
            self.active = True
            self.animation = self.animation_max
        else:
            self.animation = self.animation_max

    def Update_Duration(self):
        if not self.active:
            return False
        
        if not self.duration:
            return True
        
        self.duration = max(0, self.duration - 1)
        return False

    # # TODO: Logic for spider shooting web
    def Shoot(self, delta_time = 0):
        if not self.active:
            return
        direction_x = self.direction[0] * self.speed
        direction_y = self.direction[1] * self.speed
        self.frame_movement = (direction_x, direction_y)
        print("FRAME MOVEMENT", self.frame_movement)
        if self.Tile_Map_Collision_Detection(self.game.tilemap):
            print("TILE HIT")
            self.active = False
            
    
    # Return True if spiderweb hits wall
    def Tile_Map_Collision_Detection(self, tilemap):
        self.pos[0] += self.frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                
                self.pos[0] = entity_rect.x
                return True
        
        self.pos[1] += self.frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                
                self.pos[1] = entity_rect.y
                return True

        return False
