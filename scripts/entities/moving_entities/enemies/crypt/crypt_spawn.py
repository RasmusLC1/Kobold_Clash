 
from scripts.entities.moving_entities.enemies.crypt.skeleton.skeleton_warrior import Skeleton_Warrior
from scripts.entities.moving_entities.enemies.crypt.skeleton.skeleton_ranger import Skeleton_Ranger
from scripts.entities.moving_entities.enemies.crypt.skeleton.skeleton_bell_toller import Skeleton_Bell_Toller
from scripts.entities.moving_entities.enemies.crypt.skeleton.skeleton_cleric import Skeleton_Cleric
from scripts.entities.moving_entities.enemies.crypt.skeleton.skeleton_undertaker import Skeleton_Undertaker 
from scripts.entities.moving_entities.enemies.crypt.skeleton.skeleton_warlock import Skeleton_Warlock 
from scripts.entities.moving_entities.enemies.crypt.skeleton.skeleton_guardian import Skeleton_Guardian 
from scripts.entities.moving_entities.enemies.crypt.skeleton.skeleton_banner_bearer import Skeleton_Banner_Bearer 
from scripts.entities.moving_entities.enemies.crypt.dwellers.spider.spider import Spider
from scripts.entities.moving_entities.enemies.crypt.dwellers.ghoul import Ghoul
from scripts.entities.moving_entities.enemies.crypt.dwellers.vampire.vampire import Vampire
from scripts.entities.moving_entities.enemies.crypt.void_spawn.shade import Shade
from scripts.entities.moving_entities.enemies.crypt.void_spawn.phantom import Phantom
from scripts.entities.moving_entities.enemies.crypt.void_spawn.wraith.wraith import Wraith
from scripts.entities.moving_entities.enemies.crypt.skeleton.wight_king.wight_king import Wight_King
from scripts.entities.moving_entities.enemies.enemy_spawner import Enemy_Spawner
from scripts.engine.keys.keys import keys

