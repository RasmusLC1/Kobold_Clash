from scripts.entities.items.loot.keys.key import Key
from scripts.engine.keys.keys import keys

class Soul_Key(Key):
    def __init__(self, game, pos):
        super().__init__(game, keys.soul_key, pos)
        self.description = 'Pay souls to\nopen any door.\nsouls 30'
        self.soul_cost = 30

    # Cost souls to open door
    def Open_Door(self):
        player = self.game.player
        if player.Get_Total_Available_Souls() < self.soul_cost:
            return False
        player.Decrease_Souls(30)
        return True