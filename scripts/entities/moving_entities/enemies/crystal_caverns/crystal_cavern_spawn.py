from scripts.entities.moving_entities.enemies.crystal_caverns.elementals.fire_spirit import Fire_Spirit
from scripts.entities.moving_entities.enemies.crystal_caverns.elementals.ice_spirit import Ice_Spirit
from scripts.entities.moving_entities.enemies.crystal_caverns.elementals.earth_elemental import Earth_Elemental
from scripts.entities.moving_entities.enemies.crystal_caverns.elementals.electric_elemental import Electric_Elemental
from scripts.entities.moving_entities.enemies.crystal_caverns.elementals.poison_elemental import Poison_Elemental
from scripts.entities.moving_entities.enemies.crystal_caverns.mythicals.medusa import Medusa
from scripts.entities.moving_entities.enemies.crystal_caverns.mythicals.minotaur.minotaur import Minotaur
from scripts.entities.moving_entities.enemies.enemy_spawner import Enemy_Spawner
from scripts.engine.keys.keys import keys

class Crystal_Cavern_Spawn(Enemy_Spawner):
    def __init__(self, game):
        spawn_methods = {
            keys.fire_spirit : self.Spawn_Fire_Spirit,
            keys.ice_spirit: self.Spawn_Ice_Spirit,
            keys.earth_elemental: self.Spawn_Earth_Elemental,
            keys.electric_elemental: self.Spawn_Electric_Elemental,
            keys.poison_elemental: self.Spawn_Poison_Elemental,
            keys.minotaur: self.Spawn_Minotaur,
            keys.medusa: self.Spawn_Medusa,
        }

        enemy_types = {
            keys.fire_spirit: 0.2,
            keys.ice_spirit: 0.2,
            keys.earth_elemental: 0.2,
            keys.electric_elemental: 10000.2,
            keys.poison_elemental: 0.2,
            keys.minotaur: 0.2,
            keys.medusa: 0.2,
        }
        super().__init__(game, spawn_methods, enemy_types)
    
    def Spawn_Fire_Spirit(self, pos):
        health = 40
        strength = 4
        speed = 4
        agility = 4 
        intelligence = 2
        stamina = 2
        return Fire_Spirit(self.game,
                            pos, 
                            health,
                            strength,
                            speed,
                            agility,
                            intelligence,
                            stamina)
        

    def Spawn_Ice_Spirit(self, pos):
        health = 50
        strength = 7
        speed = 3
        agility = 3
        intelligence = 2
        stamina = 2
        return Ice_Spirit(self.game,
                        pos, 
                        health,
                        strength,
                        speed,
                        agility,
                        intelligence,
                        stamina)


    def Spawn_Earth_Elemental(self, pos):
        health = 80
        strength = 7
        speed = 2
        agility = 3
        intelligence = 2
        stamina = 2
        return Earth_Elemental(self.game,
                        pos, 
                        health,
                        strength,
                        speed,
                        agility,
                        intelligence,
                        stamina)

  

    def Spawn_Electric_Elemental(self, pos):
        health = 50
        strength = 4
        speed = 2
        agility = 3
        intelligence = 2
        stamina = 2
        return Electric_Elemental(self.game,
                        pos, 
                        health,
                        strength,
                        speed,
                        agility,
                        intelligence,
                        stamina)
    
    
    def Spawn_Poison_Elemental(self, pos):
        health = 20
        strength = 4
        speed = 4
        agility = 3
        intelligence = 2
        stamina = 2
        return Poison_Elemental(self.game,
                        pos, 
                        health,
                        strength,
                        speed,
                        agility,
                        intelligence,
                        stamina)

    def Spawn_Medusa(self, pos):
        health = 20
        strength = 4
        speed = 4
        agility = 3
        intelligence = 2
        stamina = 2
        return Medusa(self.game,
                        pos, 
                        health,
                        strength,
                        speed,
                        agility,
                        intelligence,
                        stamina)
    
    def Spawn_Minotaur(self, pos):
        health = 20
        strength = 4
        speed = 4
        agility = 3
        intelligence = 2
        stamina = 2
        return Minotaur(self.game,
                        pos, 
                        health,
                        strength,
                        speed,
                        agility,
                        intelligence,
                        stamina)