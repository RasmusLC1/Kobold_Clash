from scripts.engine.keys.keys import keys

class Keyboard_Inventory():
    def __init__(self, game, shared_inventory):
        self.inventory = shared_inventory
        self.game = game
    
    def Key_Board_Input(self):
        index = self.Check_Keyboard_input()
        
        # negative index means it's not found
        if index < 0:
            return
        
        self.Activate_Inventory_Slot(index)

    # Return negative if not no keyboard input
    def Check_Keyboard_input(self):
        keyboard = self.game.keyboard_handler

        match True:
            case keyboard._1_pressed:
                return 0
            case keyboard._2_pressed:
                return 1
            case keyboard._3_pressed:
                return 2
            case keyboard._4_pressed:
                return 3
            case keyboard._5_pressed:
                return 4
            case keyboard._6_pressed:
                return 5
            case keyboard._7_pressed:
                return 6
            case keyboard._8_pressed:
                return 7
            case keyboard._9_pressed:
                return 8
            case keyboard.z_pressed:
                return 9
            case keyboard.x_pressed:
                return 10
            case keyboard.c_pressed:
                return 11
            case _:
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