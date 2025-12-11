from scripts.entities.items.loot.loot import Loot
from scripts.entities.items.loot.passive.ivnentory_item import Inventory_Item
from scripts.engine.keys.keys import keys

class Recipe_Scroll(Inventory_Item):
    def __init__(self, game, type, pos, effect_power, rarity_value):
        super().__init__(game, type, pos, effect_power, rarity_value)


    def Set_Description(self):
        self.description =  'Improves\nefficiency\nof potions'

    def Check_Loot_In_Inventory(self):
        inventory_loot = self.game.inventory.item_inventory.Find_Loot()

        for item in inventory_loot:
            if item.sub_category != keys.loot:
                print("WRONG Item type added to Recipe Scroll", item)
                continue
            if item.ID in self.loot_IDs:
                continue
            
            if item.loot_type != keys.potion:
                continue

            # Item is verified to be a potion
            item.Increase_Strength(self.effect_power) 
            self.loot_IDs.append(item.ID)


    def Place_Down(self):
        inventory_loot = super().Place_Down()

        if not inventory_loot:
            return False

        for item in inventory_loot:

            if item.ID not in self.loot_IDs:
                continue
            
            # Item is verified to be a potion
            if item.loot_type != keys.potion:
                continue
            
            # Decrease strength of potion
            item.Decrease_Strength(self.effect_power) 
        
        self.Delete_Item()

        return True
