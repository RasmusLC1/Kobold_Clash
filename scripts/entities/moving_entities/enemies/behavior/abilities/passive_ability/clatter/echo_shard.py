from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.passive_ability import Passive_Ability
from scripts.engine.keys.keys import keys
from scripts.entities.moving_entities.enemies.behavior.abilities.registry import register_ability

INVISIBILITY_FACTOR = 6
CLATTERCOOLDOWN_MAX = 10.0


@register_ability(keys.echo_shard) # add ability to registry
class Echo_Shard(Passive_Ability):
    def __init__(self, game, entity, name):
        super().__init__(game, entity, name)
        self.clatter_cooldown = 0.01  # Trigger invisibility on first frame
        self.is_revealed = False
        
        # Subscribe to global acoustics on creation
        self.game.enemy_handler.clatter_subscription.Subscribe_To_Acoustics(self.entity)

    def Update(self, delta_time):
        super().Update(delta_time)
        
        # Only handle decay ticking every frame. No polling happens here!
        self.Handle_Cooldown(delta_time)

    # Driven purely by the event broadcaster via the Ability Handler
    def On_Clatter_Heard(self, clatter_pos):

        # Drop invisibility if they aren't already revealed
        if not self.is_revealed:
            self.entity.Remove_Effect(effect=keys.invisibility, reduce_permanent=INVISIBILITY_FACTOR)
            self.is_revealed = True
        
        # Snap the countdown back up to max (refreshes/cascades the duration)
        self.clatter_cooldown = CLATTERCOOLDOWN_MAX


    def Handle_Cooldown(self, delta_time):
        if self.clatter_cooldown <= 0:
            return
        
        self.clatter_cooldown -= delta_time
        if self.clatter_cooldown <= 0:
            # Timer hit zero! Re-apply natural stalking concealment
            self.entity.Set_Effect(effect=keys.invisibility, duration=INVISIBILITY_FACTOR, permanent=True)
            self.is_revealed = False
