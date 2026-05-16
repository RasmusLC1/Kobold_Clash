from scripts.entities.moving_entities.effects.poison.poison import Poison
from scripts.entities.moving_entities.effects.frozen.frozen import Frozen
from scripts.entities.moving_entities.effects.water.wet import Wet
from scripts.entities.moving_entities.effects.healing.regen import Regen
from scripts.entities.moving_entities.effects.movement.speed import Speed
from scripts.entities.moving_entities.effects.general.strength import Increase_Strength
from scripts.entities.moving_entities.effects.general.weakness import Weakness
from scripts.entities.moving_entities.effects.general.invisibility import Invisibility
from scripts.entities.moving_entities.effects.fire.fire_resistance import Fire_Resistance
from scripts.entities.moving_entities.effects.fire.fire import Fire
from scripts.entities.moving_entities.effects.frozen.frozen_resistance import Frozen_Resistance
from scripts.entities.moving_entities.effects.poison.poison_resistance import Poison_Resistance
from scripts.entities.moving_entities.effects.movement.snare import Snare
from scripts.entities.moving_entities.effects.movement.anchor import Anchor
from scripts.entities.moving_entities.effects.healing.healing import Healing
from scripts.entities.moving_entities.effects.healing.increase_max_health import Increase_Max_Health
from scripts.entities.moving_entities.effects.movement.slow import Slow
from scripts.entities.moving_entities.effects.healing.vampiric import Vampiric
from scripts.entities.moving_entities.effects.damage.invulnerable import Invulnerable
from scripts.entities.moving_entities.effects.damage.vulnerable import Vulnerable
from scripts.entities.moving_entities.effects.damage.thorns import Thorns
from scripts.entities.moving_entities.effects.electric.eletric import Electric
from scripts.entities.moving_entities.effects.electric.electric_resistance import Electric_Resistance
from scripts.entities.moving_entities.effects.electric.electric_charge import Electric_Charge
from scripts.entities.moving_entities.effects.general.resistance import Resistance
from scripts.engine.keys.keys import keys


class Status_Effect_Handler:
    # Instantiate the effect registry outside as a class attribute for memory effieciency
    EFFECT_REGISTRY = {
        keys.fire: Fire,
        keys.poison: Poison,
        keys.frozen: Frozen,
        keys.wet: Wet,
        keys.regen: Regen,
        keys.speed: Speed,
        keys.increase_strength: Increase_Strength,
        keys.weakness: Weakness,
        keys.invisibility: Invisibility,
        keys.fire_resistance: Fire_Resistance,
        keys.poison_resistance: Poison_Resistance,
        keys.frozen_resistance: Frozen_Resistance,
        keys.resistance: Resistance,
        keys.snare: Snare,
        keys.anchor: Anchor,
        keys.healing: Healing,
        keys.increase_max_health: Increase_Max_Health, 
        keys.slow: Slow,
        keys.vampiric: Vampiric,
        keys.invulnerable: Invulnerable,
        keys.vulnerable: Vulnerable,
        keys.thorns: Thorns,
        keys.electric: Electric,
        keys.electric_resistance: Electric_Resistance,
        keys.electric_charge: Electric_Charge,
    }

    def __init__(self, entity):
        self.entity = entity
        self.active_effects = []
        self.instantiated_effects = {}
        self.saved_data = {}

    def Save_Data(self):
        for effect in self.active_effects:
            self.saved_data[effect.effect_type] = effect.Save_Data()

        return self.saved_data


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


    # Retrieve the entire effect class
    def Get_Effect(self, effect_name):
        # Initial check if it's initalised
        if effect_name in self.instantiated_effects:
            return self.instantiated_effects[effect_name]
        
        effect_class = self.EFFECT_REGISTRY.get(effect_name, None)

        # Check if effect exists, prevents slash and blunt damage trigger
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
        
        return effect.effect
    
    
    # This only runs if 'self.name' doesn't exist yet
    def __getattr__(self, name):
        if name not in self.EFFECT_REGISTRY:
            raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")
        
        effect = self.Get_Effect(name)
        setattr(self, name, effect) # Future calls bypass __getattr__ entirely
        return effect


    # Set the effect of the entity
    def Set_Effect(self, effect_name, duration, permanent = False):
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
            print(f"Wrong effect input{e}", effect, duration, effect.effect_type)

    def Remove_Effect(self, effect, reduce_permanent = 0):
        effect = self.Get_Effect(effect)
        
        if not effect:
            return False
        try:
            remove_effect_succes = effect.Remove_Effect(reduce_permanent)
            if remove_effect_succes:
                if effect in self.active_effects:
                    self.active_effects.remove(effect)
            return remove_effect_succes 
        
        except Exception as e:
                print(f"Wrong effect input{e} EFFECT NAME", effect)

    def Check_Invulnerable(self):
        invulnerable_check = self.Get_Effect(keys.invulnerable)

        if invulnerable_check and invulnerable_check.effect:
            return True
        
        return False

    def Reset_Effects(self):
        for effect in self.active_effects:
            effect.Remove_Effect()

        self.active_effects.clear()

    # Use list comprehension for performance, remove effect if effect has run out
    def Update_Status_Effects(self, delta_time):
        def process_effect(effect): # Helper function to process the function
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

    def Damage_Taken(self, damage, attacker = None):
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