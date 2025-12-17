import random
import math
import pygame
from scripts.entities.entities import PhysicsEntity
from scripts.engine.keys.keys import keys

class Item(PhysicsEntity):
    def __init__(self, game, type, sub_category, pos, size = (16, 16), amount = 1, add_to_tile = True, rarity_value = 100, max_amount=1, max_animation = 0, durability = 1, max_durability = 1):
        super().__init__(game, type, keys.item, pos, size, sub_category)
        self.game = game
        self.sub_type = type
        self.rarity = self.Calculate_Rarity(rarity_value) # rarity used for loot defaults to common



        self.picked_up = False
        self.clicked = False # Used for if the item is active
        self.move_inventory_slot = False # Check for if the item is being moved to a new inventory slot
        self.inventory_type = None
        self.inventory_index = None
        self.floor_size = size # Used to upscale item for inventory
        self.inventory_size = (32,32) # Used to upscale item for inventory
        self.activate_cooldown = 0
        self.animation_cooldown = 0
        self.amount = int(min(max_amount, int(amount))) # Cap the amount
        self.max_amount = max_amount
        self.max_animation = max_animation
        self.animation_cooldown_max = 0.8

        self.animation = random.randint(0, self.max_animation)
        self.nearby_entities = []
        self.delete_countdown = 0
        self.value = int(rarity_value) # Placeholder gold value, counts per item in stack

        # Durability logic
        self.durability = durability
        self.max_durability = max_durability
        self.last_durability_step = 999  # Used for tracking decrements accurately so it does not skip a percentage
        self.durability_bar_image = None
        self.Update_Durability_Bar()


        self.is_projectile = False
        self.Set_Sprite()
        self.broken_rendering_counter = 0 # Counter if it hits 10, delete item since something is wrong
        if add_to_tile:
            self.game.tilemap.Add_Entity_To_Tile(self.tile, self)


    def Save_Data(self):
        super().Save_Data()
        self.saved_data['sub_type'] = self.sub_type
        self.saved_data['sub_category'] = self.sub_category
        self.saved_data['durability'] = self.durability
        self.saved_data['picked_up'] = self.picked_up
        self.saved_data['inventory_type'] = self.inventory_type
        self.saved_data['amount'] = self.amount
        self.saved_data['inventory_index'] = self.inventory_index

    
    def Load_Data(self, data):
        super().Load_Data(data)
        self.sub_type = data['sub_type']
        self.sub_category = data['sub_category']
        self.durability = data['durability']
        self.picked_up = data['picked_up']
        self.inventory_type = data['inventory_type']
        self.amount = data['amount']
        self.inventory_index = data['inventory_index']
        self.Set_Description()
        
    def Update(self, delta_time):
        self.Update_Activate_Cooldown(delta_time)

    def Update_In_Inventory(self):
        pass

    def Calculate_Value(self):
        return self.amount * self.value
    
    def Activate(self):
        if self.activate_cooldown:
            return False
        
        self.activate_cooldown = 1
        return True

    def Update_Activate_Cooldown(self, delta_time):
        if self.activate_cooldown <= 0:
            return
        self.activate_cooldown = max(0, self.activate_cooldown - delta_time)

    def Set_Inventory_Index(self, index):
        self.inventory_index = index
    
    def Find_Nearby_Entities(self, distance):
        self.nearby_entities = self.game.enemy_handler.Find_Nearby_Enemies(self, distance)


    def Pick_Up(self):
        # First Check if the player is colliding with the object as this is priority
        if not self.game.inventory.Add_Item(self):
            return None
        
        self.picked_up = True
        self.Remove_Tile()

        self.game.entities_render.Remove_Entity(self)

        self.game.sound_handler.Play_Sound(keys.item_pickup, 0.4)

        self.Set_Size(self.inventory_size) # Standard loot size in inventory

        return self.game.player
        

         

    # Returns false if the item was deleted in the process of palcedown
    def Place_Down(self):
        if self.game.decoration_handler.Check_Item_Collision(self):
            return False
        self.picked_up = False
        self.in_inventory = False
        self.Set_Tile()
        self.Set_Size(self.floor_size) # Standard loot size on floor
        self.game.sound_handler.Play_Sound(keys.item_placedown, 0.2)
        return True

    def Update_Animation(self, delta_time):
        if self.animation_cooldown > 0:
            self.animation_cooldown = max(0, self.animation_cooldown - delta_time)
        else:
            self.animation_cooldown = self.animation_cooldown_max
            self.animation = random.randint(0,self.max_animation)
            self.Set_Entity_Image()

    

    def Distance(self, start_pos, target_pos):
        return math.sqrt((start_pos[0] - target_pos[0]) ** 2 + (start_pos[1] - target_pos[1]) ** 2)
    
    def Set_Amount(self, amount):
        self.amount = min(self.max_amount, amount)

    # Setting the initial sprite type from assets, only called during initial setup
    def Set_Sprite(self):
        try:
            self.sprite = self.game.assets[self.sub_type]
            self.Set_Entity_Image()
        except Exception as e:
            print("SETTING ITEM SUBTYPE FAILED", self.sub_type, self.type)
            self.Delete_Item()

    # Setting the item image and scaling it
    def Set_Entity_Image(self):
        try:
            self.entity_image = self.sprite[self.animation].convert_alpha()
        except Exception as e:
            print(f'SET Entity image failed {e}', self.type, self.pos, self.animation, self.max_animation, self.size, self.entity_image, self.sprite)

    
    def Increase_Amount(self, amount):
        self.amount = int(min(self.max_amount, self.amount + int(amount)))

    def Decrease_Amount(self, amount):
        self.amount = max(0, self.amount - amount)
        if self.amount <= 0:
            self.durability = 0

    def Increase_Max_Amount(self, amount):
        self.max_amount = int(self.max_amount + int(amount))

    def Decrease_Max_Amount(self, amount):
        self.max_amount = max(1, self.max_amount - amount)

    def Add_Gem_Slot(self, amount):
        pass

    def Set_Inventory_Type(self, inventory_type):
        self.inventory_type = inventory_type
    
    # Check for out of bounds, return true if valid, else false
    def Move_Legal(self, mouse_pos, player_pos, tilemap, offset = (0,0)):
        # Check if distance is legal, update to account for player strength later
        if self.Distance(player_pos, mouse_pos) < 80:
            
            for rect in tilemap.physics_rects_around(mouse_pos):
                if self.rect().colliderect(rect):
                    return False
            return True
        
        else:
            return False
    
    # Update position
    def Move(self, new_pos):
        self.pos = list(new_pos)

