from scripts.entities.items.loot.radius_effect_loot import Radius_Effect_Loot
from scripts.engine.keys.keys import keys


class Bomb(Radius_Effect_Loot):
    def __init__(self, game, type, pos, amount, rarity_value):
        super().__init__(game, type, pos, 192, keys.bomb, radius=4, amount=amount, rarity_value=rarity_value, max_amount=3)
        

    def Set_Description(self):
        effect = self.type.replace('_' + keys.bomb, '')
        self.description = effect + ' explosion\nwhen thrown' 

    def Reset_Bomb(self):
        self.game.item_handler.Remove_Item(self, True)
        self.game.inventory.Remove_Item(self)
    
    # The update function in the inventory
    def Update_In_Inventory(self):
        if not super().Update_In_Inventory():
            return False
        
        if self.game.mouse.left_click:
            self.Initalise_Throw()


    # Effect of opening door on key
    def Initalise_Throw(self):
        player = self.game.player
        # SPAWN ACTUAL BOMB PROJECTILE HERE, same sprite
        player.bomb_launcher.Shoot_Bomb(player, 100, self.type, self.game.mouse.mpos)
        self.Reset_Bomb()

