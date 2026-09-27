from scripts.entities.decoration.decoration import Decoration
from scripts.engine.keys.keys import keys
from .crystal_caverns_registry import Register_Decoration
import pygame
from scripts.engine.utility.rect_handler import Rect_Handler


@Register_Decoration(keys.amplifying_node)
class Crystalisation_Shrine(Decoration):
    def __init__(self, game, pos) -> None:
        super().__init__(game, keys.crystalisation_shrine, pos, (64, 64),
                         max_animation=4, animation_cooldown_max=1.5)
        self.description = "Exchange a gem"
        self.player_in_range = False
        self.effect_strength = 3
        self.Configure_Rect_Handlers()

    def Update(self, delta_time):
        self.Check_Player_Distance()
        return super().Update(delta_time)

    def Check_Player_Distance(self):
        player = self.game.player
        in_range_now = player.rect().colliderect(self.Rune_Amplification_Rect())

        if in_range_now == self.player_in_range:
            return  # No state change — nothing to do

        self.player_in_range = in_range_now
        if in_range_now:
            player.Set_Effect(keys.power, self.effect_strength, True)
        else:
            player.Remove_Effect(keys.power, self.effect_strength)
        return
    
    def Configure_Rect_Handlers(self):
        rect_size = self.size[0] + (DEFAULT_TRIGGER_RADIUS * 2)
        self.rune_amplification_radius = Rect_Handler(rect_size, rect_size)

    def Rune_Amplification_Rect(self):
        return self.rune_amplification_radius.rect(self.pos)