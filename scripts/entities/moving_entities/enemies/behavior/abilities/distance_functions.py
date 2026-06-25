from scripts.engine.keys.keys import keys
import pygame

class Distance_Functions:

    @staticmethod
    def Standard_Distance_Check(handler, max_distance, delta_time=0):
        return handler.entity.distance_to_player < max_distance

    @staticmethod
    def Echo_Location_Distance_Check(handler, max_distance, delta_time=0):
        # 1. Physical proximity check first
        if handler.entity.distance_to_player >= max_distance:
            # If the player is physically out of range, clear the linger window entirely
            handler.echo_linger_timer = 0
            return False
            
        # 2. Dynamic state initialization on the handler
        if not hasattr(handler, 'echo_linger_timer'):
            handler.echo_linger_timer = 0.0

        # 3. Check current snapshot input state
        kh = handler.game.keyboard_handler
        player_moving = (
            kh.is_key_pressed(pygame.K_w) or 
            kh.is_key_pressed(pygame.K_a) or
            kh.is_key_pressed(pygame.K_s) or 
            kh.is_key_pressed(pygame.K_d)
        )

        # 4. State evaluation machine
        if player_moving:
            # Reset/refresh the 1-second retention window
            handler.echo_linger_timer = 5.0
            return True
        else:
            # Decay the retention window cleanly frame-by-frame
            if handler.echo_linger_timer > 0:
                handler.echo_linger_timer -= delta_time
                return True # Player is still tracked during the fade window
            
            return False # Window closed; target completely lost
        

# Map keys directly to the executable logic functions
DISTANCE_REGISTRY = {
    keys.standard: Distance_Functions.Standard_Distance_Check,
    keys.echo_location: Distance_Functions.Echo_Location_Distance_Check,
}