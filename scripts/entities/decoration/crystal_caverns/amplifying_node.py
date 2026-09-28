from scripts.entities.decoration.decoration import Decoration
from scripts.engine.keys.keys import keys
from .crystal_caverns_registry import Register_Decoration
from scripts.engine.utility.rect_handler import Rect_Handler

DEFAULT_TRIGGER_RADIUS = 200  # Pixels padded around each side of the node
DEFAULT_EFFECT_STRENGTH = 3


@Register_Decoration(keys.amplifying_node)
class Amplifying_Node(Decoration):
    def __init__(self, game, pos) -> None:
        super().__init__(game, keys.amplifying_node, pos, (32, 32),
                         max_animation=4, animation_cooldown_max=1.2)
        self.description = "Resonant energies\nAmplifies Runes"
        self.trigger_radius = DEFAULT_TRIGGER_RADIUS
        self.effect_strength = DEFAULT_EFFECT_STRENGTH
        self.player_in_range = False
        self.applied_strength = 0
        self.Configure_Rect_Handlers()

    def Update(self, delta_time):
        self.Check_Player_Distance()
        return super().Update(delta_time)

    def Check_Player_Distance(self) -> None:
        player = self.game.player
        in_range_now = player.rect().colliderect(self.Rune_Amplification_Rect())

        if in_range_now == self.player_in_range:
            return

        if in_range_now:
            self.Apply_Amplification()
        else:
            self.Remove_Amplification()

    def Apply_Amplification(self) -> None:
        self.player_in_range = True
        self.applied_strength = self.effect_strength
        self.game.player.Set_Effect(keys.power, self.applied_strength, True)

    # TODO: ENSURE THIS IS CALLED EVEN IF PLAYER TELEPORTS AWAY
    def Remove_Amplification(self) -> None:
        if not self.player_in_range:
            return
        self.player_in_range = False
        self.game.player.Remove_Effect(keys.power, self.applied_strength)
        self.applied_strength = 0

    def Configure_Rect_Handlers(self) -> None:
        width = self.size[0] + self.trigger_radius * 2
        height = self.size[1] + self.trigger_radius * 2
        self.rune_amplification_area = Rect_Handler(width, height)

    def Rune_Amplification_Rect(self):
        # Offset so the area is centred on the node, assuming Rect_Handler.rect()
        # anchors at the given position. Remove the offset if it already centres.
        return self.rune_amplification_area.rect(
            (self.pos[0] - self.trigger_radius, self.pos[1] - self.trigger_radius)
        )