from scripts.entities.moving_entities.enemies.enemy import Enemy
from scripts.entities.moving_entities.enemies.skeleton.skeleton_warrior import Skeleton_Warrior
from scripts.entities.moving_entities.enemies.skeleton.skeleton_ranger import Skeleton_Ranger
from scripts.entities.moving_entities.enemies.skeleton.skeleton_bell_toller import Skeleton_Bell_Toller
from scripts.entities.moving_entities.enemies.skeleton.skeleton_cleric import Skeleton_Cleric
from scripts.entities.moving_entities.enemies.skeleton.skeleton_undertaker import Skeleton_Undertaker 
from scripts.entities.moving_entities.enemies.fire_spirit import Fire_Spirit
from scripts.entities.moving_entities.enemies.ice_spirit import Ice_Spirit
from scripts.entities.moving_entities.enemies.spider.spider import Spider
from scripts.entities.moving_entities.enemies.skeleton.wight_king.wight_king import Wight_King
from scripts.engine.assets.keys import keys

import random

class Enemy_Handler():
    def __init__(self, game):
        self.game = game
        self.enemies = []
        self.pathfinding_queue = []
        self.pathfinding_queue_cooldown = 0
        self.nearby_enemies = []
        self.saved_data = {}

        self.spawn_methods = {
            keys.skeleton_warrior: self.Spawn_Skeleton_Warrior,
            keys.skeleton_ranger : self.Spawn_Skeleton_Ranger,
            keys.fire_spirit : self.Spawn_Fire_Spirit,
            keys.ice_spirit : self.Spawn_Ice_Spirit,
            keys.spider : self.Spawn_Spider,
            keys.wight_king : self.Spawn_Wight_King,
            keys.skeleton_bell_toller : self.Spawn_Skeleton_Bell_Toller,
            keys.skeleton_cleric : self.Spawn_Skeleton_Cleric,
            keys.skeleton_undertaker : self.Spawn_Skeleton_Undertaker
        }


    def Save_Enemy_Data(self):
        for enemy in self.enemies:
            enemy.Save_Data()
            self.saved_data[enemy.ID] = enemy.saved_data

    def Load_Data(self, data):
        for ID, item_data in data.items():
            if not item_data:
                continue
            try:
                type = item_data[keys.type]
                pos = item_data[keys.pos]
                if item_data['category'] == keys.enemy:

                    self.Enemy_Spawner(type, pos, item_data)
                    continue
            except Exception as e:
                print("DATA WRONG", item_data, e)

    def Clear_Enemies(self):
        self.enemies.clear()
        self.nearby_enemies.clear()
        self.saved_data.clear()
        self.pathfinding_queue.clear()  # Ensure pathfinding queue is reset


    
    def Initialise(self):
        spawners = self.game.tilemap.extract([(keys.spawners, 1)])
        spawners_length = len(spawners)
        for i in range(50):
            # Spawn enemy at a random location
            spawner_index = random.randint(0, spawners_length - 1)
            spawner = spawners[spawner_index]
            enemy_types = {
                keys.skeleton_warrior: 0.39,
                keys.skeleton_ranger: 0.2,
                keys.fire_spirit: 0.05,
                keys.ice_spirit: 0.05,
                keys.spider: 0.1,
                keys.skeleton_bell_toller: 0.1,
                keys.skeleton_cleric: 0.05,
                keys.skeleton_undertaker: 0.05,
                keys.wight_king: 0.01,
            }

            type = random.choices(list(enemy_types.keys()), weights=enemy_types.values())[0]

            if type:
                # Small random varience in spawning to prevent clumping together
                pos = (spawner.pos[0] + random.randint(-10, 10), spawner.pos[1] + + random.randint(-10, 10))
                self.Enemy_Spawner(type, pos)

    
    def Enemy_Spawner(self, type, pos, data=None):
        if not type:
            print("FAIL")
            return 
        # Strip off trailing "_number" if present
        base_type = type
        parts = type.split('_')
        if parts[-1].isdigit():
            # Rebuild everything except the last part
            base_type = '_'.join(parts[:-1])

        spawn_function = self.spawn_methods.get(base_type)
        if not spawn_function:
            print(f"Warning: Enemy type '{type}' not recognized. Enemyhandler Enemy_Spawner")
            return None

        enemy = spawn_function(pos)
        if enemy:
            if data:
                enemy.Load_Data(data)  # Load saved enemy data if available
            self.enemies.append(enemy)
        return enemy

    

    def Spawn_Skeleton_Warrior(self, pos):
        health = 50
        strength = 3
        speed = 2
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
        
    def Spawn_Skeleton_Ranger(self, pos):
        health = 30
        strength = 2
        speed = 3
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
        health = 40
        strength = 3
        speed = 2
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
        health = 30
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
    
    def Spawn_Skeleton_Undertaker(self, pos):
        health = 70
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
        
        
    def Spawn_Fire_Spirit(self, pos):
        health = 60
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
        

    def Spawn_Spider(self, pos):
        health = 80
        strength = 4
        speed = 3
        agility = 3
        intelligence = 5
        stamina = 2
        return Spider(self.game,
                    pos, 
                    keys.spider,
                    health,
                    strength,
                    speed,
                    agility,
                    intelligence,
                    stamina)
    
    def Spawn_Wight_King(self, pos):
        health = 150
        strength = 3
        speed = 3
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


    def Delete_Enemy(self, enemy):
        self.game.entities_render.Remove_Entity(enemy)
        if enemy in self.enemies:
            self.enemies.remove(enemy)
        if enemy in self.pathfinding_queue:
            self.pathfinding_queue.remove(enemy) 

    def Update(self):
        self.Update_Pathfinding_Queue()
        for enemy in self.enemies:
            enemy.Update(self.game.tilemap)      
                

    def Find_Nearby_Enemies(self, entity, max_distance):
        if max_distance <= 5:
            return self.game.tilemap.Search_Nearby_Tiles(max_distance, entity.pos, keys.enemy, entity.ID)
        else:
            return self.Find_Nearby_Enemies_Long_Distance(entity, max_distance)
    
    # Long distance enemy search
    def Find_Nearby_Enemies_Long_Distance(self, entity, max_distance):
        nearby_enemies = []
        for enemy in self.enemies:
            dx = entity.pos[0] - enemy.pos[0]
            dy = entity.pos[1] - enemy.pos[1]
            if dx * dx + dy * dy < max_distance * max_distance and enemy.ID != entity.ID:
                nearby_enemies.append(enemy)
        return nearby_enemies
    
    # Add enemies to a pathfinding queue for performance and lock them in and set their destination
    def Add_To_Pathfinding_Queue(self, enemy, destination):
        if enemy in self.pathfinding_queue:
            return
        self.pathfinding_queue.append(enemy)
        enemy.Set_Destination(destination)
        enemy.Set_Locked_On_Target(2000)

    # Gradually let enemies pathfind towards the target destination
    def Update_Pathfinding_Queue(self):
        if not self.pathfinding_queue:
            return
        
        if self.pathfinding_queue_cooldown:
            self.pathfinding_queue_cooldown = max(0, self.pathfinding_queue_cooldown - 1)
            return
        
        self.pathfinding_queue_cooldown = 20
        self.pathfinding_queue[0].Find_New_Path()
        self.pathfinding_queue.pop(0)

    # Sort the pathfinding queue to simulate sound spreading
    def Sort_Pathfinding_Queue(self):
        self.pathfinding_queue.sort(
            key=lambda entity: (entity.pos[0] - self.game.player.pos[0]) ** 2 +
                            (entity.pos[1] - self.game.player.pos[1]) ** 2
        )
        


    def Find_Enemy(self, ID):
        for enemy in self.enemies:
            if enemy.ID == ID:
                return enemy
            
        return None
    
    def Get_Random_Enemy(self):
        return random.choice(self.enemies)