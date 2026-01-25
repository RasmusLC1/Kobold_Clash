from scripts.engine.keys.keys import keys
import pygame

class Damage_Handler_Weapon():
    def __init__(self, weapon, effect, damage):
        self.weapon = weapon
        self.damage = {} # Damage dictionary allows many damage types on same weapon
        self.Set_Damage(effect, damage) # The damage the wepaon does

    
    def Entity_Hit(self, entity):
        weapon_entity = self.weapon.entity
        if not weapon_entity or not entity:
            return
        
        damage_sum = 0
        for damage_type in self.damage:

            damage = self.Calculate_Damage(damage_type)
            damage_sum += damage
            effect = self.Check_Effects(damage_type)
            knockback_direction = self.Calculate_Damage_Direction(entity)
            entity.Damage_Taken(damage, effect, knockback_direction)

            if entity.effects.thorns.effect:
                weapon_entity.Damage_Taken(entity.effects.thorns.effect)

        entity.Set_Damage_Cooldown()
        self.weapon.entity.effects.Damage_Dealt(damage_sum)


    def Calculate_Damage_Direction(self, entity):
        entity_pos_vec = pygame.math.Vector2(entity.pos)
        weapon_entity_pos_vec = pygame.math.Vector2(self.weapon.entity.pos)

        direction = entity_pos_vec - weapon_entity_pos_vec

        # Normalize to get unit direction (if not zero vector)
        if direction.length() != 0:
            direction = direction.normalize()

        return direction


    def Decoration_Hit(self, decoration):
        weapon_entity = self.weapon.entity
        if not weapon_entity or not decoration:
            return
        
        for damage_type in self.damage:
            damage = self.Calculate_Damage(damage_type)
            decoration.Damage_Taken(damage, damage_type)


    def Check_Effects(self, damage_type):
        damage = self.damage[damage_type]
        weapon_entity = self.weapon.entity

        if damage_type == keys.vampiric:
            weapon_entity.Set_Effect(keys.healing, damage // 4)
            return (keys.vampiric, 0) # Return vampiric with strength 0 so it's not set
        
        # Set special status effect of weapon if weapon has one
        effect_strength =  max(1, round(damage))

        return (damage_type, effect_strength)

    def Calculate_Damage(self, damage_type):
        return round(max(1, self.damage[damage_type] * (self.weapon.damage + self.weapon.entity.strength) / 2))
    
    def Get_Damage(self):
        return sum(self.damage.values())
    
    def Get_Damage_Values(self):
        return self.damage

    def Set_Damage(self, damage_type, damage):
        if damage == 0:
            return
        if damage_type in self.damage:
            self.damage[damage_type] += damage
        else:
            self.damage[damage_type] = damage


    # Iterate over the damage dictionary once and get the first key
    def Get_Dominant_Effect(self):
        if not self.damage:
            return None
        return max(self.damage, key=self.damage.get, default=None)
    
