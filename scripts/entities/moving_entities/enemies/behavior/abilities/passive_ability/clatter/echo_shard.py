from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.passive_ability import Passive_Ability
from scripts.engine.keys.keys import keys

INVISIBILITY_FACTOR = 6
CLATTERCOOLDOWN_MAX = 10.0

class Echo_Shard(Passive_Ability):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name)
        self.clatter_cooldown = 0.01 # Trigger invisibility on first frame
        self.is_revealed = False

    def Update(self, delta_time):
        # Always update the base tick smoothly
        super().Update(delta_time)

        # 1. Handle ticking down the reveal window
        self.Handle_Cooldown(delta_time)

        # 2. Check for acoustics every frame (allows resetting/refreshing the timer)
        self.Handle_Clatter()

    def Handle_Clatter(self):
        clatter_pos = self.game.clatter.Check_If_Noise_Generated()
        if not clatter_pos:
            return
        # Drop invisibility if they aren't already revealed
        if not self.is_revealed:
            self.entity.Remove_Effect(effect=keys.invisibility, reduce_permanent=INVISIBILITY_FACTOR)
            self.is_revealed = True
        
        # Snap the countdown back up to max (refreshes the 10s duration)
        self.clatter_cooldown = CLATTERCOOLDOWN_MAX

    def Handle_Cooldown(self, delta_time):
        if self.clatter_cooldown <= 0:
            return
        
        self.clatter_cooldown -= delta_time
        if self.clatter_cooldown <= 0:
            # Timer just hit zero! Re-apply natural stalking concealment
            self.entity.Set_Effect(effect=keys.invisibility, duration=INVISIBILITY_FACTOR, permanent=True)
            self.is_revealed = False