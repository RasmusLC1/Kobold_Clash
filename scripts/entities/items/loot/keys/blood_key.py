from scripts.entities.items.loot.keys.key import Key
from scripts.engine.keys.keys import keys

class Blood_Key(Key):
    def __init__(self, game, type, pos, amount, rarity_value):
        self.damage = int(max(1, 5 - amount))
        super().__init__(game, keys.blood_key, pos, rarity_value)


    def Set_Description(self):
        self.description = f'Sacrifice blood\nto open any door\n{self.damage} health'

    # Sacrifice 5 health to open door
    def Open_Door(self):
        player = self.game.player

        if player.health <= self.damage:
            return False
        self.game.player.Damage_Taken(self.damage)
        return True