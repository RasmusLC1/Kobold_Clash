# Import all effect classes
from scripts.entities.moving_entities.player.inventory_effects.blood_tomb import Blood_Tomb
from scripts.entities.moving_entities.player.inventory_effects.magnet import Magnet
from scripts.entities.moving_entities.player.inventory_effects.compass import Compass
from scripts.entities.moving_entities.player.inventory_effects.power_totem import Power_Totem
from scripts.entities.moving_entities.player.inventory_effects.strength_totem import Strength_Totem
from scripts.entities.moving_entities.player.inventory_effects.luck_totem import Luck_Totem
from scripts.entities.moving_entities.player.inventory_effects.faith_pendant import Faith_Pendant
from scripts.entities.moving_entities.player.inventory_effects.anchor_stone import Anchor_Stone
from scripts.entities.moving_entities.player.inventory_effects.muffled_boots import Muffled_Boots
from scripts.entities.moving_entities.player.inventory_effects.halo import Halo
from scripts.entities.moving_entities.player.inventory_effects.black_coin import Black_Coin
from scripts.entities.moving_entities.player.inventory_effects.vampire_locket import Vampire_Locket
from scripts.entities.moving_entities.player.inventory_effects.blood_pact import Blood_Pact
from scripts.entities.moving_entities.player.inventory_effects.demonic_bargain import Demonic_Bargain
from scripts.entities.moving_entities.player.inventory_effects.temptress_embrace import Temptress_Embrace
from scripts.entities.moving_entities.player.inventory_effects.cursed_dice import Cursed_Dice
from scripts.entities.moving_entities.player.inventory_effects.eldritch_mirror import Eldritch_Mirror
from scripts.entities.moving_entities.player.inventory_effects.forsaken_grimoire import Forsaken_Grimoire
from scripts.entities.moving_entities.player.inventory_effects.cracked_talisman import Cracked_Talisman
from scripts.entities.moving_entities.player.inventory_effects.echoing_skull import Echoing_Skull
from scripts.engine.keys.keys import keys


class Inventory_Effects_Handler:
    """Handles inventory effects for an entity."""
    
    def __init__(self, entity):
        self.entity = entity

        # Instantiate effect objects with their name
        self.effects = {
            keys.blood_tomb: Blood_Tomb(self.entity),
            keys.magnet: Magnet(self.entity),
            "compass": Compass(self.entity),
            "power_totem": Power_Totem(self.entity),
            "strength_totem": Strength_Totem(self.entity),
            "luck_totem": Luck_Totem(self.entity),
            "faith_pendant": Faith_Pendant(self.entity),
            "anchor_stone": Anchor_Stone(self.entity),
            "muffled_boots": Muffled_Boots(self.entity),
            keys.halo: Halo(self.entity),
            "black_coin": Black_Coin(self.entity),
            "vampire_locket": Vampire_Locket(self.entity),
            "blood_pact": Blood_Pact(self.entity),
            keys.demonic_bargain: Demonic_Bargain(self.entity),
            keys.temptress_embrace: Temptress_Embrace(self.entity, ),
            "cursed_dice": Cursed_Dice(self.entity, ),
            "eldritch_mirror": Eldritch_Mirror(self.entity),
            "forsaken_grimoire": Forsaken_Grimoire(self.entity),
            "cracked_talisman": Cracked_Talisman(self.entity),
            "echoing_skull": Echoing_Skull(self.entity),
        }

        self.active_effects = []

    # Enable a specific inventory effect
    def Enable(self, effect_name, effect_strength = 1):
        effect = self.effects.get(effect_name, effect_strength)
        if effect:
            effect.Enable()

    # Disable a specific inventory effect
    def Disable(self, effect_name, effect_strength = 1):
        effect = self.effects.get(effect_name, effect_strength)
        if effect:
            effect.Disable()


    def Get_Description(self, effect_name):
        effect = self.effects.get(effect_name)
        if effect:
            return effect.description