# DURABILITY LOGIC
    def Increase_Durability(self, amount):
        self.durability = max(0, min(self.max_durability, self.durability + amount))
        self.Set_Description()
        self.Update_Durability_Bar()

    def Decrease_Durability(self, amount):
        self.durability = max(0, self.durability - amount)
        self.Set_Description()
        self.Update_Durability_Bar()
    
    def Update_Durability_Bar(self):
        current_step = int((self.durability / self.max_durability) * 10)

        while self.last_durability_step > current_step:
            self.Decrease_Value(self.value // 10)
            self.last_durability_step -= 1
            self.Set_Durability_Bar_Image()

    def Set_Durability_Bar_Image(self):
        if self.max_durability <= 1:
            return

        # 10 - step maps 10 (full) to 0, and 1 (low) to 9.
        image_index = 10 - self.last_durability_step
        # Ensure the index is within the valid range [0, 9]
        image_index = max(0, min(9, image_index))
        self.durability_bar_image = self.game.assets[keys.durability_bar][image_index]

    
    def Increase_Value(self, value):
        self.value += value
        self.Set_Description()

    
    def Decrease_Value(self, value):
        self.value -= value
        self.Set_Description()

    # TODO: OPTIMISE
    def Update_Tile(self, new_pos):

        pos = (int(new_pos[0]) // self.game.tilemap.tile_size, int(new_pos[1]) // self.game.tilemap.tile_size) 
        new_tile = self.game.tilemap.Current_Tile(pos)
        if not (new_tile, self.tile):
            return
        if pos != self.tile.pos:
            self.game.tilemap.Remove_Entity_From_Tile(self.tile, self.ID)
            self.game.tilemap.Add_Entity_To_Tile(new_tile, self)
            self.tile = new_tile

    # Iterates over the thresholds until it finds one that passes
    def Calculate_Rarity(self, value):
        thresholds = [
            (90, keys.legendary),
            (70, keys.epic),
            (50, keys.rare),
            (30, keys.uncommon),
        ]
        
        for limit, rarity in thresholds:
            if value >= limit:
                return rarity
        return keys.common


    def Update_Delete_Cooldown(self, delta_time):
        if not self.delete_countdown:
            return False
        self.delete_countdown = max(0, self.delete_countdown - delta_time)

        if self.delete_countdown <= 0:
            self.Delete_Item()
        return True

    def Set_Delete_Countdown(self, time):
        self.delete_countdown = time
    
    def Delete_Item(self):
        self.game.item_handler.Remove_Item(self, True)
        self.game.inventory.Remove_Item(self)
        
    # Destroy item when damaged
    def Damage_Taken(self, damage):
        self.game.item_handler.Remove_Item(self, True)
    
    

# RENDERING LOGIC

    def Render(self, surf, offset=(0, 0)):
        if self.picked_up:
            return
        self.Render_Floor(surf, offset)

    # Render legal position
    def Render_Inventory(self, surf, pos, size):
        try:
            if not self.entity_image:
                self.Set_Entity_Image()

            item_image = pygame.transform.scale(self.entity_image, size)
            surf.blit(item_image, pos)
            
        except Exception as e:
            print(f"ITEM Render_Inventory failed {e}", self.entity_image, size, pos, self.type, self.sub_type)

        self.Render_Durability_Bar(surf, pos)

    def Render_Durability_Bar(self, surf, pos):
        try:
            if self.durability_bar_image:
                surf.blit(self.durability_bar_image, (pos[0], pos[1] + 30))
        except Exception as e:
            print(f"ITEM Render durability bar failed{e}", self.durability_bar_image, pos, self.type, self.sub_type)

    def Render_Floor(self, surf, offset=(0, 0)):
        
        if not self.Update_Light_Level():
            return
        
        self.Update_Dark_Surface()
        
        # Render the item
        if not self.rendered_image:
            self.Set_Sprite()

            if not self.rendered_image:
                
                self.broken_rendering_counter += 1
                if self.broken_rendering_counter >= 10:
                      self.Delete_Item()
                return
        surf.blit(self.rendered_image, (self.pos[0] - offset[0], self.pos[1] - offset[1]))

    def Update_Dark_Surface(self):
        if not super().Update_Dark_Surface():
            return False
        
        self.rendered_image =  pygame.transform.scale(self.rendered_image, self.floor_size)
        return True


    # Render item with fadeout if it's in an illegal position
    def Render_Out_Of_Bounds(self, player_pos, mouse_pos, surf, offset = (0,0)):
        # Calculate distance between player and mouse

        distance = max(20, 100 - self.Distance(player_pos, mouse_pos))
        entity_image =  pygame.transform.scale(self.entity_image.copy(), self.floor_size)
        
        entity_image.set_alpha(distance)

        # Render on Mouse position as the item position is not being updated
        surf.blit(entity_image, (mouse_pos[0] - offset[0], mouse_pos[1] - offset[1]))

    
    # Render item with fadeout if it's in an illegal position
    def Render_In_Bounds(self, player_pos, mouse_pos, surf, offset = (0,0)):

        entity_image =  pygame.transform.scale(self.entity_image.copy(), self.floor_size)
        
        # Render on Mouse position as the item position is not being updated
        surf.blit(entity_image, (mouse_pos[0] - offset[0], mouse_pos[1] - offset[1]))
    
    # Used to render effect when active
    def Render_Active(self, surf, offset = (0,0)):
        pass