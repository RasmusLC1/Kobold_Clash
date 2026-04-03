from scripts.entities.moving_entities.moving_entity import Moving_Entity
from scripts.entities.textbox.enemy_textbox import Enemy_Textbox
from scripts.entities.decoration.shared.bones.bones import Bones 
from scripts.entities.moving_entities.enemies.behavior.intent_manager import Intent_Manager
from scripts.engine.keys.keys import keys
from scripts.entities.moving_entities.enemies.attribute_distributor import Attribute_Distributor

import math
import pygame
import random


class Enemy(Moving_Entity):

    # Factory method
    intent_manager_class = Intent_Manager  # Default intent manager

    def __init__(self, game, pos, type, sub_category, idle_animation, run_animation, attack_animation, size = (32, 32), attack_speed = (0.5, 0.8), path_finding_strategy = keys.standard, default_range = keys.direct, is_elite = False):

        base_stats = Attribute_Distributor.Get_Enemy_Data(type, game.depth, is_elite)    
        self.max_weapon_charge = base_stats.get(keys.max_weapon_charge)
        self.soul_value = base_stats.get(keys.souls)
        self.aggression = base_stats.get(keys.aggression)

        super().__init__(game, str(type), keys.enemy, pos, size,
                         base_stats.get(keys.health),
                         base_stats.get(keys.strength),
                         base_stats.get(keys.speed),
                         base_stats.get(keys.agility),
                         base_stats.get(keys.intelligence),
                         base_stats.get(keys.stamina),
                         sub_category)
        
        self.animation_handler.Set_Animation_Num_Max(keys.run ,run_animation)
        self.animation_handler.Set_Animation_Num_Max(keys.idle ,idle_animation)
        self.animation_handler.Set_Animation_Num_Max(keys.attack, attack_animation)
        self.animation_handler.Set_Animation('running')
        self.alert_cooldown = 0
        self.active_weapon = None
        self.target = self.game.player.pos # Default target is set to player


        self.distance_to_player = 9999 # Distance to player
        self.charge = 0 # Determines when the enemy attacks
        self.movement_strategy = default_range # Attack strategy that the enemy utalises
        
        self.attack_distance  = self.size[0] * 2 # Distance that the enemy can attack from
        self.distance_calculation_cooldown = 0 # Time between checking target distance


        self.locked_on_target = 0 # If the enemy is locked onto a target, then it will not switch based on clatter

        self.attack_symbol_offset = 20
        self.health_bar = self.game.assets[keys.health_bar]

        self.intent_manager = self.intent_manager_class(game, self, attack_speed, path_finding_strategy)

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
        self.Reset_Max_Speed()
        self.Calculate_Distance_To_Player(delta_time)
        self.intent_manager.Update_Intent(delta_time)
        movement = self.direction
        super().Update(tilemap, delta_time, movement)

        self.Set_Direction_Holder()

        self.Update_Alert_Cooldown(delta_time)
        self.Update_Locked_On_Target(delta_time)


    def Set_Direction_Holder(self):
        if self.direction_x or self.direction_y:
            self.direction_x_holder = self.direction_x
            self.direction_y_holder = self.direction_y


    def Calculate_Distance_To_Player(self, delta_time):
        if self.distance_calculation_cooldown > 0:
            self.distance_calculation_cooldown = max(0, self.distance_calculation_cooldown - delta_time)
            return
         
        max_distance_cooldown = random.uniform(0.4, 0.6) # randomise time to prevent simulationious updates
        self.distance_calculation_cooldown = max_distance_cooldown
        
        player_pos = self.game.player.pos
        self.distance_to_player = math.sqrt((player_pos[0] - self.pos[0]) ** 2 + (player_pos[1] - self.pos[1]) ** 2)

    def Reset_Charge(self):
        self.charge = 0

    def Set_Charge_To_Max(self):
        self.charge = self.max_weapon_charge
    
    def Entity_Collision_Detection(self, tilemap):
        colliding_entity = super().Entity_Collision_Detection(tilemap)

        if colliding_entity:
            if colliding_entity.type == 'player':
                # Prevent further movement towards the player by stopping the enemy's movement
                self.direction = (0, 0)
                return colliding_entity

            # Collision logic for other entities
            collision_vector = pygame.math.Vector2(self.pos[0] - colliding_entity.pos[0],
                                                self.pos[1] - colliding_entity.pos[1])
            if collision_vector.length() > 0:
                collision_vector = collision_vector.normalize()
                direction_vector = pygame.math.Vector2(self.direction)
                reflected_direction = direction_vector.reflect(collision_vector)

                if self.Future_Rect(reflected_direction).colliderect(self.game.player.rect()):
                    self.direction = (0, 0)

                    return self.game.player

                self.direction = (reflected_direction.x, reflected_direction.y)

        return None
    
    def Attack(self, delta_time):
        # Check if the player is invisible
        if self.game.player.effects.invisibility.effect:
            return False
        
        self.charge = min(self.max_weapon_charge, self.charge + delta_time)

        return True


    def Trigger_Attack(self):
        self.Set_Target()
        self.active_weapon.Set_Attack()
        self.Reset_Charge()

    def Set_Target(self, pos = None):
        if not pos:
            pos = self.game.player.pos
        return super().Set_Target(pos)
    
    def Check_Attack_Direction(self, attack_direction):
        if not attack_direction:
            self.Set_Target()
            attack_direction = self.target

        return attack_direction

    def Set_Attack_Direction(self):
        if not self.charge > 0:
            self.attack_direction = (0, 0)
            return
        super().Set_Attack_Direction()
        
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
        if direction.length() > 0:
            direction.normalize_ip()
        self.direction = direction


    def Update_Locked_On_Target(self, delta_time):
        if not self.locked_on_target:
            return
        self.locked_on_target = max(0, self.locked_on_target - delta_time)
    
    def Set_Locked_On_Target(self, value):
        self.locked_on_target = value
        
    def Damage_Taken(self, damage, effect = (keys.slash, 0), direction = (0, 0)):
        self.Spawn_Damaged_Particles()
        if not super().Damage_Taken(damage, effect, direction):
            return False
        
        self.Delete()
        return True

    
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


    def Set_Action(self,  movement = None):
        if self.distance_to_player > 300 :
            return
        
        if self.charge > 0:
            self.animation_handler.Set_Animation(keys.attack)
        elif self.frame_movement:
            self.animation_handler.Set_Animation('running')
        else:
            self.animation_handler.Set_Animation('idle')


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

    def Trap_Collision_Handler(self):
        for trap in self.nearby_traps:
            if self.rect().colliderect(trap.rect()):
                # Run away in in the same direction the enemy was moving previously
                # Use min and max to prevent it teleporting
                if self.direction_x_holder < 0:
                    self.direction_x = max(-0.4, self.direction_x_holder * 4)
                else:
                    self.direction_x = min(0.4, self.direction_x_holder * 4)

                if self.direction_y_holder < 0:
                    self.direction_y = max(-0.4, self.direction_y_holder * 4)
                else:
                    self.direction_y = min(0.4, self.direction_y_holder * 4)

                self.direction = (self.direction_x, self.direction_y)
            else:
                # Check if the enemy will collide soon, if yes redirect in the opposite direction
                if self.Future_Rect(self.direction).colliderect(trap.rect()):
                    self.direction_x *= -1
                    self.direction_y *= -1
                    self.direction = (self.direction_x, self.direction_y)
                    break

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
            return
        self.Render_Health_Bar(surf, offset)
        self.Render_Attacking_Symbol(surf, offset)

    

    def Render_Health_Bar(self, surf, offset = (0,0)):
        health_fraction = self.health / self.max_health

        # Map the fraction to an index from 0 to 9 (assuming 10 total images)
        health_index = max(-1, min(int((1 - health_fraction) * 9), 9))  # Invert fraction and scale to index range
        # Correct potential rounding issues at full health
        if self.health == self.max_health:
            health_index = 0

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
    

    def Render_Attacking_Symbol(self, surf, offset = (0,0)):
        if self.charge < 0:
            return
        exclamation_mark = self.game.assets['exclamation_mark'][0]
        
        normalized_charge = min(self.charge / self.max_weapon_charge, 1)
        alpha_value = int(50 + (normalized_charge * (255 - 50)))

        exclamation_mark.set_alpha(alpha_value)
        surf.blit(exclamation_mark, (self.rect().left - offset[0], self.rect().top - offset[1] - self.attack_symbol_offset))

