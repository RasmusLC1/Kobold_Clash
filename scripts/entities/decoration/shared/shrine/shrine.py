from scripts.entities.decoration.decoration import Decoration
import random

class Shrine(Decoration):
    """Common base for all shrine decorations."""

    def __init__(self, game, type, pos, size=(64, 64), max_animation=0,
                 animation_cooldown_max=0, **kwargs) -> None:
        super().__init__(game, type, pos, size, max_animation=max_animation,
                         animation_cooldown_max=animation_cooldown_max)

    def Activate_Shrine(self):
        """Bookkeeping shared by shrines when successfully interacted with."""
        self.game.player.Set_Last_Shrine(self)


class Cycling_Shrine(Shrine):
    """Shrines that continuously loop an idle animation on a randomized cooldown."""

    def __init__(self, game, type, pos, size=(64, 64),
                 particle_type=None, particle_chance=0, particle_time_range=(1.5, 2.0),
                 max_animation=0,
                animation_cooldown_max=0) -> None:
        super().__init__(game, type, pos, size, max_animation=max_animation,
                         animation_cooldown_max=animation_cooldown_max)
        self.particle_type = particle_type
        self.particle_chance = particle_chance
        self.particle_time_range = particle_time_range

    def Update_Animation(self, delta_time):
        if not super().Update_Animation(delta_time):
            return False

        self.Maybe_Spawn_Particles()
        return True


    def Maybe_Spawn_Particles(self):
        if not self.particle_type or self.particle_chance <= 0:
            return
        if random.randint(0, self.particle_chance) == 0:
            self.game.particle_handler.Activate_Particles(
                random.randint(2, 4), self.particle_type, self.rect().center,
                time=random.uniform(*self.particle_time_range)
            )

class Menu_Shrine(Shrine):
    """Shrines that open into a dedicated menu state (rune selection, portal travel)."""

    def __init__(self, game, type, pos, size=(64, 64), max_animation = 0, animation_cooldown_max=0.0,
                 cycle_requires_open=True) -> None:
        super().__init__(game, type, pos, size, max_animation=max_animation,
                         animation_cooldown_max=animation_cooldown_max)
        self.is_open = False
        self.cycle_requires_open = cycle_requires_open

    def Save_Data(self):
        super().Save_Data()
        self.saved_data['is_open'] = self.is_open

    def Load_Data(self, data):
        super().Load_Data(data)
        self.is_open = data['is_open']

    def Update_Animation(self, delta_time):
        if self.cycle_requires_open and not self.is_open:
            return False
        return super().Update_Animation(delta_time)
        