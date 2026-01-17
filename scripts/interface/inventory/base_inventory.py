from scripts.engine.keys.keys import keys


class Base_Inventory():
    def __init__(self, game, shared_inventory):
        self.game = game
        self.size = (34, 34)
        self.shared_inventory = shared_inventory
        self.inventory = []

        self.Setup()
    
    # Return True or False depending on if the type is in the dictionary
    def Clear_Inventory_Slot(self, type):
        return self.inventory.pop(type, None) is not None # Remove the index


    def Find_Inventory_Slots_With_Sub_Type(self, sub_type):
        inventory_slots_with_item_type = []
        for inventory_slot in self.inventory:
            if not inventory_slot.item:
                continue
            if sub_type == inventory_slot.item.sub_type:
                inventory_slots_with_item_type.append(inventory_slot)
            
        return inventory_slots_with_item_type
    
    def Find_Inventory_Slots_With_Item_Type(self, type):
        inventory_slots_with_item_type = []
        for inventory_slot in self.inventory:
            if not inventory_slot.item:
                continue
            if type == inventory_slot.item.type:
                inventory_slots_with_item_type.append(inventory_slot)
            
        return inventory_slots_with_item_type
        
        
    def Append_Inventory(self, inventory_slot):
        pass

    # Configure the inventory when Initialiased
    def Setup(self):
        pass

    def Set_Inventory_Slot_Pos(self, index):
        pass

    def Add_Item(self, item):
        pass

    def Clear_Inventory(self):
        for inventory_slot in self.inventory:
            inventory_slot.Clear()

    def Find_Item_Inventory_Slot_ID(self, ID):
        for inventory_slot in self.inventory:
            if not inventory_slot.item:
                continue
            
            if inventory_slot.item.ID == ID:
                return inventory_slot
            
        return None
    
    # Clears the item from the inventory and removes it from the dictionary
    def Remove_Item_From_Inventory(self, inventory_slot):

        # Remove the item from the game
        self.game.item_handler.Remove_Item(inventory_slot.item, True)
        
        # Clear the inventory slot
        inventory_slot.Remove_Item()

    def Remove_Item(self, item):
        inventory_slot = self.Find_Item_Inventory_Slot_ID(item.ID)
        if not inventory_slot:
            return False
        
        self.Remove_Item_From_Inventory(inventory_slot)

    def Get_Next_Avaiable_Inventory_Slot(self):
        for inventory_slot in self.inventory:
            if inventory_slot.item:
                continue
            return inventory_slot
        
        return None


    def Add_Inventory_Slot(self, inventory_slot):
        self.shared_inventory[inventory_slot.index] = inventory_slot
        self.inventory.append(inventory_slot)
