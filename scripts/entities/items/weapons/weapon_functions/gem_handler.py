import pygame
from scripts.engine.keys.keys import keys


# TODO: Remove the entity effects when the weapon is not equipped and enable them when equipped
class Gem_Handler():
    def __init__(self, weapon):
        self.weapon = weapon
        self.gems = []
        self.max_gems = 3
        self.effects_active = False # Flag to prevent duplication of player effects
        self.entity = None
        self.gem_entity_effects = [
            keys.arcane_hunger,
            keys.halo,
            keys.power,
            keys.strength,
        ]

    def Add_Gem(self, gem):
        if len(self.gems) >= self.max_gems:
            return False
        
        self.gems.append(gem)
        self.Set_Effect(gem)
        return True
    

    # Finds and calls the various effect functions
    def Set_Effect(self, gem):
        gem_effects = {
            keys.fire : self.Set_Damage_Effect,
            keys.frozen : self.Set_Damage_Effect,
            keys.electric : self.Set_Damage_Effect,
            keys.poison : self.Set_Damage_Effect,
            keys.electric : self.Set_Damage_Effect,
            keys.vampiric : self.Set_Damage_Effect,
            keys.blunt : self.Set_Damage_Effect,
            keys.slash : self.Set_Damage_Effect,
            keys.wet : self.Set_Damage_Effect,
            keys.terror : self.Set_Damage_Effect,
            keys.vulnerable : self.Set_Damage_Effect,
            keys.weakness : self.Set_Damage_Effect,
            keys.range : self.Increase_Range,
            keys.speed : self.Increase_Speed,
            keys.durability : self.Increase_Durability,
            keys.arcane_hunger : self.Set_Entity_Effect_Gem,
            keys.halo : self.Set_Entity_Effect_Gem,
            keys.power : self.Set_Entity_Effect_Gem,
            keys.increase_strength : self.Set_Entity_Effect_Gem,
        }

        gem_function = gem_effects.get(gem.effect)
        if not gem_function:
            print("FAILED TO FIND GEM FUNCTION", gem.sub_type, gem.effect)
            return False
        
        return gem_function(gem)

    def Set_Damage_Effect(self, gem):
        self.weapon.Set_Damage(gem.effect, gem.amount)
        return True
    
    def Get_Effect_Amount(self, gem):
        return max(1, round(gem.amount))

    def Set_Entity_Effect(self, gem):
        if not self.weapon.entity.type == keys.player:
            return False
        
        self.weapon.entity.Set_Effect(gem.effect, self.Get_Effect_Amount(gem), True)
        return True
    
    # Set entity effect if player has weapon equipped. Only works for player
    def Set_Entity_Effect_Gem(self, gem):
        player = self.weapon.game.player
        
        if not player.weapon_handler.Check_If_Weapon_Is_Equipped(self.weapon):
            return False
        
        self.weapon.entity.Set_Effect(gem.effect, self.Get_Effect_Amount(gem), True)
        return True

    def Increase_Durability(self, gem):
        self.weapon.Increase_Durability(gem.amount)
        return True

    def Increase_Range(self, gem):
        self.weapon.Increase_Range(gem.amount)
        return True
    
    def Increase_Speed(self, gem):
        self.weapon.Increase_Speed(gem.amount)
        return True

    def Remove_Entity_Effect_Gems(self):
        if not self.effects_active:
            return
        self.effects_active = False
        for gem in self.gems:
            if not gem.effect in self.gem_entity_effects:
                continue
            
            self.entity.Remove_Effect(gem.effect, self.Get_Effect_Amount(gem))
        
        self.entity = None

    def Set_Entity_Effect_Gems(self):
        if self.effects_active:
            return
        
        self.entity = self.weapon.entity
        self.effects_active = True
        for gem in self.gems:
            if not gem.effect in self.gem_entity_effects:
                continue
            self.weapon.entity.Set_Effect(gem.effect, min(10, self.Get_Effect_Amount(gem)), True)

    def Increase_Max_Gems(self, amount = 1):
        self.max_gems += amount

    def Render_Effects(self, surf, offset=(0, 0)):
        for gem in self.gems:
            gem.Render_Effect(surf, offset, self.weapon.pos)


    
    def Render_Gems_Inventory(self, surf, pos, size):
        x_offset = 0
        render_scale = 8
        gem_pos_y = pos[1] + size[0] - render_scale
        for gem in self.gems:
            gem_pos_x = pos[0] + x_offset
            gem.Render_Inventory(surf, (gem_pos_x, gem_pos_y), (render_scale, render_scale))

            x_offset += render_scale

            if x_offset > size[0]:
                return