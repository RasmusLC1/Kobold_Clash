
from scripts.entities.moving_entities.enemies.crypt.crypt_spawn import Crypt_Spawn
from scripts.entities.moving_entities.enemies.crystal_caverns.crystal_cavern_spawn import Crystal_Cavern_Spawn
from scripts.entities.moving_entities.enemies.enemy_pathfinding_handler import Enemy_Pathfinding_Handler
from scripts.engine.keys.keys import keys
import math
import random

class Enemy_Handler():
    def __init__(self, game):
        self.game = game
        self.enemy_spawner = None
        self.enemies = []
        self.pathfinding_handler = Enemy_Pathfinding_Handler(game)
        self.nearby_enemies = []
        self.saved_data = {}


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

                    self.Enemy_Spawner(pos, type, item_data)
                    continue
            except Exception as e:
                print("DATA WRONG", item_data, e)

    def Clear_Enemies(self):
        self.enemies.clear()
        self.nearby_enemies.clear()
        self.saved_data.clear()
        self.pathfinding_handler.pathfinding_queue.clear()  # Ensure pathfinding queue is reset


    
    def Initialise(self):
        spawners = self.game.tilemap.extract([(keys.spawners, 1)])
        spawners_length = len(spawners)

        self.Set_Spawner_Type()


        
        for i in range(10):
            # Spawn enemy at a random location
            spawner_index = random.randint(0, spawners_length - 1)
            spawner = spawners[spawner_index]

            type = self.Get_Random_Enemy_Type()

            if type:
                spawner_pos = spawner[keys.pos]
                # Small random varience in spawning to prevent clumping together
                pos = (spawner_pos[0] + random.randint(-10, 10), spawner_pos[1] + random.randint(-10, 10))
                self.Enemy_Spawner(pos, type)


    def Set_Spawner_Type(self):
        spawner_types = {
            keys.ancient_crypt : Crypt_Spawn,
            keys.crystal_caverns : Crystal_Cavern_Spawn
        }

        spawner_type = spawner_types.get(self.game.dungeon_type)

        self.enemy_spawner = spawner_type(self.game)

    def Get_Random_Enemy_Type(self) :
        type = random.choices(list(self.enemy_spawner.enemy_types.keys()),
                              weights=list(self.enemy_spawner.enemy_types.values()))[0]
        return type

    
    def Enemy_Spawner(self, pos, type = None, data=None):
        if not type:
            type = self.Get_Random_Enemy_Type()
        
        if len(self.enemies) > 50:
            return True
        
        # Strip off trailing "_number" if present
        base_type = type
        parts = type.split('_')
        if parts[-1].isdigit():
            # Rebuild everything except the last part
            base_type = '_'.join(parts[:-1])

        spawn_function = self.enemy_spawner.Get_Spawn_Function()
        if not spawn_function:
            print(f"Warning: Enemy type '{type}' not recognized. Enemyhandler Enemy_Spawner")
            return None

        enemy = spawn_function(pos)
        if enemy:
            if data:
                enemy.Load_Data(data)  # Load saved enemy data if available
            self.enemies.append(enemy)
            self.Add_To_Patrol_Queue(enemy)
        return enemy
    

    def Delete_Enemy(self, enemy):
        self.game.entities_render.Remove_Entity(enemy)
        if enemy in self.enemies:
            self.enemies.remove(enemy)
        if enemy in self.pathfinding_handler.pathfinding_queue:
            self.pathfinding_handler.pathfinding_queue.remove(enemy) 


    def Update(self, delta_time):
        self.pathfinding_handler.Update()
        for enemy in self.enemies:
            enemy.Update(self.game.tilemap, delta_time)      

    def Get_Number_Of_Enemies(self):
        return len(self.enemies)

    # Split the search, use tiles for short distance as it's faster, but distance for longer
    # as it has constant runtime
    def Find_Nearby_Enemies(self, entity, max_distance):
        if max_distance <= 5:
            return self.game.tilemap.Search_Nearby_Tiles(max_distance, entity.pos, keys.enemy, entity.ID)
        else:
            return self.Find_Nearby_Enemies_Long_Distance(entity, max_distance)
   
    
    # Long distance enemy search
    def Find_Nearby_Enemies_Long_Distance(self, entity, max_distance):
        nearby_enemies = []
        max_distance_squared = max_distance * max_distance
        for enemy in self.enemies:
            distance = (enemy.pos[0] - entity.pos[0]) ** 2 + (enemy.pos[1] - entity.pos[1]) ** 2
            if distance < max_distance_squared and enemy.ID != entity.ID:
                nearby_enemies.append(enemy)
        return nearby_enemies
    
   
    # Add enemies to a pathfinding queue for performance and lock them in and set their destination
    def Add_To_Pathfinding_Queue(self, enemy, destination):
        self.pathfinding_handler.Add_To_Pathfinding_Queue(enemy, destination)
        # Sort the queue once everything has been added
        self.pathfinding_handler.Sort_Pathfinding_Queue()

   
    # Seperate low priority queue for patrol to prevent patrol from clogging the active pathfinding
    def Add_To_Patrol_Queue(self, enemy):
        self.pathfinding_handler.Add_To_Patrol_Queue(enemy)

