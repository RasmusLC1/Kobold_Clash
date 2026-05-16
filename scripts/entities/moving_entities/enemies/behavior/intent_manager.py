import random
from scripts.engine.keys.keys import keys
from scripts.entities.moving_entities.enemies.behavior.path_finding import Path_Finding
from scripts.entities.moving_entities.enemies.behavior.movement_strategies import Movement_Strategies
from scripts.entities.moving_entities.enemies.behavior.behavior_manager import Behavior_Manager


class Intent_Manager():
    def __init__(self, game, entity, path_finding_strategy, behavior, max_weapon_charge) -> None:
        self.game = game
        self.entity = entity

        self.path_finding = Path_Finding(game, entity, path_finding_strategy) # Pathfinding logic for enemy
        self.movement_strategies = Movement_Strategies(game, entity) # Pathfinding logic for enemy
        self.behavior_manager = Behavior_Manager(game, entity, behavior, max_weapon_charge) 




    def Save_Data(self):
        self.path_finding.Save_Data()
        self.behavior_manager.Save_Data()
        self.movement_strategies.Save_Data()


    def Load_Data(self, data):
        self.path_finding.Load_Data(data)
        self.behavior_manager.Load_Data(data)
        self.movement_strategies.Load_Data(data)

    # Update the entity's behavior
    def Update_Intent(self, delta_time):
        self.path_finding.Path_Finding(delta_time)
        self.behavior_manager.Update_Behavior(delta_time)
        self.movement_strategies.Set_Movement_Strategy(self.behavior_manager.Get_Movement_Behavior())


    def Find_New_Path(self):
        if not self.path_finding.Find_Shortest_Path():
            self.entity.target = None
            return False
        

    def Movement_Strategy(self, delta_time):
        return self.movement_strategies.Movement_Strategy(delta_time)
    
    def Get_Attack_Charge(self):
        return self.behavior_manager.Get_Attack_Charge()
    
    def Reset_Attack(self):
        return self.behavior_manager.Reset_Attack()
    
    def Set_Retreat(self):
        return self.behavior_manager.Set_Fallback_Behavior(keys.retreat)
    
    def Trigger_Instant_Attack(self):
        return self.behavior_manager.Trigger_Instant_Attack()     

    def Reset_Attack_Speed(self):
        return self.behavior_manager.Reset_Attack_Speed()
    
    def Set_Behavior_Pattern(self, pattern):
        return self.behavior_manager.Set_Behavior_Pattern(pattern)
    
    def Damage_Taken(self, damage, effect, direction, attacker):
        return self.behavior_manager.Damage_Taken(damage, effect, direction, attacker)
    
    def Reset_Behavior(self):
        return self.behavior_manager.Reset_Behavior()
    
    def Set_Ability(self, ability_name):
        return self.behavior_manager.Set_Ability(ability_name)
    
    def Render_Abilities(self, surf, offset):
        self.behavior_manager.Render_Abilities(surf, offset)