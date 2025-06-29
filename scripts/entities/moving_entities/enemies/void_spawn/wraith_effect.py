from scripts.entities.moving_entities.effects.effects_handler import Status_Effect_Handler
from scripts.entities.moving_entities.effects.enemy_effects.soul_stealer import Soul_Stealer
from scripts.engine.assets.keys import keys
from scripts.entities.moving_entities.player.effect_icon import Effect_Icon


class Wraith_Status_Effect_Handler(Status_Effect_Handler):
    def __init__(self, entity):
        super().__init__(entity)

        
    def Initialise_Effects(self):
        super().Initialise_Effects()

        self.soul_stealer =  Soul_Stealer(self.entity)
        self.effects.update({
            self.soul_stealer.effect_type: self.soul_stealer,
        })


        



