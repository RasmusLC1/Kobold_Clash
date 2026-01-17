from scripts.entities.items.item import Item
from scripts.entities.items.weapons.weapon_functions.charge_effect_weapon import Charge_Effect_Weapon
from scripts.entities.items.weapons.weapon_functions.attack_effect_weapon import Attack_Effect_Weapon
from scripts.entities.items.weapons.weapon_functions.player_weapon_attack import Player_Weapon_Attack
from scripts.entities.items.weapons.weapon_functions.enemy_weapon_attack import Enemy_Weapon_Attack
from scripts.entities.items.weapons.weapon_functions.damage_handler_weapon import Damage_Handler_Weapon
from scripts.entities.items.weapons.weapon_functions.gem_handler import Gem_Handler
from scripts.entities.textbox.weapon_textbox import Weapon_Textbox
import pygame
import math
import random
from scripts.engine.keys.keys import keys

class Weapon(Item):
    def __init__(self, game, pos, type, damage, speed, range, max_charge_time, weapon_class, effect = 'slash', attack_types = ['cut'], size = (16, 16), add_to_tile = True, max_animation = 0, amount = 1, max_amount = 1, durability = 100, max_durability = 100):
        self.speed = max(1, 10 - speed) # Speed of the weapon
        self.range = range # Range of the weapon
        self.damage = damage
        self.entity = None # Entity that holds the weapon
        self.active_attack_type = '' # The currently active attack type
        self.attack_types = attack_types # Different kinds of attacks, like cutting and stabbing
        self.in_inventory = False # Is the weapon in an inventory
        self.equipped = False # Is the weapon currently equipped and can be used to attack

        self.flip_x = False

        self.wall_hit = False
        

        self.rotate = 0 # Rotation value of weapon
        self.nearby_enemies = [] # Nearby enemies that the weapon can interact with
        self.nearby_decoration = [] # Nearby decoration that the weapon can interact with
        # Can be expanded to damaged or dirty versions of weapons later
        self.weapon_class = weapon_class # Determines how it's wielded, one or two hand, bow, etc
        self.charge_time = 0  # Tracks how long the button is held
        self.max_charge_time = max_charge_time  # Maximum time to fully charge
        self.is_charging = False  # Tracks if the player is charging
        self.special_attack = 0 # special attack counter
        self.special_attack_active = False # Check if weapon is special attacking
        self.entities_hit = [] # Index of entities hit by weapon in attack

        self.weapon_cooldown = 0
        self.weapon_cooldown_max = 50 # How fast the weapon can attack

        self.delete_timer = 0 # time before weapon is deleted

        self.entity_attack_type = None # Used to determine if the weapon is being used by enemy or player
        self.damage_handler = Damage_Handler_Weapon(self, effect, damage)
        self.charge_effect_handler = Charge_Effect_Weapon(game, self)
        self.attack_effect_handler = Attack_Effect_Weapon(game, self)
        self.gem_handler = Gem_Handler(self)
        super().__init__(game, type, keys.weapon, pos, size, amount=amount, max_amount=max_amount, add_to_tile=add_to_tile, max_animation = max_animation, durability=durability, max_durability=max_durability)

    def Save_Data(self):
        if self.entity:
            if self.entity.category == keys.enemy:
                return
        super().Save_Data()
        
        self.saved_data['damage'] = self.damage_handler.damage
        self.saved_data[keys.speed] = self.speed
        self.saved_data['range'] = self.range
        self.saved_data['in_inventory'] = self.in_inventory
        self.saved_data['equipped'] = self.equipped
        self.saved_data['rotate'] = self.rotate
        self.saved_data['special_attack'] = self.special_attack
        

    
    def Load_Data(self, data):
        super().Load_Data(data)
        self.speed = data[keys.speed]
        self.range = data['range']
        self.in_inventory = data['in_inventory']
        self.equipped = data['equipped']
        self.rotate = data['rotate']
        self.special_attack = data['special_attack']
   
    # General Update function, handles setting the attack and general logic
    def Update(self, delta_time, offset = (0,0)):
        super().Update(delta_time)
        self.Special_Attack()
        self.Update_Delete_Countdown()
        if not self.entity:
            return False
        
        self.Set_Weapon_Charge(offset)
        return True

 
    # Update the attack logic
    def Update_Attack(self, delta_time):
        if not self.entity_attack_type:
            return False
        
        if self.entity_attack_type.Update_Attack(delta_time):
            self.Delete_Item()
            return
        self.Attack_Align_Weapon()

    # Initialise the attack and reset attack values
    def Set_Attack(self):
        if not self.entity_attack_type:
            return False
        
        if not self.entity_attack_type.Set_Attack():
            return False
        
        # Handle animations internally in weapon
        self.Set_Attack_Type()
        self.Set_Charge_Time(0)  # Reset charge time
        self.wall_hit = False
        self.attack_effect_handler.Init_Attack_Effect_Animation()
        return True
    
            
    def Set_Attack_Type(self):
        self.active_attack_type = random.choice(self.attack_types)


    # Check tile logic for wall collision
    def Check_Tile(self, new_pos):
        pos = (int(new_pos[0]) // self.game.tilemap.tile_size, int(new_pos[1]) // self.game.tilemap.tile_size) 
        tile = self.game.tilemap.Current_Tile(pos)
        if not tile:
            return True
        if not self.wall_hit and 'wall' in tile.sub_type:
            self.wall_hit = True
            self.Spawn_Spark()
            return False
        
        return True
    

    def Set_Rotation(self):
        if self.entity.category == keys.enemy:
            self.Point_Towards_Mouse_Enemy()
        else:
            self.Point_Towards_Mouse_Player() 

  

    # Handle weapon charging, triggers attack when full
    def Set_Weapon_Charge(self, offset = (0, 0)):
        if self.weapon_cooldown:

            self.weapon_cooldown = max(0, self.weapon_cooldown - 1)
            return
        self.Charge_Player_Or_Enemy()
        
        if self.Check_Charge():
            return
        
        self.Determine_Attack_Type(offset)


    def Determine_Attack_Type(self, offset):
        # If the button is released quickly
        if self.charge_time > 0 and self.charge_time <= 20:
            self.Set_Attack()  # Trigger the attack
            self.Reset_Weapon_Charge()
            return
        
        # Trigger special attack if mouse if held for > 20 frames
        elif self.charge_time >= self.max_charge_time:
            self.Set_Special_Attack(offset)
            self.Reset_Weapon_Charge()
            return
        
        # Resetting weapon if no special attack
        elif self.charge_time >= 20:
            self.Reset_Weapon_Charge()
    

    def Reset_Weapon_Charge(self):
        self.charge_time = 0  # Reset the charge time
        self.weapon_cooldown = self.weapon_cooldown_max
        return

    def Check_Charge(self):
        if not self.is_charging:
            return False
        
        # Slow the entity whilst charging weapon
        self.entity.Reduce_Movement(4)
        # Increase charge time while holding the button
        self.charge_time += 1
        if self.charge_time >= self.max_charge_time:
            self.charge_time = self.max_charge_time  # Cap the charge time
        return True
   
    def Charge_Player_Or_Enemy(self):
        try:
            if keys.enemy == self.entity.category:
                self.Set_Charging_Enemy()
            
            elif keys.player == self.entity.type:
                self.Set_Charging_Player()
        except TypeError as e:
            print(f"Entity neither enemy nor player: {e}")


     # Initialise special attack
    def Set_Special_Attack(self, offset = (0, 0)):
        if not self.entity:
            return
        self.entity.Attack_Direction_Handler()
        self.Set_Block_Direction()
        self.special_attack = min(self.charge_time, self.max_charge_time)
        self.Set_Rotation()
        self.special_attack_active = True


    def Reset_Special_Attack(self):
        if not self.special_attack_active:
            return
        self.rotate = 0
        self.special_attack_active = False


    # Initialise the charging of the weapon
    def Set_Charging_Player(self):
        # Detect if the player is holding down the button
        self.is_charging = self.game.mouse.hold_down_left

    # Damage Entity
    def Entity_Hit(self, entity):
        return self.damage_handler.Entity_Hit(entity)
    
    def Decoration_Hit(self, decoration):
        return self.damage_handler.Decoration_Hit(decoration)
    
    # TODO: Better calculation
    def Calculate_Value(self):
        return self.value * self.damage

    def Set_Description(self):
        
        self.description = (
                            f"Damage {self.damage_handler.Get_Damage()}\n"
                            f"speed {self.speed}\n"
                            f"range {self.range}\n"
                            f"Dur {self.durability} / {self.max_durability}\n"
                            f"Gemslots {self.gem_handler.max_gems}\n"
                            f"{self.Calculate_Value()} {keys.gold}\n"
                        )

    # Set the attack direction   
    def Set_Block_Direction(self):
        self.entity.Attack_Direction_Handler()
        if not self.entity.attack_direction[0] or not self.entity.attack_direction[1]:
            return
        # self.entity.attack_direction = pygame.math.Vector2(self.entity.attack_direction[0], self.entity.attack_direction[1])
        self.entity.attack_direction.normalize_ip()
        return

    # Point the weapon towards the mouse
    def Point_Towards_Mouse_Enemy(self):
        # Get the direction using attack_direction
        dx = self.entity.pos[0] + self.entity.attack_direction[0] * 100 - self.entity.pos[0]
        dy = self.entity.pos[1] + self.entity.attack_direction[1] * 100 - self.entity.pos[1]

        # Calculate the angle in degrees
        self.rotate = math.degrees(math.atan2(dx, dy))
    

    # Point the weapon towards the mouse
    def Point_Towards_Mouse_Player(self):
        if self.entity.category != keys.player:
            return
        # Get the direction using attack_direction
        dx = self.game.mouse.mpos[0] - self.entity.pos[0]
        dy = self.game.mouse.mpos[1] - self.entity.pos[1]
        # Calculate the angle in degrees
        self.rotate = abs(math.degrees(math.atan2(dx, dy)))

    def Get_Dominant_Effect(self):
        return self.damage_handler.Get_Dominant_Effect()

    # Handle deletion of items when enemies drop weapons, don't want them to linger forever
    def Update_Delete_Countdown(self):
        if not self.delete_countdown:
            return
        self.delete_countdown = max(0, self.delete_countdown - 1)
        if not self.delete_countdown:
            self.game.item_handler.Remove_Item(self, True)


    def Set_Delete_Countdown(self, delete_countdown = 0.2):
        self.delete_countdown = delete_countdown

    def Set_Damage(self, damage_type, damage):
        self.damage_handler.Set_Damage(damage_type, damage)
        self.charge_effect_handler.Set_Charge_Effect()

    # Reset the attack charge
    def Reset_Charge(self):
        self.is_charging = 0
        self.charge_time = 0
        return

    
    def Set_Entity(self, entity):
        self.entity = entity
        if not entity:
            return
        
        self.Set_Entity_Attack_Type(entity.type)
        
    
    def Set_Entity_Attack_Type(self, type):
        if type == keys.player:
            self.entity_attack_type = Player_Weapon_Attack(self.game, self)
        else:
            self.entity_attack_type = Enemy_Weapon_Attack(self.game, self)

    def Delete_Item(self):
        self.gem_handler.Remove_Entity_Effect_Gems()
        if self.entity and self.entity.type == keys.player:
            self.game.player.weapon_handler.Check_If_Weapon_Should_Be_Removed(self)
        return super().Delete_Item()

   
    # TODO: Write charge logic for enemy
    def Set_Charging_Enemy(self):
        self.is_charging = self.entity.charge


    def Set_Charge_Time(self, state):
        self.charge_time = state

    def Special_Attack(self):
        pass


    # Align the weapon with the attacking entity while attacking
    def Attack_Align_Weapon(self):
        pass
    
    
    # Takes the entity's sprite type and applies it to weapon
    def Set_Equipped_Sprite(self):
        self.sub_type = self.type + '_' + self.entity.animation_handler.action
        self.Set_Sprite()

    # Responsible for calculating offset and centering the weapon 
    def Calculate_Image_Rect(self, image, offset):
        flip_offset_x = 0
        player_action = self.entity.animation_handler.action
        if not self.flip_x:
            flip_offset_x = 10
        if 'attack' in player_action:
            flip_offset_x = 5
            if self.flip_x:
                flip_offset_x = 20

        flip_offset_y = 0
        if 'up' in player_action:
            flip_offset_y = 5
        image_size = image.get_size()
        image_rect = image.get_rect(center=(self.pos[0] - offset[0]  - flip_offset_x + image_size[0] // 2,
                                        self.pos[1] - offset[1]  - flip_offset_y + image_size[1] // 2))

        return image_rect
    
    def Set_Animation(self, animation_num):
        self.animation = animation_num
        self.Set_Equipped_Sprite()

    # Render the weapon in player's hand 
    def Render_Equipped(self, surf, offset=(0, 0)):
        if not self.entity:
            return
        self.Set_Equipped_Sprite()
        weapon_image = self.entity_image.copy()
        self.flip_x = self.entity.animation_handler.flip[0]


        image_rect = self.Calculate_Image_Rect(weapon_image, offset)

        surf.blit( pygame.transform.flip(weapon_image, self.flip_x, False), image_rect)
        self.attack_effect_handler.Render_Attack_Effect(surf, image_rect, self.flip_x)
        self.charge_effect_handler.Render_Charge_Effect(surf, offset)
    

    # Render the weapon in entity's hand
    def Render_Equipped_Enemy(self, surf, offset=(0, 0)):
        alpha_value = max(0, min(255, self.active)) 

        if not alpha_value:
            return

        self.Update_Dark_Surface_Enemy(alpha_value)

        if not self.rendered_image:
            self.rendered_image = self.entity_image.copy()
        surf.blit(
            pygame.transform.flip(self.rendered_image, False, False),
                                  (self.pos[0] - offset[0], self.pos[1] - offset[1]))
    
    # Updates the dark surface for enemies
    def Update_Dark_Surface_Enemy(self, alpha_value):
        if not self.render_needs_update:
            return
        self.rendered_image = self.entity_image.copy()
        self.rendered_image.set_alpha(alpha_value)


         # Create a darkening surface that is affected by darkness
        dark_surface = pygame.Surface(self.rendered_image.get_size(), pygame.SRCALPHA).convert_alpha()
        dark_surface.fill((self.light_level, self.light_level, self.light_level, 255))  

        self.rendered_image.blit(dark_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)


    def Render_Inventory(self, surf, pos, size):
        self.gem_handler.Render_Gems_Inventory(surf, pos, size)
        return super().Render_Inventory(surf, pos, size)
    
    # Used to reset weapon when equipped by enemy
    def Pickup_Reset_Weapon(self, entity):
        self.entity = entity
        self.in_inventory = True
        self.picked_up = True
        self.rotate = 0
        self.light_level = 10
    
    # Prevent textbox when carried by enemy
    def Update_Text_Box(self, hitbox_1, hitbox_2):
        if self.entity:
            if self.entity.category == keys.enemy:
                return
        return super().Update_Text_Box(hitbox_1, hitbox_2)


    def Set_Equip(self, state, entity):
        self.Set_Entity(entity)
        self.equipped = state
        if state:
            self.render = False
        else:
            self.render = True

    def Set_Equipped_Position(self, direction_y):
        if not self.entity:
            return
        if direction_y < 0:
            self.Move((self.entity.pos[0] - 5 , self.entity.pos[1]))
        else:
            self.Move((self.entity.pos[0] + 5 , self.entity.pos[1]))

    def Place_Down(self):
        self.entity = None
        return super().Place_Down()

    # Only used for Player Weapons
    def Equip(self):
        self.Set_Equip(True, self.game.player)
        self.Activate_Gem_Effect()
        self.game.player.Set_Active_Weapon(self)
        self.animation = 0 # Reset animation when equipped

    def Unequip(self):
        self.Set_Equip(False, None)


    def Spawn_Spark(self):
        self.game.particle_handler.Activate_Particles(random.randint(2, 5), keys.spark_particle, self.rect().center, random.uniform(1, 1.5))


    def Add_Gem_Slot(self, amount):
        self.gem_handler.Increase_Max_Gems(amount)

    def Add_Gem(self, gem):
        return self.gem_handler.Add_Gem(gem)

    # Set the player effects for gem
    def Activate_Gem_Effect(self):
        self.gem_handler.Set_Entity_Effect_Gems()

    # Disable the player effects for gem
    def Disable_Gem_Effect(self):
        self.gem_handler.Remove_Entity_Effect_Gems()

    def Increase_Range(self, amount):
        self.range += amount

    def Increase_Speed(self, amount):
        self.Set_Description()
        self.range += amount


    def Decrease_Range(self, amount):
        self.range -= amount

    def Decrease_Speed(self, amount):
        self.Set_Description()
        self.range -= amount


    
    def Set_Text_Box(self):
        self.text_box = Weapon_Textbox(self)