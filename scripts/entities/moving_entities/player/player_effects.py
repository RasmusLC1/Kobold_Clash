from scripts.entities.moving_entities.effects.effects_handler import Status_Effect_Handler
from scripts.entities.moving_entities.effects.player.silence import Silence
from scripts.entities.moving_entities.effects.player.soul_drained import Soul_Drained
from scripts.entities.moving_entities.effects.souls.arcane_conduit import Arcane_Conduit
from scripts.entities.moving_entities.effects.souls.arcane_hunger import Arcane_Hunger
from scripts.entities.moving_entities.effects.player.magnet import Magnet
from scripts.entities.moving_entities.effects.player.halo import Halo
from scripts.entities.moving_entities.effects.player.blood_tomb import Blood_Tomb
from scripts.entities.moving_entities.effects.player.player_movement_invunerable import Player_Movement_Invunerable
from scripts.entities.moving_entities.effects.player.power import Power
from scripts.entities.moving_entities.effects.player.demonic_bargain import Demonic_Bargain
from scripts.entities.moving_entities.effects.player.temptress_embrace import Temptress_Embrace
from scripts.entities.moving_entities.effects.souls.increase_souls import Increase_Souls
from scripts.entities.moving_entities.effects.player.luck import Luck
from scripts.entities.moving_entities.effects.player.blood_ring import Blood_Ring
from scripts.engine.keys.keys import keys
from scripts.entities.moving_entities.player.effect_icon import Effect_Icon


class Player_Status_Effect_Handler(Status_Effect_Handler):
    PLAYER_REGISTRY = {
        keys.silence: Silence,
        keys.arcane_conduit: Arcane_Conduit,
        keys.arcane_hunger: Arcane_Hunger,
        keys.magnet: Magnet,
        keys.blood_tomb: Blood_Tomb,
        keys.halo: Halo,
        keys.power: Power,
        keys.demonic_bargain: Demonic_Bargain,
        keys.temptress_embrace: Temptress_Embrace,
        keys.increase_souls: Increase_Souls,
        keys.soul_drained: Soul_Drained,
        keys.luck: Luck,
        keys.blood_ring:  Blood_Ring,
        'player_movement_invunerable': Player_Movement_Invunerable # Use key if available
    }
    
    # Combine both registries into one for this class
    EFFECT_REGISTRY = Status_Effect_Handler.EFFECT_REGISTRY | PLAYER_REGISTRY

    
    def __init__(self, entity):
        super().__init__(entity)

        self.active_effect_symbols = []

        # UI position
        self.x_pos = 20
        self.y_pos = 60
        self.y_pos_increment = 20
        self.sound_cooldown = 0
        
        self.Initalise_Effect_Icons()

    def Load_Data(self, data):
        super().Load_Data(data)

        # Load in the effect icons by iterating over all active effects
        for effect in self.active_effects:
            self.Find_Available_Effect_Icon(effect.effect_type)


    def Update_Status_Effects(self, delta_time):
        super().Update_Status_Effects(delta_time)
        self.Update_Sound_Cooldown(delta_time)

        # Reverse over the loop for safety
        for i in range(len(self.active_effect_symbols) - 1, -1, -1):
            icon = self.active_effect_symbols[i]
            if icon.Update(): 
                self.Disable_Effect_Icon(icon)

    # Prevent spamming of sound effects
    def Update_Sound_Cooldown(self, delta_time):
        if not self.sound_cooldown:
            return
        
        self.sound_cooldown = max(0, self.sound_cooldown - delta_time)
        return

    def Set_Effect(self, effect_name, duration, permanent = False):
        try:
            if not super().Set_Effect(effect_name, duration, permanent):
                return False
            
            self.Play_Sound_Effect(effect_name)

            return self.Set_Effect_Icon(effect_name)
        except Exception as e:
            print(f'FAILED TO SET PLAYER EFFECT {e}', effect_name, duration, permanent)
            return False

    def Play_Sound_Effect(self, effect):
        if self.sound_cooldown:
            return
        
        self.sound_cooldown = 0.8
        sound = self.entity.game.sound_handler
        if not sound.Check_If_Sound_Exist(effect):
            sound.Play_Sound(keys.generic_effect, 0.3)

            return
        sound.Play_Sound(effect, 0.2)


    # Check if the effect is already in the active effects before setting it
    # Prevents effect icon duplication
    def Set_Effect_Icon(self, effect):
        check_effect = self.Get_Effect(effect)
        if not check_effect:
            return False
        
        already_in_effects =  self.Check_If_Effect_Symbol_Exists(check_effect.effect_type)

        if already_in_effects:
            return True
        
        self.Find_Available_Effect_Icon(effect)

        return True
    
    def Check_If_Effect_Symbol_Exists(self, check_effect_type):
        for effect_symbol in self.active_effect_symbols:
            if effect_symbol.effect.effect_type == check_effect_type:
                return True

        return False

    # Disable a given effect_icon and remove it and shift all icons below it up
    def Disable_Effect_Icon(self, effect_icon):
        self.active_effect_symbols.remove(effect_icon)

        self.Shift_Icons_Up(effect_icon)

        effect_icon.Disable()

    def Shift_Icons_Up(self, effect_icon):
        for other_effect_icon in self.active_effect_symbols:
            if other_effect_icon.pos[1] > effect_icon.pos[1]:
                other_effect_icon.Update_Y_Position(self.y_pos_increment)   

    def Find_Available_Effect_Icon(self, effect):
        for effect_icon in self.effect_icons_pool:
            if effect_icon.effect is None:
                self.Activate_Effect_Icon(effect_icon, effect)
                return
        
        self.Spawn_Extra_Pool_Icon()
        self.Activate_Effect_Icon(self.effect_icons_pool[-1], effect)
    
    def Activate_Effect_Icon(self, effect_icon, effect):
        new_y_pos = self.y_pos + self.y_pos_increment * (len(self.active_effect_symbols) + 1)
        effect_icon.Set_Active((self.x_pos, new_y_pos), self.Get_Effect(effect))
        self.active_effect_symbols.append(effect_icon)

    # Fallback in case the icon pool needs to be increased
    def Spawn_Extra_Pool_Icon(self):
        self.effect_icons_pool.append(Effect_Icon(self.entity.game))
        self.pool_length += 1

    # Setup of icon pool for performance
    def Initalise_Effect_Icons(self):
        self.pool_length = 10
        self.effect_icons_pool = []
        for _ in range(self.pool_length):
            self.effect_icons_pool.append(Effect_Icon(self.entity.game))
            

    def Render_Effects_Symbols(self, surf):
        for effect_icon in self.active_effect_symbols:
            effect_icon.Render(surf)


