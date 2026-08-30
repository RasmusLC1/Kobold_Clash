from .base_animation_handler import Base_Animation_Handler


class Static_Animation_Handler(Base_Animation_Handler):
    """For entities that never animate — gold, static decoration, etc.
    Explicitly opts out of the animation cooldown loop rather than
    relying on a zero/unset value to mean the same thing."""

    def __init__(self, entity, animation_max=0, animation_cooldown_max=1):
        # cooldown_max is irrelevant here — this handler never advances frames
        super().__init__(entity, animation_max=animation_max, animation_cooldown_max=animation_cooldown_max)

    def Update_Animation(self, movement, delta_time):
        return False  # never advances — this is deliberate, not a misconfiguration