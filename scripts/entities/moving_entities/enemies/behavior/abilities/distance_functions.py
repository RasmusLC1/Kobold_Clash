from scripts.engine.keys.keys import keys
import pygame

class DistanceStrategy:
    def __init__(self, handler):
        self.handler = handler

    def check(self, max_distance, delta_time=0) -> bool:
        raise NotImplementedError


class StandardDistanceCheck(DistanceStrategy):
    def check(self, max_distance, delta_time=0) -> bool:
        return self.handler.entity.distance_to_target < max_distance


class EchoLocationDistanceCheck(DistanceStrategy):
    def __init__(self, handler):
        super().__init__(handler)
        # The timer now lives completely inside this specific ability strategy instance!
        self.echo_linger_timer = 0.0

    def check(self, max_distance, delta_time=0) -> bool:
        # 1. Physical proximity check first
        if self.handler.entity.distance_to_target >= max_distance:
            self.echo_linger_timer = 0.0
            return False

        player_moving = self._Check_Keyboard_Input()

        # 2. State evaluation machine
        if player_moving:
            self.echo_linger_timer = 5.0
            return True
        else:
            if self.echo_linger_timer > 0:
                self.echo_linger_timer -= delta_time
                return True 
            
            return False

    def _Check_Keyboard_Input(self):
        kh = self.handler.game.keyboard_handler
        return (
            kh.is_key_pressed(pygame.K_w) or 
            kh.is_key_pressed(pygame.K_a) or
            kh.is_key_pressed(pygame.K_s) or 
            kh.is_key_pressed(pygame.K_d)
        )

# Map keys directly to the strategy Classes instead of static methods
DISTANCE_REGISTRY = {
    keys.standard: StandardDistanceCheck,
    keys.echo_location: EchoLocationDistanceCheck,
}