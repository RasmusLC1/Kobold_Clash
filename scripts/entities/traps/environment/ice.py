from scripts.entities.traps.trap import Trap
from ..traps.shared.shared_registry import register_trap

import random
from scripts.engine.keys.keys import keys


@register_trap(keys.ice_env) # No value as this needs to be spawned as lakes
class Ice(Trap):
    def __init__(self, game, pos, type):
        super().__init__(game, pos, type)
        self.animation = random.randint(0, 1)
        self.Set_On_Ice_Amount()


    def Apply_Entity_Effect(self, entity):
        entity.On_Ice(self.on_ice_amount)
        

    def Set_On_Ice_Amount(self):
        if self.type == keys.shallow_ice_env:
            self.on_ice_amount = 200
        elif self.type == keys.medium_ice_env:
            self.on_ice_amount = 500
        elif self.type == keys.deep_ice_env:
            self.on_ice_amount = 1000

        else:
            self.on_ice_amount = 200


