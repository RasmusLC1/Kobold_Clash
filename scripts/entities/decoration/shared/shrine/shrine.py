from scripts.entities.decoration.decoration import Decoration
import random


class Shrine(Decoration):
    """Common base for all shrine decorations."""

    def __init__(self, game, type, pos, size=(64, 64), **kwargs) -> None:
        super().__init__(game, type, pos, size, **kwargs)

    def Activate_Shrine(self):
        """Bookkeeping shared by shrines when successfully interacted with."""
        self.game.player.Set_Last_Shrine(self)


class Cycling_Shrine(Shrine):
    """Shrines that continuously loop an idle animation on a randomized cooldown."""

    def __init__(self, game, type, pos, size=(64, 64), cooldown_range=(0.5, 0.7),
                 particle_type=None, particle_chance=0, particle_time_range=(1.5, 2.0),
                 **kwargs) -> None:
        super().__init__(game, type, pos, size, **kwargs)
        self.animation_cooldown = 0
        self.cooldown_range = cooldown_range
        self.particle_type = particle_type
        self.particle_chance = particle_chance
        self.particle_time_range = particle_time_range

    def Update(self, delta_time):
        self.Update_Animation(delta_time)
        return super().Update(delta_time)

    def Update_Animation(self, delta_time):
        if not self.Animation_Cooldown_Handler(delta_time):
            return

        if self.animation >= self.max_animation:
            self.Set_Animation(0)
        else:
            self.Set_Animation(self.animation + 1)

        self.Maybe_Spawn_Particles()

    def Animation_Cooldown_Handler(self, delta_time):
        if self.animation_cooldown <= 0:
            self.animation_cooldown = random.uniform(*self.cooldown_range)
            return True
        self.animation_cooldown -= delta_time
        return False

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

    def __init__(self, game, type, pos, size=(64, 64), animation_cooldown_max=0.3,
                 cycle_requires_open=True, **kwargs) -> None:
        super().__init__(game, type, pos, size, **kwargs)
        self.is_open = False
        self.animation_cooldown = 0
        self.animation_cooldown_max = animation_cooldown_max
        self.min_animation = 0
        self.max_animation = 0
        self.cycle_requires_open = cycle_requires_open

    def Save_Data(self):
        super().Save_Data()
        self.saved_data['is_open'] = self.is_open

    def Load_Data(self, data):
        super().Load_Data(data)
        self.is_open = data['is_open']

    def Update(self, delta_time):
        self.Update_Animation(delta_time)
        return super().Update(delta_time)

    def Update_Animation(self, delta_time):
        if self.cycle_requires_open and not self.is_open:
            return
        if self.animation_cooldown > 0:
            self.animation_cooldown -= delta_time
        else:
            self.animation_cooldown = self.animation_cooldown_max
            self.Set_Animation(random.randint(self.min_animation, self.max_animation))