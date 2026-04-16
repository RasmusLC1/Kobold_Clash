from scripts.entities.moving_entities.enemies.attacks.Dash import Dash
from scripts.entities.moving_entities.enemies.attacks.Jump_Attack import Jump_Attack

from scripts.engine.keys.keys import keys


class Special_Attack_Handler():
    def __init__(self, game, entity):
        self.game = game
        self.entity = entity
        self.special_attacks = {}
        self.special_attacks_cooldown = 0 

    def Add_Special_Attack(self, key_trigger):
        # Define the mapping of keys to Classes (not instances)
        lookup = {
            keys.Dash: Dash,
            keys.jump: Jump_Attack
        }

        # Get the class based on the key passed
        attack_class = lookup.get(key_trigger)

        if attack_class:
            # Instantiate the attack and store it with its key
            self.special_attacks[key_trigger] = attack_class(self.game, self.entity)
        else:
            print(f"Attack for {key_trigger} not found.")


    def Handle_Dash(self):
        if not self.dash.dashing:
            self.dash.Dash()

        self.dash.Dashing_Update()

        if self.dash.dashing == 1:
            self.Increment_Intent()
            self.entity.Set_Charge_To_Max()
        return
