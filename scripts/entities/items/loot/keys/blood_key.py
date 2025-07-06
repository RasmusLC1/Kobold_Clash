from scripts.entities.items.loot.keys.key import Key
from scripts.engine.keys.keys import keys

class Blood_Key(Key):
    def __init__(self, game, pos):
        super().__init__(game, keys.blood_key, pos)
        self.description = 'Sacrifice blood\nto open any door\n5 health'


    # Sacrifice 5 health to open door
    def Open_Door(self):
        player = self.game.player

        if player.health <= 5:
            return False
        self.game.player.Damage_Taken(5)
        return True