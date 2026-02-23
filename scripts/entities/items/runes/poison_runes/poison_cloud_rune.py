from scripts.entities.items.runes.rune import Rune
from scripts.entities.items.weapons.magic_attacks.poison.poison_cloud import Poison_Cloud
from scripts.engine.keys.keys import keys

class Poison_Cloud_Rune(Rune):
    def __init__(self, game, type, pos, amount, rarity_value):
        super().__init__(game, keys.poison_cloud_rune, pos, amount, rarity_value)
        self.poison_cloud = None

    def Save_Data(self):
        super().Save_Data()
        if self.poison_cloud:
            self.saved_data['delete_countdown'] = self.poison_cloud.delete_countdown
        else:
            self.saved_data['delete_countdown'] = 0
        return self.saved_data
    
    def Load_Data(self, data):
        super().Load_Data(data)
        if data['delete_countdown']:
            self.Trigger_Effect()
            self.poison_cloud.Set_Delete_Countdown(data['delete_countdown'])



    def Update(self, delta_time):
        super().Update(delta_time)
        if not self.poison_cloud:
            return
        if self.poison_cloud.delete_countdown:
            self.poison_cloud.Update(delta_time)
            self.poison_cloud.delete_countdown -= delta_time
            if self.poison_cloud.delete_countdown <= 0:
                self.game.entities_render.Remove_Entity(self.poison_cloud)

                del(self.poison_cloud)
                self.poison_cloud = None

    def Trigger_Effect(self):
        self.Trigger_Rune()
        if self.poison_cloud:
            self.poison_cloud.Set_Duration(self.power)
        else:
            self.poison_cloud = Poison_Cloud(self.game, self.game.player.pos, self.power, self.game.player)
            self.game.entities_render.Add_Entity(self.poison_cloud)

    def Render_Animation(self, surf, offset=(0, 0)):
        pass
            
