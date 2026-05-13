
class Attack_Handler():
    def __init__(self, game, entity, max_weapon_charge):
        self.game = game
        self.entity = entity
        self.attack_triggered = False
        self.entity_has_attacked = False
        self.max_weapon_charge = max_weapon_charge
        self.max_weapon_charge_holder = max_weapon_charge
        self.charge = 0 # Determines when the enemy attacks

    def Save_Data(self):
        self.entity.saved_data['attack_triggered'] = self.attack_triggered
        self.entity.saved_data['entity_has_attacked'] = self.entity_has_attacked
        self.entity.saved_data['max_weapon_charge'] = self.max_weapon_charge
        self.entity.saved_data['charge'] = self.charge


    def Load_Data(self, data):
        self.attack_triggered = data['attack_triggered']
        self.entity_has_attacked = data['entity_has_attacked']
        self.max_weapon_charge = data['max_weapon_charge']
        self.charge = data['charge']


    def Update_Attack(self, delta_time):
        if not self.attack_triggered:
            return False
        
        self.Update_Charge(delta_time)
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


    def Set_Charge_To_Max(self):
        self.charge = self.max_weapon_charge

    def Set_Max_Weapon_Charge(self, amount):
        self.max_weapon_charge = amount
        self.entity.Set_Max_Weapon_Charge(amount)
        return True


    def Reset_Max_Weapon_Charge(self):
        self.max_weapon_charge = self.max_weapon_charge_holder
        self.entity.Set_Max_Weapon_Charge(self.max_weapon_charge_holder)
        return True



    def Update_Charge(self, delta_time):
        charge = min(self.max_weapon_charge, self.charge + delta_time)
        self.Set_Charge(charge)


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