class Crypt_Spawn(Enemy_Spawner):
    def __init__(self, game):
        spawn_methods = {
            keys.skeleton_warrior: self.Spawn_Skeleton_Warrior,
            keys.skeleton_ranger : self.Spawn_Skeleton_Ranger,
            keys.spider : self.Spawn_Spider,
            keys.wight_king : self.Spawn_Wight_King,
            keys.vampire : self.Spawn_Vampire,
            keys.skeleton_bell_toller : self.Spawn_Skeleton_Bell_Toller,
            keys.skeleton_cleric : self.Spawn_Skeleton_Cleric,
            keys.skeleton_undertaker : self.Spawn_Skeleton_Undertaker,
            keys.skeleton_warlock : self.Spawn_Skeleton_Warlock,
            keys.skeleton_guardian : self.Spawn_Skeleton_Guardian,
            keys.skeleton_banner_bearer : self.Spawn_Skeleton_Banner_Bearer,
            keys.shade : self.Spawn_Shade,
            keys.phantom : self.Spawn_Phantom,
            keys.wraith : self.Spawn_Wraith,
            keys.ghoul : self.Spawn_Ghoul,
        }

        enemy_types = {
            keys.skeleton_warrior: 10.4,
            keys.skeleton_ranger: 10.2,
            keys.skeleton_bell_toller: 10.1,
            keys.skeleton_cleric: 10.05,
            keys.skeleton_undertaker: 10.05,
            keys.skeleton_guardian: 10.2,
            keys.skeleton_warlock: 10.05,
            keys.skeleton_banner_bearer: 10.05,
            keys.phantom: 10.1,
            keys.wraith: 10.05,
            keys.shade: 10.05,
            keys.spider: 10.1,
            keys.ghoul: 10.2,
            keys.wight_king: 10.01,
            keys.vampire: 10.01,
        }
        super().__init__(game, spawn_methods, enemy_types)
        
    def Spawn_Skeleton_Warrior(self, pos):
        health = 70
        strength = 3
        speed = 3
        agility = 2 
        intelligence = 2
        stamina = 2
        return Skeleton_Warrior(
            self.game,
            pos, 
            health,
            strength,
            speed,
            agility,
            intelligence,
            stamina)
    
    def Spawn_Skeleton_Guardian(self, pos):
        health = 120
        strength = 4
        speed = 1
        agility = 2 
        intelligence = 2
        stamina = 2
        return Skeleton_Guardian(
            self.game,
            pos, 
            health,
            strength,
            speed,
            agility,
            intelligence,
            stamina)
        
    def Spawn_Skeleton_Ranger(self, pos):
        health = 40
        strength = 2
        speed = 4
        agility = 2 
        intelligence = 2
        stamina = 2
        return Skeleton_Ranger(
            self.game,
            pos, 
            health,
            strength,
            speed,
            agility,
            intelligence,
            stamina)
    
    def Spawn_Skeleton_Bell_Toller(self, pos):
        health = 60
        strength = 3
        speed = 3
        agility = 2 
        intelligence = 2
        stamina = 2
        return Skeleton_Bell_Toller(
            self.game,
            pos, 
            health,
            strength,
            speed,
            agility,
            intelligence,
            stamina)
    
    def Spawn_Skeleton_Cleric(self, pos):
        health = 40
        strength = 1
        speed = 2
        agility = 2 
        intelligence = 2
        stamina = 2
        return Skeleton_Cleric(
            self.game,
            pos, 
            health,
            strength,
            speed,
            agility,
            intelligence,
            stamina)
    
    def Spawn_Skeleton_Banner_Bearer(self, pos):
        health = 50
        strength = 1
        speed = 2
        agility = 2 
        intelligence = 2
        stamina = 2
        return Skeleton_Banner_Bearer(
            self.game,
            pos, 
            health,
            strength,
            speed,
            agility,
            intelligence,
            stamina)
    
    def Spawn_Skeleton_Warlock(self, pos):
        health = 40
        strength = 1
        speed = 1
        agility = 2 
        intelligence = 5
        stamina = 2
        return Skeleton_Warlock(
            self.game,
            pos, 
            health,
            strength,
            speed,
            agility,
            intelligence,
            stamina)
    
    def Spawn_Skeleton_Undertaker(self, pos):
        health = 110
        strength = 5
        speed = 2
        agility = 2 
        intelligence = 2
        stamina = 2
        return Skeleton_Undertaker(
            self.game,
            pos, 
            health,
            strength,
            speed,
            agility,
            intelligence,
            stamina)
    
    def Spawn_Wight_King(self, pos):
        health = 200
        strength = 6
        speed = 4
        agility = 6
        intelligence = 5
        stamina = 5
        return Wight_King(self.game,
                    pos, 
                    health,
                    strength,
                    speed,
                    agility,
                    intelligence,
                    stamina)
    
    def Spawn_Shade(self, pos):
        health = 50
        strength = 3
        speed = 1
        agility = 2 
        intelligence = 2
        stamina = 2
        return Shade(
            self.game,
            pos, 
            health,
            strength,
            speed,
            agility,
            intelligence,
            stamina)
    
    def Spawn_Phantom(self, pos):
        health = 20
        strength = 5
        speed = 6
        agility = 2 
        intelligence = 2
        stamina = 2
        return Phantom(
            self.game,
            pos, 
            health,
            strength,
            speed,
            agility,
            intelligence,
            stamina)

    def Spawn_Wraith(self, pos):
        health = 50
        strength = 3
        speed = 4
        agility = 2 
        intelligence = 2
        stamina = 2
        return Wraith(
            self.game,
            pos, 
            health,
            strength,
            speed,
            agility,
            intelligence,
            stamina)
    
    def Spawn_Ghoul(self, pos):
        health = 80
        strength = 6
        speed = 6
        agility = 2 
        intelligence = 2
        stamina = 2
        return Ghoul(
            self.game,
            pos, 
            health,
            strength,
            speed,
            agility,
            intelligence,
            stamina)
    
    def Spawn_Vampire(self, pos):
        health = 150
        strength = 4
        speed = 3
        agility = 3
        intelligence = 2
        stamina = 2
        return Vampire(
            self.game,
            pos, 
            health,
            strength,
            speed,
            agility,
            intelligence,
            stamina)
    
    def Spawn_Spider(self, pos):
        health = 60
        strength = 4
        speed = 6
        agility = 3
        intelligence = 5
        stamina = 2
        return Spider(self.game,
                    pos, 
                    health,
                    strength,
                    speed,
                    agility,
                    intelligence,
                    stamina)
        
