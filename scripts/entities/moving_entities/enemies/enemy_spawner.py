from scripts.engine.keys.keys import keys


class Enemy_Spawner():
    def __init__(self, game, spawn_methods, enemy_types):
        self.game = game
        self.spawn_methods = spawn_methods
        self.enemy_types = enemy_types
    

    def Get_Spawn_Function(self, base_type):
        return self.spawn_methods.get(base_type)