from scripts.entities.items.runes.rune import Rune
from scripts.engine.keys.keys import keys


class Key_Rune(Rune):
    def __init__(self, game, type, pos, amount, rarity_value):
        super().__init__(game, keys.key_rune, pos, amount, rarity_value)


    def Activate(self):
        if not super().Activate():
            return
        
        nearby_decorations = self.game.decoration_handler.Find_Nearby_Decorations(self.game.player.pos, 4)

        # Filter for doors
        doors = [decoration for decoration in nearby_decorations if 'door' in decoration.type]
        mouse = self.game.mouse
        # Iterate over doors and check for collision
        for door in doors:
            if not door.rect().colliderect(mouse.rect_pos()):
                continue
            
            door.Set_Highlight()
            door.Open()
            self.game.player.Decrease_Souls(self.soul_cost)
            self.Set_Animation_Time()
            self.Reset_Animation_Size()
        return
