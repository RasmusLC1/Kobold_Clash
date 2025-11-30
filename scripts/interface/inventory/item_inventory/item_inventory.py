from scripts.interface.inventory.base_inventory import Base_Inventory
from scripts.interface.inventory.inventory_slot import Inventory_Slot
from scripts.engine.keys.keys import keys

class Item_Inventory(Base_Inventory):

    def Setup(self):
        for i in range(9):
            (x, y) = self.Set_Inventory_Slot_Pos(i)
            inventory_slot = Inventory_Slot(self.game, (x, y), keys.item, self.size, None, i, str(i + 1))
            inventory_slot.Set_White_List([keys.weapon, 'potion', keys.loot])
            self.Add_Inventory_Slot(inventory_slot)

    def Set_Inventory_Slot_Pos(self, index):
        x = index * self.size[1] + self.game.screen_width / 2 / self.game.render_scale - 120
        y = self.game.screen_height / self.game.render_scale - 40
        return (x, y)
    

    
    # Add item to the inventory
    def Add_Item(self, item):
        # Check if an item can have more than one charge, example health potion is 3
        if self.Add_Item_To_Inventory_Slot_Merge(item):
            return True
                    
        return self.Add_Item_To_Inventory_Slot(item)

    

    # Merges items into existing slots if possible
    def Add_Item_To_Inventory_Slot_Merge(self, item):
        if item.max_amount <= 1:
            return False  # Can't merge single-stack items
        # Check if this item type is already in the inventory, return false
        # if not return False
        inventory_slots_with_type = self.Find_Inventory_Slots_With_Sub_Type(item.sub_type)
        if not inventory_slots_with_type:
            return False

        for inventory_slot in inventory_slots_with_type:  
            if not inventory_slot.item or inventory_slot.item.amount >= inventory_slot.item.max_amount:
                continue

            # Calculate how much can be merged
            available_space = int(inventory_slot.item.max_amount - inventory_slot.item.amount)
            amount_to_merge = int(min(item.amount, available_space))

            # Merge items
            inventory_slot.item.Increase_Amount(amount_to_merge)
            item.Set_Amount(item.amount - amount_to_merge)

            # If the entire item was merged, remove it
            if item.amount == 0:
                self.game.item_handler.Remove_Item(item)
                inventory_slot.item.Update(self.game.delta_time)
                return True
            
        # If there is still remaining amount, try placing it in an empty slot
        if item.amount > 0:
            return self.Add_Item_To_Inventory_Slot(item)

        return False  # No slot to merge into
    

    # Returns true if inventory contains an arrow and reduces the amount of the
    # amount of the first arrow by 1
    def Find_Arrow(self):
        inventory_slots = self.Find_Inventory_Slots_With_Type('arrow')

        if not inventory_slots:
            return False
        
        inventory_slot = inventory_slots[0]
        inventory_slot.item.Decrease_Amount(1)
        
        if inventory_slot.item.amount <= 0:
            self.Remove_Item_From_Inventory(inventory_slot)

        return True
    
    # Returns all items in the inventory
    def Find_Loot(self):
        loot_items = []
        for inventory_slot in self.inventory:
            item = inventory_slot.item
            if not item:
                continue
            if item.sub_category == keys.loot:
                    loot_items.append(item)

        return loot_items


    def Revive(self):
        for inventory_slot in self.inventory:
            item = inventory_slot.item
            if not item:
                continue
            if hasattr(item, "Revive") and callable(getattr(item, "Revive")):
                if item.Revive():
                    return True
                
        return False
    
    def Check_Gold_In_Inventory(self):
        gold_inventory_slots = self.Find_Inventory_Slots_With_Sub_Type("gold")
        if not gold_inventory_slots:
            return 0
        
        gold_sum = 0
        
        for inventory_slot in gold_inventory_slots:
            item = inventory_slot.item
            if not item:
                continue

            gold_sum += item.amount

        return gold_sum
    

    def Pay_Gold(self, gold_to_pay):
        gold_in_inventory = self.Check_Gold_In_Inventory()

        if gold_to_pay > gold_in_inventory:
            return False
        
        gold_inventory_slots = self.Find_Inventory_Slots_With_Sub_Type("gold")
        
        for inventory_slot in gold_inventory_slots:
            item = inventory_slot.item
            
            # Skip empty slots, safety check
            if not item:
                continue
                
            # Determine the amount to deduct from this stack: 
            deduction = min(gold_to_pay, item.amount)
            
            # Delete item if amount <= 0
            item.Decrease_Amount(deduction)
            
            # If all required gold has been paid, stop iterating.
            gold_to_pay -= deduction
            if gold_to_pay <= 0:
                break
                
        return True

    # Places an item in an empty slot if merging is not possible
    def Add_Item_To_Inventory_Slot(self, item):

        for inventory_slot in self.inventory:
            if inventory_slot.item:
                continue
            if not inventory_slot.Add_Item(item):
                continue
            
            self.game.item_handler.Remove_Item(item)
            
            inventory_slot.item.Update(self.game.delta_time)
            return True
        
        return False  # No available slots
