# Profile for each behavior style
class Behavior_Profile:
    def __init__(self, behavior_function, max_dist, movement, cooldown_range, attack_distance, retreat_opts=None):
        self.behavior_function = behavior_function
        self.max_dist = max_dist # Max distance it engages with player
        self.movement = movement # String with movement
        self.cooldown_range = cooldown_range # (min, max)
        self.retreat_opts = retreat_opts # Array of options
        self.attack_distance = attack_distance # Int determines the attack distance