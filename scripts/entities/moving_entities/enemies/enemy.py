from scripts.entities.moving_entities.moving_entity import Moving_Entity
from scripts.entities.textbox.enemy_textbox import Enemy_Textbox
from scripts.entities.decoration.shared.bones.bones import Bones 
from scripts.entities.moving_entities.enemies.behavior.intent_manager import Intent_Manager
from scripts.engine.keys.keys import keys
from scripts.entities.moving_entities.enemies.attribute_distributor.attribute_distributor import Attribute_Distributor

import math
import pygame
import random


class Enemy(Moving_Entity):
    intent_manager_class = Intent_Manager 

    def __init__(self, game, pos, type, is_elite=False):

        # 1. Fetch the Profile (Contains scaled stats AND animation info)
        stats = Attribute_Distributor.Get_Enemy_Profile(type, game.depth, is_elite)
        
        self.max_weapon_charge = stats.max_weapon_charge
        self.soul_value = stats.souls
        
        # 2. Call super().__init__ using the clean attributes
        super().__init__(
            game, str(type), keys.enemy, pos, stats.size,
            stats.health,
            stats.strength,
            stats.speed,
            stats.agility,
            stats.intelligence,
            stats.stamina,
            stats.sub_category
        )
        
        self.Set_Description()
        
        # --- Animation Setup ---
        self.animation_handler.Set_Animation_Num_Max(keys.run, stats.run_animation)
        self.animation_handler.Set_Animation_Num_Max(keys.idle, stats.idle_animation)
        self.animation_handler.Set_Animation_Num_Max(keys.attack, stats.attack_animation)
        self.animation_handler.Set_Animation('running')


        # --- Combat & AI State ---
        self.alert_cooldown = 0
        self.active_weapon = None
        self.target = self.game.player.pos
        self.charge = 0
        self.damaged = False 

        self.distance_to_player = 9999
        self.player_spotted = False
        self.attack_distance = self.size[0] * 2 
        self.distance_calculation_cooldown = 0

        self.locked_on_target = 0 
        self.attack_symbol_offset = 20
        self.health_bar = self.game.assets[keys.health_bar]

        # 4. Initialize Intent Manager using the clean behavior and ability strings
        self.intent_manager = self.intent_manager_class(
            game, self, stats.path_finding_strategy, 
            stats.behavior, self.max_weapon_charge
        )

        self.Set_Ability(stats.ability)
        self.Set_Description()

    
    def Save_Data(self):
        super().Save_Data()
        self.intent_manager.Save_Data()
        self.saved_data['alert_cooldown'] = self.alert_cooldown
        self.saved_data['distance_to_player'] = self.distance_to_player
        self.saved_data['charge'] = self.charge
        self.saved_data['locked_on_target'] = self.locked_on_target
        self.saved_data['target'] = self.target


    def Load_Data(self, data):
        super().Load_Data(data)
        self.intent_manager.Load_Data(data)
        self.alert_cooldown = data['alert_cooldown']
        self.distance_to_player = data['distance_to_player']
        self.charge = data['charge']
        self.locked_on_target = data['locked_on_target']
        self.target = data['target']


    def Update(self, tilemap, delta_time, movement=(0, 0)):
        # 1. Calculate player distance states
        self.Calculate_Distance_To_Player(delta_time)
        
        # 2. Run AI logic FIRST (This updates self.movement.direction via Calculate_Path_Segment)
        self.intent_manager.Update_Intent(delta_time)
        
        # 3. Grab the freshly calculated AI direction vector
        movement = self.movement.direction
        
        # 4. Pass it down to the engine physics/movement handlers
        super().Update(tilemap, delta_time, movement)

        # 5. Handle post-movement updates
        self.movement.Set_Direction_Holder()
        self.Update_Alert_Cooldown(delta_time)
        self.Update_Locked_On_Target(delta_time)
        self.Set_Damaged(False)
        self.Reset_Max_Speed()


    def Calculate_Distance_To_Player(self, delta_time):
        if self.distance_calculation_cooldown > 0:
            self.distance_calculation_cooldown = max(0, self.distance_calculation_cooldown - delta_time)
            return
         
        max_distance_cooldown = random.uniform(0.2, 0.3) # randomise time to prevent simultaneous updates
        self.distance_calculation_cooldown = max_distance_cooldown
        
        player_pos = self.game.player.pos
        self.distance_to_player = math.sqrt((player_pos[0] - self.pos[0]) ** 2 + (player_pos[1] - self.pos[1]) ** 2)


    def Set_Charge_To_Max(self):
        self.charge = self.max_weapon_charge
    
    def Movement_Strategy(self, delta_time):
        return self.intent_manager.Movement_Strategy(delta_time)
    
    def Set_Active_Weapon(self, weapon):
        self.active_weapon = weapon

    def Update_Alert_Cooldown(self, delta_time):
        if self.alert_cooldown:
            self.alert_cooldown = max(0, self.alert_cooldown - delta_time)

    def Set_Alert_Cooldown(self, amount):
        self.alert_cooldown = amount

    def Find_New_Path(self):
        self.intent_manager.Find_New_Path()

    def Set_Direction(self, direction):
        self.movement.Set_Direction(direction)
        

    def Update_Locked_On_Target(self, delta_time):
        if not self.locked_on_target:
            return
        self.locked_on_target = max(0, self.locked_on_target - delta_time)
    
    def Set_Locked_On_Target(self, value):
        self.locked_on_target = value
        
    def Damage_Taken(self, damage, effect = (keys.slash, 0), direction = (0, 0), attacker = None):
        # Adjusts damage taken based on abilities
        final_damage = self.intent_manager.Damage_Taken(damage, effect, direction, attacker)
        
        if final_damage > 0:
            self.Spawn_Damaged_Particles()
            self.Set_Damaged(True)
        
        # Pass final modified damage downward to subtract from entity HP
        if not super().Damage_Taken(final_damage, effect, direction, attacker):
            return False # Entity survived
        
        self.Delete() # Entity died
        return True
    
    # Used to check if enemy is damaged this tick
    def Set_Damaged(self, state):
        self.damaged = state

    
    def Delete(self, generate_soul = True):
        if self.health > 0:
            return False
        
        self.Spawn_Bones()
        self.Drop_Loot()
        self.game.enemy_handler.Delete_Enemy(self)
        self.game.entities_render.Remove_Entity(self)
        if self.distance_to_player < 300 and generate_soul:
            self.game.player.Increase_Souls(self.soul_value)
        super().Delete()
        return True


    def Set_Action(self, movement = None):
        if self.distance_to_player > 300 :
            return
        
        if self.charge > 0:
            self.animation_handler.Set_Animation(keys.attack)
        elif self.movement.frame_movement:  # Updated to look inside movement component
            self.animation_handler.Set_Animation('running')
        else:
            self.animation_handler.Set_Animation('idle')

    def Set_Target(self, pos = None):
        if not pos:
            pos = self.game.player.pos
        return super().Set_Target(pos)


    def Spawn_Damaged_Particles(self):
        self.game.particle_handler.Activate_Particles(10, keys.blood_particle, self.rect().center, random.uniform(0.2, 0.5))


    def Spawn_Bones(self):
        bones = Bones(self.game, self.pos, self.type)
        self.game.decoration_handler.Add_Decoration(bones)
        return

    def Drop_Loot(self):
        loot_weights = {keys.passive : 0.05,
                        keys.key : 0.2,
                        keys.bomb : 0.4,
                        keys.potion : 0.5,
                        keys.revive : 0.05,
                        keys.utility : 0.1,
                        keys.curse : 0.1,
                        keys.valuable : 2.0,
                        keys.nothing : 3.0}
        
        loot_types = list(loot_weights.keys())
        weight_values = [loot_weights[loot_type] for loot_type in loot_types]
        loot_type = random.choices(loot_types, weight_values, k=1)[0]

        if loot_type == keys.nothing:
            return
        
        self.game.item_handler.Spawn_Item_By_Type(loot_type, self.pos)
    

    def Set_Description(self):
        self.description = (
                            f"health {self.health}\n"
                            f"increase_strength {self.strength}\n"
                            f"speed {self.agility}\n"
                        )

    
    # NOTE: This version of the method is currently overwritten by the one below it in Python.
    # It has been updated to be vector-compatible just in case you plan to rename or merge it.
    def Entity_Collision_Detection_With_Tilemap(self, tilemap):
        colliding_entity = super().Entity_Collision_Detection(tilemap)

        if colliding_entity:
            if colliding_entity.type == 'player':
                self.movement.direction.update(0, 0)
                return colliding_entity

            # Collision logic for other entities
            collision_vector = pygame.math.Vector2(self.pos[0] - colliding_entity.pos[0],
                                                   self.pos[1] - colliding_entity.pos[1])
            if collision_vector.length_squared() > 0:
                collision_vector = collision_vector.normalize()
                direction_vector = pygame.math.Vector2(self.movement.direction)
                reflected_direction = direction_vector.reflect(collision_vector)

                if self.Future_Rect(reflected_direction).colliderect(self.game.player.rect()):
                    self.movement.direction.update(0, 0)
                    return self.game.player

                self.movement.direction.update(reflected_direction.x, reflected_direction.y)

        return None
    

    def Trap_Collision_Handler(self):
        for trap in self.nearby_traps:
            if self.rect().colliderect(trap.rect()):
                # Run away in the same direction the enemy was moving previously
                # Utilizes the updated Vector2 holder properties (.x and .y)
                dir_x = max(-0.4, self.movement.direction_holder.x * 4) if self.movement.direction_holder.x < 0 else min(0.4, self.movement.direction_holder.x * 4)
                dir_y = max(-0.4, self.movement.direction_holder.y * 4) if self.movement.direction_holder.y < 0 else min(0.4, self.movement.direction_holder.y * 4)
                
                self.movement.direction.update(dir_x, dir_y)
            else:
                # Check if the enemy will collide soon, if yes redirect in the opposite direction
                if self.Future_Rect(self.movement.direction).colliderect(trap.rect()):
                    self.movement.direction *= -1
                    break
    
    def Set_Attack_Direction(self):
        if not self.charge > 0:
            self.attack_direction = (0, 0)
            return
        super().Set_Attack_Direction()

    def Improve_Weapon(self, effect, amount):
        if not self.active_weapon:
            print("FAILED TO IMPROVE WEAPON, ", effect, self.type, vars(self))

        self.active_weapon.Set_Damage(effect, amount)

        
    def Set_Text_Box(self):
        self.text_box = Enemy_Textbox(self)


    def Future_Rect(self, direction):
         return pygame.Rect(self.pos[0] + direction[0]*32, self.pos[1] + direction[1]*32, self.size[0], self.size[1])

    
    # RENDER FUNCTIONS
    def Render(self, surf, offset = (0,0)):
        if not super().Render(surf, offset):
            return False
        
        if self.active <= 100: # Invisibility has lower limit of 100 active for level 1
            return False
        
        self.Render_Health_Bar(surf, offset)
        self.Render_Attacking_Symbol(surf, offset)
        self.intent_manager.Render_Abilities(surf, offset) # Function to render all passive abilities
        return True

    
    def Get_Health_Index(self):
        if self.health == self.max_health:
            return 0
        health_fraction = self.health / self.max_health
        health_index = max(-1, min(int((1 - health_fraction) * 9), 9))
        return health_index


    def Render_Health_Bar(self, surf, offset = (0,0)):
        health_index = self.Get_Health_Index()
        health_bar = self.health_bar[health_index]
        surf.blit(health_bar, (self.rect().left - offset[0], self.rect().bottom - offset[1] - self.size[1] // 2 + 4))


    def Equip_Weapon(self, weapon):
        if not weapon:
            return False

        weapon.Pickup_Reset_Weapon(self)
        weapon.Set_Equip(True, self)
        self.Set_Active_Weapon(weapon)

        self.active_weapon.render = False
        del(weapon)
        return True
    

    def Trigger_Attack(self):
        self.Set_Target()
        self.Trigger_Basic_Attack()
        self.intent_manager.Reset_Attack()


    def Trigger_Basic_Attack(self):
        if not self.active_weapon:
            return
        
        self.active_weapon.Set_Attack()
    

    def Set_Charge(self, charge):
        self.charge = charge


    # This is the active collision method overriding the tilemap signature variant above
    def Entity_Collision_Detection(self):
        future_pos = super().Entity_Collision_Detection()
        player = self.game.player
        
        # Handle collision with the player using the component set
        if player.rect().colliderect(self.rect_future(future_pos)):
            self.movement.pushed_entities.add(player)
        
        return future_pos


    def Set_Ability(self, ability_name):
        self.intent_manager.Set_Ability(ability_name)

    def Set_Retreat(self):
        return self.intent_manager.Set_Retreat()
    
    def Trigger_Instant_Attack(self):
        return self.intent_manager.Trigger_Instant_Attack()
    
    def Reset_Attack_Speed(self):
        return self.intent_manager.Reset_Attack_Speed()
    
    def Set_Behavior_Pattern(self, pattern):
        return self.intent_manager.Set_Behavior_Pattern(pattern)
    
    def Set_Max_Weapon_Charge(self, amount):
        self.max_weapon_charge = amount

    def Set_Player_Spotted(self, state):
        self.player_spotted = state

    def Reset_Behavior(self):
        self.intent_manager.Reset_Behavior()
    

    def Render_Attacking_Symbol(self, surf, offset = (0,0)):
        if self.charge < 0:
            return
        exclamation_mark = self.game.assets['exclamation_mark'][0]
        
        normalized_charge = min(self.charge / self.max_weapon_charge, 1)
        alpha_value = int(50 + (normalized_charge * (255 - 50)))

        exclamation_mark.set_alpha(alpha_value)
        surf.blit(exclamation_mark, (self.rect().left - offset[0], self.rect().top - offset[1] - self.attack_symbol_offset))