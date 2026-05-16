from scripts.entities.moving_entities.enemies.enemy import Enemy
from scripts.engine.keys.keys import keys

CRYSTAL_SCALE_HEALTH_COOLDOWN_MAX = 1 # heals 1 health every second

class Elemental(Enemy):
    def __init__(self, game, pos, type):
        super().__init__(game, pos, type)
        self.crystal_scale_max = self.max_health // 4
        self.crystal_scale = self.crystal_scale_max
        self.crystal_scale_heal_cooldown = CRYSTAL_SCALE_HEALTH_COOLDOWN_MAX
        self.crystal_scale_holder = 9999
        self.touching_ground = False
        self.crystal_scale_bar = self.game.assets[keys.crystal_scale_bar]


    def Save_Data(self):
        super().Save_Data()
        self.saved_data['crystal_scale_max'] = self.crystal_scale_max
        self.saved_data['crystal_scale'] = self.crystal_scale
    
    def Load_Data(self, data):
        self.crystal_scale = data['crystal_scale']
        self.crystal_scale_max = data['crystal_scale_max']
        return super().Load_Data(data)

    def Update(self, tilemap, delta_time, movement = (0, 0)):
        super().Update(tilemap, delta_time, movement)
        self.Heal_Crystal_Scale(delta_time)
        
    
    def Heal_Crystal_Scale(self, delta_time):
        if self.crystal_scale == self.crystal_scale_max:
            return
        
        if self.crystal_scale_heal_cooldown <= 0:
            self.crystal_scale = min(self.crystal_scale + 1, self.crystal_scale_max)
            self.crystal_scale_heal_cooldown = CRYSTAL_SCALE_HEALTH_COOLDOWN_MAX
            return
        
        self.crystal_scale_heal_cooldown -= delta_time


    def Damage_Taken(self, damage, effect = (keys.slash, 0), direction = (0, 0), attacker = None):
        damage = self.Check_Crystal_Scale(damage)
        return super().Damage_Taken(damage, effect, direction, attacker)
    
    def Check_Crystal_Scale(self, damage):
        if self.crystal_scale < 0:
            return damage
        
        absorbed = min(damage, self.crystal_scale)
        damage -= absorbed
        self.crystal_scale -= absorbed
        self.Set_Damaged(True)
        # TODO: ADD Special shield color text, currently using water as temp
        self.game.text_box_handler.Spawn_Damage_Text(self.pos.copy(), keys.wet, str(absorbed))
        return damage

    def Update_Crystal_Fraction(self):
        if self.crystal_scale == self.crystal_scale_holder:
            return
        # Correct potential rounding issues at full health
        if self.crystal_scale == self.crystal_scale_max:
            self.crystal_scale_index = 0

        self.crystal_scale_holder = self.crystal_scale
        crystal_scale_fraction = self.crystal_scale / self.crystal_scale_max

        # Map the fraction to an index from 0 to 9 (assuming 10 total images)
        self.crystal_scale_index = max(-1, min(int((1 - crystal_scale_fraction) * 9), 9))  # Invert fraction and scale to index range

        
    def Render_Health_Bar(self, surf, offset = (0,0)):
        super().Render_Health_Bar(surf, offset)
        self.Render_Crystal_Scale_Bar(surf, offset)
    
    def Render_Crystal_Scale_Bar(self, surf, offset):
        if not self.crystal_scale:
            return

        self.Update_Crystal_Fraction()


        crystal_scale_bar = self.crystal_scale_bar[self.crystal_scale_index]
        surf.blit(crystal_scale_bar, (self.rect().left - offset[0], self.rect().bottom - offset[1] - self.size[1] // 2 + 10))
