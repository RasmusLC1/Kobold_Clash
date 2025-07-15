from scripts.entities.moving_entities.effects.poison.poison import Poison
from scripts.entities.moving_entities.effects.frozen.frozen import Frozen
from scripts.entities.moving_entities.effects.water.wet import Wet
from scripts.entities.moving_entities.effects.healing.regen import Regen
from scripts.entities.moving_entities.effects.movement.speed import Speed
from scripts.entities.moving_entities.effects.general.increase_strength import Increase_Strength
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
from scripts.entities.moving_entities.effects.general.resistance import Resistance
from scripts.engine.keys.keys import keys



class Status_Effect_Handler:

    def __init__(self, entity):
        self.entity = entity

        self.Initialise_Effects()       

        self.active_effects = []
        
        self.is_on_ice = 0
        self.saved_data = {}

    def Save_Data(self):
        for effect in self.active_effects:
            self.saved_data[effect.effect_type] = effect.Save_Data()

        return self.saved_data


    def Load_Data(self, data):
        for ID, effect_data in data.items():
            if not effect_data:
                continue
            
            if not ID in self.effects:
                continue
            try:
                self.effects[ID].Load_Data(effect_data)
                self.active_effects.append(self.effects[ID])
            except Exception as e:
                print(f"Wrong loaded data{e}", effect_data, ID)

    
    # Used to initialise effects so different entities can have different effects
    # Keep unique self.fire etc for easy callback since they are widely used,
    # Improves performance as it removes search and easier to build with
    def Initialise_Effects(self):
        self.fire = Fire(self.entity)

        self.poison = Poison(self.entity)
        
        self.frozen = Frozen(self.entity)

        self.wet = Wet(self.entity)

        self.regen = Regen(self.entity)
        
        self.speed = Speed(self.entity)

        self.increase_strength = Increase_Strength(self.entity)
        
        self.weakness = Weakness(self.entity)

        self.invisibility = Invisibility(self.entity)
        
        self.fire_resistance = Fire_Resistance(self.entity)

        self.poison_resistance = Poison_Resistance(self.entity)
        
        self.frozen_resistance = Frozen_Resistance(self.entity)

        self.resistance = Resistance(self.entity)

        self.snare = Snare(self.entity)

        self.anchor = Anchor(self.entity)

        self.healing = Healing(self.entity)

        self.increase_max_health = Healing(self.entity)

        
        self.slow = Slow(self.entity)
        
        self.vampiric = Vampiric(self.entity)

        self.invulnerable = Invulnerable(self.entity)
        
        self.vulnerable = Vulnerable(self.entity)

        self.thorns = Thorns(self.entity)

        self.electric = Electric(self.entity)

        self.electric_resistance = Electric_Resistance(self.entity)

        self.effects = {
            self.fire.effect_type: self.fire,
            self.poison.effect_type: self.poison,
            self.frozen.effect_type: self.frozen,
            self.wet.effect_type: self.wet,
            self.regen.effect_type: self.regen,
            self.speed.effect_type: self.speed,
            self.increase_strength.effect_type: self.increase_strength,
            self.weakness.effect_type: self.weakness,
            self.invisibility.effect_type: self.invisibility,
            self.fire_resistance.effect_type: self.fire_resistance,
            self.poison_resistance.effect_type: self.poison_resistance,
            self.frozen_resistance.effect_type: self.frozen_resistance,
            self.resistance.effect_type: self.resistance,
            self.snare.effect_type: self.snare,
            self.anchor.effect_type: self.anchor,
            self.healing.effect_type: self.healing,
            self.increase_max_health.effect_type: self.increase_max_health,
            self.slow.effect_type: self.slow,
            self.vampiric.effect_type: self.vampiric,
            self.invulnerable.effect_type: self.invulnerable,
            self.vulnerable.effect_type: self.vulnerable,
            self.thorns.effect_type: self.thorns,
            self.electric.effect_type: self.electric,
            self.electric_resistance.effect_type: self.electric_resistance,
            'slash': None,
            'blunt': None,
        }


    # Set the effect of the entity
    def Set_Effect(self, effect, duration, permanent = False):
        if self.entity.effects.invulnerable.effect:
            return False
        try:
            effect = self.effects.get(effect)
            
            if not effect:
                return False
            effect_set_success = effect.Set_Effect(duration, permanent)
            if effect_set_success:
                effect_found = False

                for active_effect in self.active_effects:
                    # Check if the type is in effects and skip if yes
                    if effect.effect_type == active_effect.effect_type:
                        effect_found = True
                        break
                
                if not effect_found:
                    self.active_effects.append(effect)
            return effect_set_success
        except Exception as e:
            print(f"Wrong effect input{e}", effect, duration, effect.effect_type)


    def Reset_Effects(self):
        for effect in self.active_effects:
            effect.Remove_Effect()
            self.active_effects.remove(effect)

    # Use list comprehension for performance, remove effect if effect has run out
    def Update_Status_Effects(self):
        self.active_effects = [effect for effect in self.active_effects if effect.Update_Effect()]


    def Get_Effect_Description(self, effect):
        effect = self.effects[effect]
        if not effect:
            return None
        
        return effect.description
    
    def Get_Effect(self, effect):
        return self.effects.get(effect)

    def Remove_Effect(self, effect, reduce_permanent = 0):

        effect = self.effects[effect]
        
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


    def Damage_Dealt(self, damage):
        for effect in self.active_effects:
            effect.Damage_Dealt(damage)

    def Damage_Taken(self, damage):
        for effect in self.active_effects:
            effect.Damage_Taken(damage)

    def Push(self, direction):
        for effect in self.active_effects:
            effect.Push(direction)

    def Entity_Dead(self):
        for effect in self.active_effects:
            effect.Entity_Dead()


    def Render_Effects(self, surf, offset=(0, 0)):
        for effect in self.active_effects:
            effect.Render_Effect(surf, offset)