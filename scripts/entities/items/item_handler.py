import pygame
import random
import traceback
from scripts.engine.keys.keys import keys
from scripts.entities.items.weapons.weapon_handler import Weapon_Handler
from scripts.entities.items.runes.rune_handler import Rune_Handler
from scripts.entities.items.loot.loot_handler import Loot_Handler

class Item_Handler():
    def __init__(self, game):
        self.game = game
        self.items = []
        self.nearby_items = []
        self.nearby_item_cooldown = 0
        self.saved_data = {}
        
        self.weapon_handler = Weapon_Handler(self.game, self)
        self.loot_handler = Loot_Handler(self.game, self)
        self.rune_handler = Rune_Handler(self.game, self)

    def Save_Item_Data(self):
        for item in self.items:
            item.Save_Data()
            self.saved_data[item.ID] = item.saved_data

    def Load_Data(self, data):
        for ID, item_data in data.items():
            if item_data:
                self.Load_Item_From_Data(item_data)

    def Load_Item_From_Data(self, item_data):
        try:
            type = item_data[keys.type]
            pos = item_data[keys.pos]
            item = None
            
            sub_cat = item_data.get('sub_category')
            if sub_cat == keys.weapon:
                item = self.weapon_handler.Weapon_Spawner(type, pos[0], pos[1], data=item_data)
            elif sub_cat == keys.loot:
                loot_type = item_data[keys.loot_type]
                item = self.loot_handler.Spawn_Loot_Type(loot_type, pos, item_data)
            elif sub_cat == keys.rune:
                item = self.rune_handler.Load_Data(item_data)
                
            return item
        except Exception as e:
            print("DATA WRONG ITEM HANDLER", item_data, e)

    def Clear_Items(self):
        self.items.clear()
        self.nearby_items.clear()
        self.saved_data.clear()
        self.rune_handler.Clear_Runes()

    def Initialise(self):
        for gold in self.game.tilemap.extract([(keys.gold, 0)].copy()):
            gold_item = self.loot_handler.Spawn_Loot_Type(keys.valuable, gold[keys.pos], type=keys.gold)
            if gold_item:
                self.Add_Item(gold_item)
        self.rune_handler.Initialise_Runes()
        
    def Add_Item(self, item):
        if item not in self.items:
            self.items.append(item)

    def Remove_Item(self, item, delete_item=False):
        if item in self.items:
            self.items.remove(item)
        self.game.entities_render.Remove_Entity(item)
        self.game.tilemap.Remove_Entity_From_Tile(item.tile, item.ID)
        if delete_item:
            item.Delete()

    def Update(self, delta_time):
        self.Check_Keyboard_Input()
        
        if self.Update_Nearby_Items_Cooldown(delta_time):
            self.nearby_items.clear()
            self.nearby_items = self.Find_Nearby_Item(self.game.player.pos, 3)
        
        # FIXED: Iterate backward to prevent list mutation skips
        for i in range(len(self.items) - 1, -1, -1):
            item = self.items[i]
            
            item.Update_Delete_Cooldown(delta_time)
            
            # Fixed check for internal object expiration status
            if getattr(item, 'is_dead', False):
                self.Remove_Item(item, True)
                continue

            if item.picked_up:
                self.items.remove(item)
                continue

            self.Throw_Projectile(item, delta_time)

        self.rune_handler.Update(delta_time)

    def Throw_Projectile(self, item, delta_time):
        if not item.type or not item.is_projectile or item.special_attack:
            return
        if not item.entity:
            return
            
        if item.shoot_speed and item.entity.category == keys.enemy and not item.delete_countdown:
            item.Set_Delete_Countdown(0.2)
            return
            
        try:
            if item in self.items:
                item.Shoot(delta_time)
        except Exception as e:
            traceback.print_exc()
            if not item.type:
                self.Remove_Item(item, True)

    def Check_Keyboard_Input(self):
        if self.game.keyboard_handler.is_key_pressed(pygame.K_e):
            if self.Pick_Up_Items(2):
                self.game.keyboard_handler.Set_E_Key(False)

    def Pick_Up_Items(self, distance) -> bool:
        nearby_items = self.Find_Nearby_Item(self.game.player.pos, distance)
        # Clean out stale references before processing sorting operations
        nearby_items = [item for item in nearby_items if not item.picked_up]
        if not nearby_items:
            return False
            
        player_pos = self.game.player.pos
        nearby_items.sort(key=lambda item: (player_pos[0] - item.pos[0]) ** 2 + (player_pos[1] - item.pos[1]) ** 2)
        return nearby_items[0].Pick_Up()

    def Find_Nearby_Item(self, entity_pos, max_distance):
        if max_distance <= 5:
            return self.game.tilemap.Search_Nearby_Tiles(max_distance, entity_pos, keys.item)
        return self.Search_For_Nearby_Items(entity_pos, max_distance)

    def Search_For_Nearby_Items(self, entity_pos, max_distance):
        nearby_items = []
        max_dist_sq = max_distance * max_distance
        for item in self.items:
            dx = entity_pos[0] - item.pos[0]
            dy = entity_pos[1] - item.pos[1]
            if (dx * dx + dy * dy) < max_dist_sq:
                nearby_items.append(item)
        return nearby_items

    def Update_Nearby_Items_Cooldown(self, delta_time):
        if self.nearby_item_cooldown > 0:
            self.nearby_item_cooldown = max(0, self.nearby_item_cooldown - delta_time)
            return False
        self.nearby_item_cooldown = 0.5
        return True

    # Sub-component proxy passes
    def Spawn_Rune(self, pos, type=None, rarity_value=None): return self.rune_handler.Loot_Spawner(pos, type, rarity_value)
    
    def Remove_Rune_From_Active_Runes(self, rune): return self.rune_handler.Remove_Rune_From_Active_Runes(rune)
    
    def Get_Active_Runes(self): return self.rune_handler.Get_Active_Runes()
    
    def Replace_Rune_In_Inventory(self, r, n): return self.rune_handler.Replace_Rune_In_Inventory(r, n)
    
    def Check_For_Damage_Rune(self): return self.rune_handler.Check_If_Player_Has_Damage_Runes()
    
    def Spawn_Weapon(self, pos, type=None): return self.weapon_handler.Weapon_Spawner(type, pos[0], pos[1]) if type else self.weapon_handler.Spawn_Random_Weapon(pos)
    
    def Spawn_Arrow_For_Trap(self, pos): return self.weapon_handler.Spawn_Arrow_For_Trap(pos)
    
    def Get_Gems_For_Weapon(self, value): return self.loot_handler.Get_Gems_For_Weapon(value)
    
    def Check_If_Loot_Is_Affordable(self, t, r): return self.loot_handler.Check_If_Loot_Is_Affordable(t, r)
    
    def Spawn_Item_By_Type(self, cat, pos, type=None, rarity=0): self.loot_handler.Spawn_Loot_Type(cat, pos, type=type, rarity_value=rarity)