from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.passive_ability import Passive_Ability
from scripts.engine.keys.keys import keys

CRYSTAL_SCALE_HEALTH_COOLDOWN_MAX = 1 # heals 1 health every second

class Crystal_Scale(Passive_Ability):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name)
        self.crystal_scale_max = entity.max_health // 4
        self.crystal_scale = self.crystal_scale_max
        self.crystal_scale_heal_cooldown = CRYSTAL_SCALE_HEALTH_COOLDOWN_MAX
        self.crystal_scale_holder = 9999
        self.crystal_scale_bar = self.game.assets[keys.crystal_scale_bar]

    def Save_Data(self):
        super().Save_Data()
        self.entity.saved_data['crystal_scale_max'] = self.crystal_scale_max
        self.entity.saved_data['crystal_scale'] = self.crystal_scale
        self.entity.saved_data['crystal_scale_heal_cooldown'] = self.crystal_scale_heal_cooldown
    
    def Load_Data(self, data):
        self.crystal_scale = data['crystal_scale']
        self.crystal_scale_max = data['crystal_scale_max']
        self.crystal_scale_heal_cooldown = data['crystal_scale_heal_cooldown']
        return super().Load_Data(data)

    def Update(self, delta_time):
        self.Heal_Crystal_Scale(delta_time)    


    def Heal_Crystal_Scale(self, delta_time):
        if self.crystal_scale == self.crystal_scale_max:
            return
        
        if self.crystal_scale_heal_cooldown <= 0:
            self.crystal_scale = min(self.crystal_scale + 1, self.crystal_scale_max)
            self.crystal_scale_heal_cooldown = CRYSTAL_SCALE_HEALTH_COOLDOWN_MAX
            return
        
        self.crystal_scale_heal_cooldown -= delta_time

    def Damage_Taken(self, damage, effect, direction, attacker):
        damage = self.Check_Crystal_Scale(damage, effect)
        return damage
    
    def Check_Crystal_Scale(self, damage, effect):
        if self.crystal_scale <= 0:  # Safer guard check
            return damage
        
        # 1. Apply modifier to a localized variable
        incoming_force = damage * 2 if effect == keys.blunt else damage

        # 2. Determine how much shield force is actually consumed
        absorbed_force = min(incoming_force, self.crystal_scale)
        self.crystal_scale -= absorbed_force
        
        # Spawn text based on the visual shield value depleted
        self.game.text_box_handler.Spawn_Damage_Text(
            self.entity.pos.copy(), keys.wet, str(absorbed_force)
        )
        
        # 3. Calculate actual breakthrough damage
        # If it was blunt, divide the unabsorbed force back by 2 to get real health damage
        unabsorbed_force = incoming_force - absorbed_force
        
        if effect == keys.blunt:
            return max(0, unabsorbed_force // 2) # Use integer division for clean health numbers
        
        return max(0, unabsorbed_force)
    


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


    def Render(self, surf, offset = (0,0)):
        self.Render_Crystal_Scale_Bar(surf, offset)
    
    def Render_Crystal_Scale_Bar(self, surf, offset):
        if not self.crystal_scale:
            return

        self.Update_Crystal_Fraction()
        entity = self.entity

        crystal_scale_bar = self.crystal_scale_bar[self.crystal_scale_index]
        surf.blit(crystal_scale_bar, (entity.rect().left - offset[0], entity.rect().bottom - offset[1] - entity.size[1] // 2 + 10))
