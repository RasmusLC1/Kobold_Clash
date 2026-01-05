from scripts.entities.items.loot.passive.passive_loot import Passive_Loot
from scripts.engine.keys.keys import keys
import pygame

# Generic passive loot that changes depending on the type, simplified to one
# class since it uses effects
class Cursed_Loot(Passive_Loot):
    def __init__(self, game, type, pos, effect_power, value):
        super().__init__(game, type, pos, effect_power=effect_power, rarity_value=value, loot_type=keys.curse)



    def Place_Down(self):
        if self.game.decoration_handler.Check_Item_Collision(self):
            return False
        self.game.player.Disable_Inventory_Effect(self.type, self.effect_power)
        self.Delete_Item()
        return False


    def Set_Effect(self, type):
        effects = {
            keys.blood_tomb : keys.blood_tomb,
            keys.black_coin : keys.black_coin,
            keys.vampire_locket : keys.vampiric,
            keys.demonic_bargain : keys.demonic_bargain,
            keys.temptress_embrace : keys.temptress_embrace,
            keys.cursed_dice : keys.cursed_dice,
            keys.eldritch_mirror : keys.eldritch_mirror,
            keys.forsaken_grimoire : keys.forsaken_grimoire,
            keys.cracked_talisman : keys.cracked_talisman,
            keys.echoing_skull : keys.echoing_skull,
        }
        self.effect = effects.get(type)

        if not self.effect:
            print("EFFECT NOT FOUND IN CURSED LOOT")
            return False

        return True


      # # Render item with fadeout if it's in an illegal position
    def Render_In_Bounds(self, player_pos, mouse_pos, surf, offset = (0,0)):
         # Copy image and set alpha
        entity_image =  pygame.transform.scale(self.entity_image.copy(), self.floor_size)
        # entity_image.set_alpha(255)

        # Create red overlay
        red_overlay = pygame.Surface(entity_image.get_size(), pygame.SRCALPHA)
        red_overlay.fill((255, 0, 0, 100))  # Red with transparency

        # Blit entity and red overlay
        pos = (mouse_pos[0] - offset[0], mouse_pos[1] - offset[1])
        surf.blit(entity_image, pos)
        surf.blit(red_overlay, pos)

