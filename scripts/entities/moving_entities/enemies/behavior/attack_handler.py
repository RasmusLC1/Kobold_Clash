
class Attack_Handler():
    def __init__(self, game, entity, max_weapon_charge):
        self.game = game
        self.entity = entity
        self.attack_triggered = False
        self.entity_has_attacked = False
        self.max_weapon_charge = max_weapon_charge
        self.charge = 0 # Determines when the enemy attacks

    def Update_Attack(self, delta_time):
        if not self.attack_triggered:
            return False
        
        self.Set_Charge(min(self.max_weapon_charge, self.charge + delta_time))

        return True


    def Set_Attack_Triggered(self, state):
        self.attack_triggered = state

    def Set_Entity_Has_Attacked(self, state):
        self.entity_has_attacked = state

    def Get_Entity_Has_Attacked(self):
        return self.entity_has_attacked
    
    def Check_Attack_Direction(self, attack_direction):
        if not attack_direction:
            self.Set_Target()
            attack_direction = self.target

        return attack_direction


    # TODO: USED FOR DASH ATTACKS, not implemented yet, migrated from enemies class
    def Set_Charge_To_Max(self):
        self.charge = self.max_weapon_charge


    def Set_Charge(self, amount):
        self.charge = amount
        self.entity.Set_Charge(amount) # Sync the player charge for animation purpose

    def Get_Attack_Charge(self):
        return self.charge
    

    def Reset_Attack(self):
        self.Set_Charge(0)
        self.attack_triggered = False
        self.Set_Entity_Has_Attacked(True)

    def Get_Attack_Triggered(self):
        return self.attack_triggered