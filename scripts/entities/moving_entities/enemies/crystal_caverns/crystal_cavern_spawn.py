from scripts.entities.moving_entities.enemies.crystal_caverns.elementals.fire_spirit import Fire_Spirit
from scripts.entities.moving_entities.enemies.crystal_caverns.elementals.ice_spirit import Ice_Spirit
from scripts.engine.keys.keys import keys

class Crystal_Cavern_Spawn():
    def __init__(self, game):
        self.game = game
        self.spawn_methods = {
            keys.fire_spirit : self.Spawn_Fire_Spirit,
            keys.ice_spirit: self.Spawn_Ice_Spirit,
        }

        self.enemy_types = {
            keys.fire_spirit: 0.2,
            keys.ice_spirit: 0.2,
        }
    
    def Spawn_Fire_Spirit(self, pos):
        health = 80
        strength = 4
        speed = 5
        agility = 4 
        intelligence = 2
        stamina = 2
        return Fire_Spirit(self.game,
                            pos, 
                            keys.fire_spirit,
                            health,
                            strength,
                            speed,
                            agility,
                            intelligence,
                            stamina)
        

    def Spawn_Ice_Spirit(self, pos):
        health = 100
        strength = 7
        speed = 3
        agility = 3
        intelligence = 2
        stamina = 2
        return Ice_Spirit(self.game,
                        pos, 
                        keys.ice_spirit,
                        health,
                        strength,
                        speed,
                        agility,
                        intelligence,
                        stamina)

  