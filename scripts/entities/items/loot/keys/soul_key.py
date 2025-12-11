from scripts.entities.items.loot.keys.key import Key
from scripts.engine.keys.keys import keys

class Soul_Key(Key):
    def __init__(self, game, type, pos, amount, rarity_value):
        self.soul_cost = int(max(5, 30 - amount * 5))
        super().__init__(game, keys.soul_key, pos, rarity_value)


    def Set_Description(self):
        self.description = f'Pay souls to\nopen any door.\nsouls {self.soul_cost}'

    # Cost souls to open door
    def Open_Door(self):
        player = self.game.player
        if player.Get_Total_Available_Souls() < self.soul_cost:
            return False
        player.Decrease_Souls(self.soul_cost)
        return True