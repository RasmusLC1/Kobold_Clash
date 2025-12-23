from scripts.interface.inventory.keyboard_inventory import Keyboard_Inventory
from scripts.interface.inventory.weapon_inventory.weapon_inventory import Weapon_Inventory
from scripts.interface.inventory.rune_inventory.rune_inventory import Rune_Inventory
from scripts.interface.inventory.item_inventory.item_inventory import Item_Inventory
from scripts.engine.keys.keys import keys


class Inventory_Handler():
    def __init__(self, game):
        self.game = game
        self.active_item = None
        self.item_clicked = 0
        self.Set_Clicked_Inventory_Slot()
        self.clicked_inventory_slot_lock = False
        self.inventory = [None] * 14 # General shared inventory

        self.item_inventory = Item_Inventory(game, self.inventory)
        self.weapon_inventory = Weapon_Inventory(game, self.inventory)
        self.rune_inventory = Rune_Inventory(game, self.inventory)
        self.keyboard_handler = Keyboard_Inventory(game, self.inventory)
        self.saved_data = {}
        
    

    def Save_Inventory_Data(self):
        self.saved_data.clear()

        for inventory_slot in self.inventory:
            if not inventory_slot.item:
                continue
            inventory_slot.item.Save_Data()
            self.saved_data[inventory_slot.index] = inventory_slot.item.saved_data
            self.saved_data['active_inventory'] = self.weapon_inventory.active_inventory_slot.index


    # Loads inventory data and updates inventory_dic
    def Load_Data(self, data):
        self.saved_data = data  # Store loaded data

        for inventory_index, item_data in data.items():
            if not item_data:
                continue
            
            # Get the active_inventory_slot
            if isinstance(item_data, int):
                continue
            if "inventory_index" not in item_data:
                continue
            # Find correct slot
            inventory_slot = next((slot for slot in self.inventory if slot.index == item_data["inventory_index"]), None)
            if not inventory_slot:
                continue
            item = self.game.item_handler.Load_Item_From_Data(item_data)
            if not item:
                continue
            

            item.Remove_Tile()
            if not inventory_slot.Add_Item(item):
                print("FAILED TO LOAD ITEM: ", item.type, inventory_slot)
            
            # self.weapon_inventory.Set_Active_Inventory_Slot()

        # self.weapon_inventory.Set_Active_Inventory_Slot(self.inventory[0])

    # General Update function
    def Update(self, delta_time, offset=(0, 0)):

        self.Active_Item(offset)
        for inventory_slot in self.inventory:
            if not inventory_slot.item:
                continue
            inventory_slot.Update_Item(delta_time)
            if not self.Update_Inventory_Slot_Item_Animation(inventory_slot, delta_time):
                continue
            # Check if the mouse has been clicked, if no we skip that inventory
            # slot if no continue to next inventory slot
            if not self.game.mouse.left_click:
                continue
            if not self.Inventory_Slot_Collision_Click(inventory_slot):
                continue
            if self.Pickup_Item_To_Move(inventory_slot):
                return
            
            
        self.Item_Click()
        self.keyboard_handler.Key_Board_Input()
        return

    def Update_Runes(self):
        self.rune_inventory.Add_Active_Runes()

    # Needs to resize the UI correctly when screen is resized
    def Update_Inventory_Slot_Pos(self):
        return
        for index, inventory_slot in enumerate(self.inventory):
            pos = self.Set_Item_Inventory_Slot_Pos(index)
            inventory_slot.Update_Pos(pos)

    def Clear_Inventory(self):
        self.item_inventory.Clear_Inventory()
        self.weapon_inventory.Clear_Inventory()
        self.rune_inventory.Clear_Inventory()
        for inventory_slot in self.inventory:
            inventory_slot.Clear()


    def Increment_Weapon_Inventory(self):
        self.weapon_inventory.Mouse_Scroll_Update_Active_Inventory()


    def Remove_Item(self, item):
        self.item_inventory.Remove_Item(item)
        self.weapon_inventory.Remove_Item(item)
        self.rune_inventory.Remove_Item(item)

    # Activates when mouse has been held down for 10 ticks and
    # the inventory slot is not active anymore 
    def Pickup_Item_To_Move(self, inventory_slot):
        if self.game.mouse.hold_down_left > 10 and not inventory_slot.active:
            # Move the item
            self.active_item = inventory_slot.item
            self.active_item.picked_up = False
            inventory_slot.item = None
            inventory_slot.Set_Active(True)
            return True
        return False

    # Check for collision with inventory slot, if no collision return False
    def Inventory_Slot_Collision_Click(self, inventory_slot):
        if inventory_slot.rect().colliderect(self.game.mouse.rect_click()):
            self.Set_Clicked_Inventory_Slot(inventory_slot)
            self.clicked_inventory_slot_lock = True
            self.item_clicked += 1
            return True
        
        return False

    # Update the animation of the item, return False if no item
    def Update_Inventory_Slot_Item_Animation(self, inventory_slot, delta_time):
        if inventory_slot.item:
            inventory_slot.item.Update_Animation(delta_time)
            return True
        return False

     # Handle clicking items
    def Item_Click(self):
        if not self.game.mouse.left_click:
            if self.clicked_inventory_slot:
                if self.Item_Double_Click():
                    if self.weapon_inventory.active_inventory_slot.item:
                        self.weapon_inventory.active_inventory_slot.item.Set_Position(self.weapon_inventory.active_inventory_slot.pos)
                    return
                if self.Item_Single_Click():
                    return
        return
    
    # Handle double clicking behaviour, return True if valid double click
    def Item_Double_Click(self):
        if self.game.mouse.double_click and self.clicked_inventory_slot.item:
            if not self.clicked_inventory_slot.item.sub_category == keys.weapon:
                return False
            
            # Transfer to the next available inventory slot
            active_inventory_slot = self.Get_Double_Click_Inventory_Slot()

            if not active_inventory_slot:
                return False
            
                      
            if self.Swap_Item(active_inventory_slot, self.clicked_inventory_slot.item):
                self.Set_Clicked_Inventory_Slot()
                return True

            if self.Move_Item(self.clicked_inventory_slot.item, active_inventory_slot):
                self.Reset_Inventory_Slot()
                for inventory_slot in self.inventory:
                    if not inventory_slot.item:
                        continue
                self.Set_Clicked_Inventory_Slot()
                return True
            self.Set_Clicked_Inventory_Slot()
            return True
        
        self.active_item = None
        self.Set_Clicked_Inventory_Slot()
        return False

    # Gets the next avaiable inventory slot for either weapon or item inventory
    def Get_Double_Click_Inventory_Slot(self):
            if self.clicked_inventory_slot.type == keys.weapon:
                return self.item_inventory.Get_Next_Avaiable_Inventory_Slot()
            elif self.clicked_inventory_slot.type == keys.item:
                return self.weapon_inventory.Get_Next_Avaiable_Inventory_Slot()

            return None

    # Finds the first empty inventory slot
    def Find_Available_Inventory_Slot(self):
        for i, inventory_slot in enumerate(self.inventory):
            if inventory_slot is None:
                return i # return index
        return None  # No available slots

    # Add item to the inventory
    def Add_Item(self, item):
        if item.sub_category == keys.rune:
            return self.rune_inventory.Add_Item(item)
        else:
            return self.item_inventory.Add_Item(item)

    def Add_Rune(self, rune):
        self.rune_inventory.Add_Item(rune)

    def Replace_Rune(self, old_rune, new_rune):
        self.rune_inventory.Replace_Rune(old_rune, new_rune)

    # Handle single clicking behavior, return True if valid click
    def Item_Single_Click(self):
        if not self.clicked_inventory_slot or not self.clicked_inventory_slot.item:
            return False
        if self.game.mouse.single_click_delay and self.game.mouse.double_click:
            return False

        if not (0 < self.game.mouse.hold_down_left < 5):
            return False

        self.clicked_inventory_slot.item.Activate()
        self.clicked_inventory_slot.Update()
        self.Set_Clicked_Inventory_Slot()
        self.game.mouse.Set_Inventory_Clicked(10)
        return True

    def Find_Inventory_Slot(self, index):
        return self.inventory[index]

    # Return the item to its previous Inventory slot and deactivate the item and slot
    def Return_Item(self):
        if self.clicked_inventory_slot:
            if not self.clicked_inventory_slot.item:  # Ensure slot is empty before returning item
                self.Move_Item(self.active_item, self.clicked_inventory_slot)
                # inventory_slot = self.item_inventory.Find_Item_Inventory_Slot_ID(self.active_item.ID)
                self.active_item = None
                self.Set_Clicked_Inventory_Slot()
            else:
                print("Error: Slot already occupied when trying to return item.")
        return

    # Move the item around
    def Drag_Item(self, offset):
        self.active_item.Move(self.game.mouse.mpos)

        if not self.game.mouse.left_click:
            self.Place_Down_Item()
            self.Reset_Inventory_Slot()
            return False
        return True

    # Places an item down from the inventory
    def Place_Down_Item(self):
        if self.active_item.Place_Down():
            inventory_slot = self.item_inventory.Find_Item_Inventory_Slot_ID(self.active_item.ID)
            
            if inventory_slot:
                self.item_inventory.Remove_Item_From_Inventory(inventory_slot)
            
            self.game.item_handler.Add_Item(self.active_item)
            self.active_item.picked_up = False
            self.active_item.Set_Tile()
        
        self.active_item = None



    # Set the inventory to be inactive again
    def Reset_Inventory_Slot(self):
        if not self.clicked_inventory_slot:
            return
        
        self.clicked_inventory_slot.Set_Active(False)

        if self.clicked_inventory_slot.type == keys.weapon:
            self.game.player.Remove_Active_Weapon()

        self.clicked_inventory_slot.item = None
        self.Set_Clicked_Inventory_Slot()


    def Move_Item_To_New_Slot(self, offset):
        # Check if the item is being moved to another inventory
        if self.active_item.move_inventory_slot:
            self.active_item.move_inventory_slot = False
            self.active_item = None  # Clear active item
            return True

        for inventory_slot in self.inventory:
            if inventory_slot.rect().colliderect(self.game.mouse.rect_pos(offset)):
                if inventory_slot.active:
                    return False

                if self.Gem_Check(inventory_slot):
                    return True
                

                if self.Swap_Item(inventory_slot, self.active_item):
                    return True

                if self.Move_Item(self.active_item, inventory_slot):
                    self.Reset_Inventory_Slot()
                    for inventory_slot in self.inventory:
                        if not inventory_slot.item:
                            continue
                    self.active_item = None  # Clear active item
                    return True
        return False

    def Gem_Check(self, inventory_slot):
        if not inventory_slot.item:
            return False

        if not {inventory_slot.item.sub_category == keys.weapon
            and not self.active_item.type == keys.gem}:
            return False
            
        if self.Add_Gem_To_Weapon(inventory_slot.item, self.active_item):
            return True
        else:
            return False

    def Ingot_Check(self, inventory_slot):
        if not inventory_slot.item:
            return False

        if not self.active_item.type == keys.ingot:
            return False
        
        item_types = {
            keys.Steel_ingot : keys.weapon,
            keys.Gold_ingot : keys.weapon,
            keys.Silver_ingot : keys.rune,
            keys.jade_ingot : keys.rune,
            keys.copper_ingot : keys.utility,
        }


        # Check for the inventory item type matches the ingot type
        affected_item_type = item_types.get(self.active_item.sub_type, None)

        if not affected_item_type:
            print("INGOT NOT FOUND", self.active_item.sub_type, inventory_slot.item)
            return False
        
        if inventory_slot.item.type != affected_item_type:
            return False
        
        # Returns true if succesfully added
        add_ingot_success = self.active_item.Add_Ingot_To_Item(inventory_slot.item)
        self.Reset_Active_Item()
        return add_ingot_success
    
    def Reset_Active_Item(self):
        # Reset the gem inventory slot
        self.clicked_inventory_slot.Reset_Inventory_Slot()
        self.Set_Clicked_Inventory_Slot()  # Clear clicked slot
        self.active_item = None  # Clear active item


    def Move_Item(self, item, inventory_slot):
        inventory_type_holder = item.inventory_type
        item.picked_up = True  # Ensure the item is marked as picked up

        # Try to place the item in the inventory slot
        if not inventory_slot.Add_Item(item):
            return False

        inventory_slot.Set_Active(False)  # Deactivate slot after placing item

        if inventory_type_holder:
            item.Update_Player_Hand(inventory_type_holder)

        self.weapon_inventory.Equip_Weapon()
        
        return True


    # item_being_moved is the active item
    # receiving_inventory_slot is the inventory slot that item_being_moved is
    # being moved to
    def Swap_Item(self, receiving_inventory_slot, item_being_moved):
        if not receiving_inventory_slot.item:
            return False
        

        item_holder = receiving_inventory_slot.item  # Store item to be swapped

        
        self.clicked_inventory_slot.Reset_Inventory_Slot()
        receiving_inventory_slot.Reset_Inventory_Slot()
        # Check if the items being moved are gems and weapons

        # Move original item to active inventory slot
        self.clicked_inventory_slot.Add_Item(item_holder)

        self.Set_Clicked_Inventory_Slot()  # Clear clicked slot

        
        # Move active item into the new slot
        receiving_inventory_slot.Add_Item(item_being_moved)

        self.weapon_inventory.Equip_Weapon()


        self.active_item = None  # Clear active item
        return True


    def Add_Gem_To_Weapon(self, weapon, gem):
        if gem.type != keys.gem:
            return False

        if weapon.sub_category != keys.weapon:
            return False

        if not weapon.Add_Gem(gem):
            return False
        
        # Reset the gem inventory slot
        self.Reset_Active_Item()
        return True

    def Active_Item(self, offset=(0, 0)):
        if not self.active_item:
            return

        item_out_of_bounds = self.active_item.Move_Legal(
            self.game.mouse.mpos, self.game.player.pos, self.game.tilemap, offset
        )

        if not item_out_of_bounds:
            if not self.game.mouse.left_click:
                if self.Move_Item_To_New_Slot(offset):
                    return  
                if not self.active_item:
                    return
                self.Return_Item()
                return
            self.active_item.Render_Out_Of_Bounds(
                self.game.player.pos, self.game.mouse.mpos, self.game.display, offset
            )
        else:
            if not self.Drag_Item(offset):
                return
            self.active_item.Render_In_Bounds(
                self.game.player.pos, self.game.mouse.mpos, self.game.display, offset
            )

    def Set_Clicked_Inventory_Slot(self, inventory_slot = None):
        if inventory_slot:
            self.clicked_inventory_slot_lock = True
        else:
            self.clicked_inventory_slot_lock = False

        self.clicked_inventory_slot = inventory_slot
        


    def Overflow(self, item):
        empty_slots = {i: slot for i, slot in enumerate(self.inventory) if not slot.item}
        
        for slot in empty_slots.values():
            if slot.Add_Item(item):
                slot.item.Update(self.game.delta_time)
                return True

        return False

    def Render(self, surf):
        for inventory_slot in self.inventory:
            inventory_slot.Render(surf)
