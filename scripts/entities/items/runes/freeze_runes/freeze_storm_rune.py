from scripts.entities.items.runes.rune import Rune
from scripts.entities.items.weapons.magic_attacks.ice.ice_storm import Ice_Storm
from scripts.engine.keys.keys import keys


class Freeze_Storm_Rune(Rune):
    def __init__(self, game, pos):
        super().__init__(game, keys.freeze_storm_rune, pos, 1, 30)
        self.animation_time_max = 0.5
        self.animation_size_max = 15
        self.clicked = False
        self.ice_storm = None

    def Save_Data(self):
        super().Save_Data()
        if self.ice_storm:
            self.saved_data['ice_storm_duration'] = self.ice_storm.duration
        else:
            self.saved_data['ice_storm_duration'] = 0
        return self.saved_data
    
    def Load_Data(self, data):
        super().Load_Data(data)
        if data['ice_storm_duration']:
            self.Trigger_Effect()
            self.ice_storm.Reset_Duration()
            self.ice_storm.Set_Duration(data['ice_storm_duration'])



    def Update(self, delta_time):
        super().Update(delta_time)
        if not self.ice_storm:
            return
        if self.ice_storm.duration:
            self.ice_storm.Update(delta_time)
            if self.ice_storm.duration <= 0:
                self.game.entities_render.Remove_Entity(self.ice_storm)

                del(self.ice_storm)
                self.ice_storm = None

    def Trigger_Effect(self):
        self.Trigger_Rune()
        if self.ice_storm:
            self.ice_storm.Set_Duration(self.current_power * 10)
        else:
            self.ice_storm = Ice_Storm(self.game, self.game.player, self.current_power)
            self.game.entities_render.Add_Entity(self.ice_storm)

    def Render_Animation(self, surf, offset=(0, 0)):
        pass
            
