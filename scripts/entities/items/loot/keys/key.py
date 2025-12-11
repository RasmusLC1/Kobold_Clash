from scripts.entities.items.loot.interactive_loot import Interactive_Loot
from scripts.engine.keys.keys import keys

class Key(Interactive_Loot):
    def __init__(self, game, type, pos, rarity_value, amount = 1, max_amount = 1):
        super().__init__(game, type, pos, max_distance=64, size=(16, 16), loot_type=keys.key, rarity_value=rarity_value, amount=amount, max_amount=max_amount)


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

