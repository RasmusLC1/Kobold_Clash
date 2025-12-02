from scripts.engine.keys.keys import keys
import pygame

class Keyboard_Inventory():
    def __init__(self, game, shared_inventory):
        self.inventory = shared_inventory
        self.game = game
        self.KEY_MAP = {
            pygame.K_1: 0,
            pygame.K_2: 1,
            pygame.K_3: 2,
            pygame.K_4: 3,
            pygame.K_5: 4,
            pygame.K_6: 5,
            pygame.K_7: 6,
            pygame.K_8: 7,
            pygame.K_9: 8,
            pygame.K_z: 9,
            pygame.K_x: 10,
            pygame.K_c: 11,
        }
    
    def Key_Board_Input(self):
        index = self.Check_Keyboard_input()
        
        # negative index means it's not found
        if index < 0:
            return
        
        self.Activate_Inventory_Slot(index)

    # Return negative if not no keyboard input
    def Check_Keyboard_input(self):
            keyboard_handler = self.game.keyboard_handler
            
            # Iterate through the keys in the predefined map
            for key_constant, return_index in self.KEY_MAP.items():
                
                if keyboard_handler.is_key_pressed(key_constant):
                    return return_index

            # Default case: no mapped key is pressed
            return -999

    def Find_Inventory_Slot_By_Index(self, index):
        for inventory_slot in self.inventory:
            if inventory_slot.index == index:
                return inventory_slot

        return None 

    def Activate_Inventory_Slot(self, index):
        inventory_slot = self.Find_Inventory_Slot_By_Index(index)
        if not inventory_slot:
            return
        
        if not inventory_slot.item:
            return
        
        inventory_slot.item.Activate()
        inventory_slot.Update()