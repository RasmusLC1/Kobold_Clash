from scripts.interface.inventory.base_inventory import Base_Inventory
from scripts.interface.inventory.inventory_slot import Inventory_Slot
from scripts.engine.keys.keys import keys

class Rune_Inventory(Base_Inventory):


    def Setup(self):
        symbols = ['z', 'x', 'c']
        for i in range(3):
            
            (x_pos, y_pos) = self.Set_Inventory_Slot_Pos(i)
            index = i + 9
            inventory_slot = Inventory_Slot(self.game, (x_pos, y_pos), 'rune', self.size, None, index, symbols[i])
            background = self.game.assets['rune_background'][0]
            inventory_slot.Add_Background(background)
            # inventory_slot.inventory_type = 'rune'
            inventory_slot.Set_White_List(['rune'])
            self.Add_Inventory_Slot(inventory_slot)
        

    def Set_Inventory_Slot_Pos(self, index):
        x_pos = index * self.size[0] + self.game.screen_width / self.game.render_scale - 160
        y_pos = self.game.screen_height / self.game.render_scale - 40
        return (x_pos, y_pos)

    def Replace_Rune(self, old_rune, new_rune):
        # Find the corresponding inventory slot
        inventory_slot = self.Find_Item_Inventory_Slot_ID(old_rune.ID)

        if not inventory_slot:
            return False
        
        return inventory_slot.Add_Item(new_rune)

    def Set_Descriptions(self):
        for inventory_slot in self.inventory:  # Each value is a list of slots
            item = inventory_slot.item
            if not item:
                continue
            item.Set_Description()

    def Add_Item(self, item):
        for inventory_slot in self.inventory:
            if inventory_slot.item:
                continue
            if not inventory_slot.Add_Item(item):
                continue
            self.game.item_handler.Remove_Item(item)
            
            inventory_slot.item.Update(self.game.delta_time)
            item.Remove_Tile()
            return True
        return False  # No available slots