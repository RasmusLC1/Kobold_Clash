from scripts.entities.moving_entities.effects.effects_handler import Status_Effect_Handler
from scripts.entities.moving_entities.effects.player.player_registry import EFFECTS_REGISTRY, register_effect
from scripts.entities.moving_entities.effects.player import load_all
from scripts.engine.keys.keys import keys
from scripts.entities.moving_entities.player.effect_icon import Effect_Icon


class Player_Status_Effect_Handler(Status_Effect_Handler):

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

        for effect in self.active_effects:
            self.Find_Available_Effect_Icon(effect.effect_type)

    def Update_Status_Effects(self, delta_time):
        super().Update_Status_Effects(delta_time)
        self.Update_Sound_Cooldown(delta_time)

        for i in range(len(self.active_effect_symbols) - 1, -1, -1):
            icon = self.active_effect_symbols[i]
            if icon.Update():
                self.Disable_Effect_Icon(icon)

    def Update_Sound_Cooldown(self, delta_time):
        if not self.sound_cooldown:
            return

        self.sound_cooldown = max(0, self.sound_cooldown - delta_time)

    def Set_Effect(self, effect_name, duration, permanent=False):
        try:
            if not super().Set_Effect(effect_name, duration, permanent):
                return False

            self.Play_Sound_Effect(effect_name)
            return self.Set_Effect_Icon(effect_name)
        except Exception as e:
            print(f"FAILED TO SET PLAYER EFFECT {e}", effect_name, duration, permanent)
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

    def Set_Effect_Icon(self, effect):
        check_effect = self.Get_Effect(effect)
        if not check_effect:
            return False

        if self.Check_If_Effect_Symbol_Exists(check_effect.effect_type):
            return True

        self.Find_Available_Effect_Icon(effect)
        return True

    def Check_If_Effect_Symbol_Exists(self, check_effect_type):
        return any(symbol.effect.effect_type == check_effect_type for symbol in self.active_effect_symbols)

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

    def Spawn_Extra_Pool_Icon(self):
        self.effect_icons_pool.append(Effect_Icon(self.entity.game))
        self.pool_length += 1

    def Initalise_Effect_Icons(self):
        self.pool_length = 10
        self.effect_icons_pool = [Effect_Icon(self.entity.game) for _ in range(self.pool_length)]

    def Render_Effects_Symbols(self, surf):
        for effect_icon in self.active_effect_symbols:
            effect_icon.Render(surf)