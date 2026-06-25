from scripts.engine.keys.keys import keys

class Distance_Functions:
    @staticmethod
    def Standard_Distance_Check(handler, max_distance):
        return handler.entity.distance_to_player < max_distance

    @staticmethod
    def Echo_Location_Distance_Check(handler, max_distance):
        # Must still be close enough to hear
        if handler.entity.distance_to_player >= max_distance:
            return False
            
        # Check if player is making physical movement
        player_moving = (
            abs(handler.game.player.velocity[0]) > 0.1 or 
            abs(handler.game.player.velocity[1]) > 0.1
        )
        return player_moving

# Map keys directly to the executable logic functions
DISTANCE_REGISTRY = {
    keys.standard: Distance_Functions.Standard_Distance_Check,
    keys.echo_location: Distance_Functions.Echo_Location_Distance_Check,
}