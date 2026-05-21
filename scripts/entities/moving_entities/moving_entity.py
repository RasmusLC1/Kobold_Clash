import math
import pygame
from scripts.entities.moving_entities.effects.effects_handler import Status_Effect_Handler
from scripts.entities.moving_entities.animation.animation_handler import Animation_Handler
from scripts.entities.moving_entities.moving_entity_functions.movement import Movement
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
        
        # Initialize the Movement component passing 'self' as the parent entity
        self.movement = Movement(self, max_speed, agility)

        self.attack_direction = (0,0)
        self.target = (0,0)
        self.active_ability = None
        
        self.damage_cooldown = 0
        
        self.nearby_traps = []
        self.nearby_traps_cooldown = 0
        self.nearby_enemies = []
        self.nearby_enemies_cooldown = 0

        # Attributes, placeholder should be assigned on creation
        self.strength = strength 
        self.strength_holder = strength 
        self.agility = agility 
        self.intelligence = intelligence 
        self.stamina = stamina 
        self.health = health
        self.healing_enabled = True
        self.max_health = self.health
        self.touching_ground = True 

        # Handle Blocking
        self.block_direction = (0,0)

        # Status Effects
        self.effects = self._effect_handler(self)
        self.animation_handler = self._animation_handler(self)

        self.active_weapon_cooldown = 0
        self.Set_Sprite()

    # --- Backward Compatibility Properties ---
    # These ensure external handlers can access movement values seamlessly
    @property
    def velocity(self): return self.movement.velocity
    @velocity.setter
    def velocity(self, val): self.movement.velocity = val


    @property
    def frame_movement(self): return self.movement.frame_movement
    @frame_movement.setter
    def frame_movement(self, val): self.movement.frame_movement = val

    @property
    def last_frame_movement(self): return self.movement.last_frame_movement
    @last_frame_movement.setter
    def last_frame_movement(self, val): self.movement.last_frame_movement = val

    @property
    def max_speed(self): return self.movement.max_speed
    @max_speed.setter
    def max_speed(self, val): self.movement.max_speed = val

    @property
    def max_speed_holder(self): return self.movement.max_speed_holder

    @property
    def friction(self): return self.movement.friction
    @friction.setter
    def friction(self, val): self.movement.friction = val

    @property
    def friction_holder(self): return self.movement.friction_holder

    @property
    def acceleration(self): return self.movement.acceleration
    @acceleration.setter
    def acceleration(self, val): self.movement.acceleration = val

    @property
    def acceleration_holder(self): return self.movement.acceleration_holder


    @property
    def pushed_entities(self): return self.movement.pushed_entities

    # --- Save & Load ---
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

    # --- Core Engine Cycle ---
    def Update(self, tilemap, delta_time, movement=(0, 0)):
        self.movement.Update_Movement(movement, delta_time)
        self.animation_handler.Update_Animation(movement, delta_time)
        self.Update_Status_Effects(delta_time)

        # self.Update_Traps(delta_time)
        self.Nearby_Enemies(2, delta_time)
        self.Update_Damage_Cooldown(delta_time)

        self.movement.Resolve_Movement(tilemap)
        self.Update_Tile(delta_time)

    # --- Movement Component Passthroughs ---
    def Reset_Velocity(self):
        self.movement.Reset_Velocity()

    def Push(self, direction, tilemap, push_strength=-1):
        self.movement.Push(direction, tilemap, push_strength)

    def Reduce_Movement(self, factor):
        self.movement.Reduce_Movement(factor)

    def Increase_Max_Speed(self, factor):
        self.movement.Increase_Max_Speed(factor)

    def Reset_Max_Speed(self):
        self.movement.Reset_Max_Speed()

    def On_Ice(self, effect):
        self.movement.On_Ice(effect)

    def Get_Pushed_Entities(self):
        return self.movement.pushed_entities

    # --- Entity Mechanics ---
    def Set_Active(self, duration):
        if hasattr(self, "effects"):
            if self.active_ability == keys.invisibility:
                return
        return super().Set_Active(duration)

    def Set_Description(self):
        pass
    
    def Attack_Direction_Handler(self):
        self.Set_Attack_Direction()
        self.animation_handler.Attack_Direction_Handler()

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

    def Update_Damage_Cooldown(self, delta_time):
        if self.damage_cooldown > 0:
            self.damage_cooldown -= delta_time
            if self.damage_cooldown <= 0:
                self.damage_cooldown = 0
    
    def Set_Damage_Cooldown(self):
        self.damage_cooldown = DAMAGE_COOLDOWN_MAX

    def Damage_Taken(self, damage, effect = (keys.slash, 0), direction = (0, 0), attacker = None):
        if self.health <= 0:
            return False
        if self.active_ability == keys.invulnerable:
            return False
        if self.Check_Blocking_Direction(direction) or self.damage_cooldown > 0:
            return False
        
        self.game.text_box_handler.Spawn_Damage_Text(self.pos.copy(), effect[0], str(damage))
        self.Set_Health(self.health - damage)
        self.Set_Description()
        
        self.effects.Damage_Taken(damage, attacker)
        if direction:
            strength_multiplier = 1
            if attacker:
                strength_multiplier = attacker.strength * 0.2
            self.Push(direction, self.game.tilemap, damage * strength_multiplier)
        
        if effect[1] > 0 and not keys.vampiric in effect[0]:
            effect_strength = max(effect[1] // 10, 1)
            self.effects.Set_Effect(effect[0], effect_strength)

        self.Check_If_Dead()
        return True

    def Check_If_Dead(self):
        if self.health > 0:
            return False
        if self.tile:
            self.tile.Clear_Entity(self.ID)
        self.game.enemy_handler.Delete_Enemy(self)
        self.effects.Reset_Effects()
        self.Update_Status_Effects(self.game.delta_time)
        self.render = False
        return True

    def Check_Blocking_Direction(self, direction) -> bool:
        if self.block_direction == (0, 0):
            return False
        
        attack_vector = pygame.math.Vector2(self.attack_direction)
        block_vector = pygame.math.Vector2(direction)

        if attack_vector.length() == 0 or block_vector.length() == 0:
            return False

        attack_vector.normalize_ip()
        block_vector.normalize_ip()

        dot_product = attack_vector.dot(block_vector)
        dot_product = max(-1.0, min(1.0, dot_product))
        angle = math.acos(dot_product)
        angle_degrees = math.degrees(angle)

        if angle_degrees >= 130:
            return True
        return False

    def Set_Attack_Direction(self, attack_direction=None):
        attack_direction = self.Check_Attack_Direction(attack_direction)
        if not attack_direction:
            self.Set_Target(self.game.player.pos)
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
                return None
            attack_direction = self.target
        return attack_direction

    def Reset_Attack_Direction(self):
        self.attack_direction = (0, 0)

    def Set_Frame_movement(self, movement):
        self.movement.frame_movement = movement

    def Set_Target(self, pos):
        self.target = pos

    def Set_Active_Ability(self, ability):
        if self.active_ability:
            return self.active_ability == ability                
        self.active_ability = ability
        return True
    
    def Remove_Active_Ability(self):
        self.active_ability = None

    def Set_Health(self, amount):
        self.health = amount

    def Set_Attack_Triggered(self):
        pass

    def Get_Effect(self, effect_name):
        return self.effects.Get_Effect(effect_name)

    def Get_Effect_Strength(self, effect_name):
        return self.effects.Get_Effect_Strength(effect_name)

    def Update_Status_Effects(self, delta_time):
        self.movement.friction = self.movement.friction_holder
        self.movement.max_speed = self.movement.max_speed_holder
        self.Set_Strength(self.strength_holder)
        self.effects.Update_Status_Effects(delta_time)

    def Set_Strength(self, strength):
        self.strength = strength
    
    def Set_Effect(self, effect, duration, permanent = False):
        return self.effects.Set_Effect(effect, duration, permanent)
    
    def Remove_Effect(self, effect, reduce_permanent = 0):
        return self.effects.Remove_Effect(effect, reduce_permanent)

    def Set_Block_Direction(self, direction):
        self.block_direction = direction

    def Set_Healing_Enabled(self, state):
        self.healing_enabled = state

    def Update_Health(self, value):
        self.health = min(self.max_health, self.health + value)
        self.Set_Description()

    def Increase_Max_Health(self, value):
        self.max_health += value

    def Set_Touching_Ground(self, state):
        self.touching_ground = state

    def Set_Action(self, movement = None):
        pass

    # --- Graphics Rendering ---
    def Render(self, surf, offset=(0, 0)):
        if not self.active:
            return False
        if not self.Update_Light_Level():
            return False
        if not self.animation_handler.entity_image:
            return False

        self.Update_Dark_Surface()
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

    def Update_Dark_Surface(self):
        if not self.render_needs_update:
            return
        if not self.animation_handler.entity_image:
            self.animation_handler.Set_Entity_Image()
            print("SET dark surface for entity: ", self.type, vars(self))
            return
        self.rendered_image = self.animation_handler.entity_image.copy()
        self.rendered_image.set_alpha(min(255, self.active))

        dark_surface = pygame.Surface(self.rendered_image.get_size(), pygame.SRCALPHA).convert_alpha()
        dark_surface.fill((self.light_level, self.light_level, self.light_level, 255))  

        self.rendered_image.blit(dark_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.render_needs_update = False