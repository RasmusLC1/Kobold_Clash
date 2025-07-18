import random

class Enemy_Pathfinding_Handler():
    def __init__(self, game):
        self.game = game
        self.pathfinding_queue = []
        self.pathfinding_queue_cooldown = 0

        self.patrol_queue_cooldown = 0
        self.patrol_queue = []

    def Update(self):
        self.Update_Pathfinding_Queue()
        self.Update_Patrol_Queue()

    # Add enemies to a pathfinding queue for performance and lock them in and set their destination
    def Add_To_Pathfinding_Queue(self, enemy, destination):
        if enemy in self.pathfinding_queue:
            return
        
        if enemy in self.patrol_queue:
            self.patrol_queue.remove(enemy)

        self.pathfinding_queue.append(enemy)
        enemy.Set_Target(destination)
        enemy.Set_Locked_On_Target(30)

    # Gradually let enemies pathfind towards the target destination
    def Update_Pathfinding_Queue(self):
        if not self.pathfinding_queue:
            return
        
        if self.pathfinding_queue_cooldown:
            self.pathfinding_queue_cooldown = max(0, self.pathfinding_queue_cooldown - 1)
            return
        
        self.pathfinding_queue_cooldown = 40
        self.pathfinding_queue[0].Find_New_Path()
        self.pathfinding_queue.pop(0)


    # Sort the pathfinding queue to simulate sound spreading
    def Sort_Pathfinding_Queue(self):
        self.pathfinding_queue.sort(
            key=lambda entity: (entity.pos[0] - self.game.player.pos[0]) ** 2 +
                            (entity.pos[1] - self.game.player.pos[1]) ** 2
        )
    

    # Seperate low priority queue for patrol to prevent patrol from clogging the active pathfinding
    def Add_To_Patrol_Queue(self, enemy):
        enemy_target = self.Get_Random_Enemy()

        if not enemy_target:
            return
        
        destination = enemy_target.pos

        if enemy in self.patrol_queue or enemy in self.pathfinding_queue:
            return
        self.patrol_queue.append(enemy)
        enemy.Set_Target(destination)
        enemy.Set_Locked_On_Target(30)

    # Gradually let enemies pathfind towards the target destination
    def Update_Patrol_Queue(self):
        if not self.patrol_queue:
            return
        
        if self.patrol_queue_cooldown:
            self.patrol_queue_cooldown = max(0, self.patrol_queue_cooldown - 1)
            return
        
        self.patrol_queue_cooldown = 100
        self.patrol_queue[0].Find_New_Path()
        self.patrol_queue.pop(0)


    def Find_Enemy(self, ID):
        enemies = self.game.enemy_handler.enemies
        for enemy in enemies:
            if enemy.ID == ID:
                return enemy
            
        return None
    
    def Get_Random_Enemy(self):
        return random.choice(self.game.enemy_handler.enemies)