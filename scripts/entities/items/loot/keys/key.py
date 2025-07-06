from scripts.entities.items.loot.interactive_loot import Interactive_Loot
from scripts.engine.keys.keys import keys

class Key(Interactive_Loot):
    def __init__(self, game, type, pos):
        super().__init__(game, type, pos, 64, (16, 16), keys.key, 1)


    # The update function in the inventory
    def Update_In_Inventory(self):
        if not super().Update_In_Inventory():
            return False
        
        self.Check_If_Doors_Can_Open()
        
    
    def Check_If_Doors_Can_Open(self):
        nearby_decorations = self.game.decoration_handler.Find_Nearby_Decorations(self.game.player.pos, 4)

        # Filter for doors
        doors = [decoration for decoration in nearby_decorations if 'door' in decoration.type]
        mouse = self.game.mouse
        # Iterate over doors and check for collision
        for door in doors:
            if not door.rect().colliderect(mouse.rect_pos()):
                continue
            
            door.Set_Highlight()
            if not mouse.left_click:
                continue
            if not self.Open_Door():
                return
            door.Open()


    # Effect of opening door on key
    def Open_Door(self):
        pass

