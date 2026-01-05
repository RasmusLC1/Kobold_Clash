from scripts.entities.items.loot.loot import Loot
from scripts.engine.keys.keys import keys

# Generic passive loot that changes depending on the type, simplified to one
# class since it uses effects
class Passive_Loot(Loot):
    def __init__(self, game, type, pos, effect_power, rarity_value, loot_type=keys.passive):
        if not self.Set_Effect(type):
            return False
        self.effect_power = int(effect_power)
        super().__init__(game, type, pos, (16, 16), rarity_value=rarity_value, loot_type=loot_type)

    def Pick_Up(self):
        if not super().Pick_Up():
            return False
        
        self.game.player.Enable_Inventory_Effect(self.effect, self.effect_power)
        return True

    def Place_Down(self):
        if not super().Place_Down():
            return False
        
        self.game.player.Disable_Inventory_Effect(self.effect, self.effect_power)

        return True

    def Set_Effect(self, type):
        effects = {
            keys.magnet : keys.magnet,
            keys.compass : keys.compass,
            keys.power_totem : keys.power,
            keys.strength_totem : keys.increase_strength,
            keys.lucky_charm : keys.luck,
            keys.faith_pendant : keys.faith_pendant,
            keys.anchor_stone : keys.anchor,
            keys.muffled_boots : keys.silence,
            keys.halo : keys.halo,
        }
        
        self.effect = effects.get(type)

        if not self.effect:
            print("EFFECT NOT FOUND IN PASSIVE LOOT", self.type, self.effect)
            return False

        return True

    def Set_Description(self):
        self.description = (
                            f"{self.type} {self.effect_power}\n"
                            f"{self.Calculate_Value()} {keys.gold}\n"
                            f"rarity: {self.rarity}"
                        )
