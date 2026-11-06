from . import registry
from . import load_all
from scripts.engine.keys.keys import keys


class Status_Effect_Handler:
    
    def __init__(self, entity):
        self.entity = entity
        self.active_effects = []
        self.instantiated_effects = {}

    def Save_Data(self):
        return {
            effect.effect_type: effect.Save_Data()
            for effect in self.active_effects
        }

    def Load_Data(self, data):
        for effect_id, effect_data in data.items():
            if not effect_data:
                continue

            effect = self.Get_Effect(effect_id)

            if not effect:
                continue
    
            try:
                effect.Load_Data(effect_data)
                if effect not in self.active_effects:
                    self.active_effects.append(effect)
            except Exception as e:
                print(f"Error loading {effect_id}: {e}")

    # Retrieve the entire effect class / instance
    def Get_Effect(self, effect_name):
        # Initial check if it's already instantiated
        if effect_name in self.instantiated_effects:
            return self.instantiated_effects[effect_name]
        
        # Look up effect class dynamically from the registry module
        effect_class = registry.EFFECT_REGISTRY.get(effect_name)

        # Check if effect exists, prevents unmapped triggers
        if not effect_class:
            return None
        
        # Instantiate new effect
        new_effect = effect_class(self.entity)
        self.instantiated_effects[effect_name] = new_effect

        return new_effect
    
    # Retrieve only the effect strength
    def Get_Effect_Strength(self, effect_name):
        effect = self.Get_Effect(effect_name)

        if not effect:
            return None
        
        return effect.effect_strength
    
    # Dynamic access fallback
    def __getattr__(self, name):
        if name not in registry.EFFECT_REGISTRY:
            raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")
        
        effect = self.Get_Effect(name)
        setattr(self, name, effect) # Future calls bypass __getattr__ entirely
        return effect

    # Set the effect of the entity
    def Set_Effect(self, effect_name, duration, permanent=False):
        # Check if entity is invulnerable
        if self.Check_Invulnerable():
            return False

        effect = self.Get_Effect(effect_name)
        if not effect:
            return False
        
        try:
            effect_set_success = effect.Set_Effect(duration, permanent)

            if effect_set_success and effect not in self.active_effects:
                self.active_effects.append(effect)

            return effect_set_success
        except Exception as e:
            print(f"Wrong effect input {e}", effect, duration, effect.effect_type)

    def Remove_Effect(self, effect, reduce_permanent=0):
        effect = self.Get_Effect(effect)
        
        if not effect:
            return False
        try:
            remove_effect_success = effect.Remove_Effect(reduce_permanent)
            if remove_effect_success:
                if effect in self.active_effects:
                    self.active_effects.remove(effect)
            return remove_effect_success 
        
        except Exception as e:
            print(f"Wrong effect input {e} EFFECT NAME", effect)

    def Check_Invulnerable(self):
        invulnerable_check = self.Get_Effect_Strength(keys.invulnerable)
        return bool(invulnerable_check)

    def Reset_Effects(self):
        for effect in self.active_effects:
            effect.Remove_Effect()

        self.active_effects.clear()

    # Use list comprehension for performance, remove effect if effect has run out
    def Update_Status_Effects(self, delta_time):
        def process_effect(effect):
            is_alive = effect.Update_Effect(delta_time)
            if not is_alive:
                effect.Remove_Effect()
            return is_alive

        self.active_effects = [effect for effect in self.active_effects if process_effect(effect)]

    def Get_Effect_Description(self, effect):
        effect = self.Get_Effect(effect)
        if not effect:
            return None
        return effect.description

    def Damage_Dealt(self, damage):
        for effect in self.active_effects:
            effect.Damage_Dealt(damage)

    def Damage_Taken(self, damage, attacker=None):
        for effect in self.active_effects:
            effect.Damage_Taken(damage, attacker)

    def Push(self, direction):
        for effect in self.active_effects:
            effect.Push(direction)

    def Entity_Dead(self):
        for effect in self.active_effects:
            effect.Entity_Dead()

    def Render_Effects(self, surf, offset=(0, 0)):
        for effect in self.active_effects:
            effect.Render_Effect(surf, offset)