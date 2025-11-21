from scripts.entities.items.loot.curse.cursed_loot import Cursed_Loot
import pygame
from scripts.engine.keys.keys import keys

class Black_Coin(Cursed_Loot):
    def __init__(self, game, type, pos, effect_power, value):
        super().__init__(game, keys.black_coin, pos, effect_power, value)
        self.update_cooldown = 0
        self.gold_IDs = {}
        self.description = 'Increases gold\nand damage\ntaken'


    def Update(self, delta_time):
        if self.update_cooldown:
            self.update_cooldown -= delta_time
        else:
            self.update_cooldown = 1.6
            self.Check_Loot_In_Inventory()
            
            
        return super().Update(delta_time)
    
    def Check_Loot_In_Inventory(self):
        inventory_loot = self.game.inventory.item_inventory.Find_Loot()

        for item in inventory_loot:
            if item.sub_category != keys.loot:
                print("WRONG Item type added to Recipe Scroll", item)
                continue

            if item.ID in self.gold_IDs.keys():
                self.Check_For_Gold_Change(item)
                continue
                


            
            if item.loot_type != keys.gold:
                continue

            # Item is verified to be a potion
            item.Increase_Amount(item.amount // 4) 
            self.gold_IDs[item.ID] = item.amount

    # Check if the item amount has changed and update the gold accordingly
    def Check_For_Gold_Change(self, item):
        change = item.amount - self.gold_IDs[item.ID]
        if change <= 0:
            return
        item.Increase_Amount(change // 4) 
        self.gold_IDs[item.ID] = item.amount


    def Place_Down(self):
        self.Delete_Item()