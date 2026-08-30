class Cooldown_Handler:
    def __init__(self, max_value=0):
        self.value = 0
        self.max_value = max_value

    # Looping cooldown
    def Update_Cooldown(self, delta_time):
        if self.value > 0:
            self.value = max(0, self.value - delta_time)
            return False
        self.Reset_Cooldown()
        return True

    # One off cooldown — caller owns what happens on expiry
    def Tick(self, delta_time):
        if self.value > 0:
            self.value = max(0, self.value - delta_time)
        return self.value <= 0

    def Reset_Cooldown(self):
        self.value = self.max_value

    def Save_Data(self):
        return {'value': self.value, 'max_value': self.max_value}

    def Load_Data(self, data):
        self.value = data['value']
        self.max_value = data['max_value']