import pygame
from scripts.engine.utility.utils import load_image, load_images, Animation, get_tiles_from_sheet
from scripts.engine.keys.keys import keys

class Audio_Loader:
    def Run_All(self):
        self.sfx = {}
        Audio_Loader.Decoration_Effects(self)
        Audio_Loader.Weapons_Effects(self)
        Audio_Loader.Magic_Effects(self)
        Audio_Loader.Loot_Effects(self)
        Audio_Loader.Effect_Effects(self)
        Audio_Loader.Menu_Effects(self)
        Audio_Loader.Awakening_Effects(self)
        Audio_Loader.Trap_Effects(self)


    def Decoration_Effects(self):
        chest_effects ={
            keys.chest_open : pygame.mixer.Sound('data/sounds/decorations/chest/chest_open.wav'),
            keys.chest_break : pygame.mixer.Sound('data/sounds/decorations/chest/chest_break.wav'),
            keys.vase_break : pygame.mixer.Sound('data/sounds/decorations/chest/vase_break.wav'),
            keys.door_open : pygame.mixer.Sound('data/sounds/decorations/door_open.wav'),
            keys.soul_well_sound : pygame.mixer.Sound('data/sounds/decorations/soul_well.wav'),
            keys.teleportation : pygame.mixer.Sound('data/sounds/decorations/teleportation.wav'),
            keys.boss_spawning : pygame.mixer.Sound('data/sounds/decorations/shrine/boss_spawning.wav'),
            keys.tomb_lid : pygame.mixer.Sound('data/sounds/decorations/chest/tomb_lid.wav'),
            keys.collapse : pygame.mixer.Sound('data/sounds/decorations/collapse.wav'),
            keys.hunter_shrine_activation : pygame.mixer.Sound('data/sounds/decorations/shrine/hunter_shrine_activation.wav'),
            keys.good_reward : pygame.mixer.Sound('data/sounds/decorations/shrine/good_reward.wav'),
            keys.mid_reward : pygame.mixer.Sound('data/sounds/decorations/shrine/mid_reward.wav'),
            keys.bad_reward : pygame.mixer.Sound('data/sounds/decorations/shrine/bad_reward.wav'),
        }
        self.sfx.update(chest_effects)
        self.sfx[keys.chest_open].set_volume(0.1)
        self.sfx[keys.chest_break].set_volume(0.2)
        self.sfx[keys.vase_break].set_volume(0.2)
        self.sfx[keys.door_open].set_volume(0.4)
        self.sfx[keys.teleportation].set_volume(0.4)
        self.sfx[keys.soul_well_sound].set_volume(0.6)
        self.sfx[keys.boss_spawning].set_volume(0.4)
        self.sfx[keys.tomb_lid].set_volume(0.4)
        self.sfx[keys.collapse].set_volume(0.4)
        self.sfx[keys.hunter_shrine_activation].set_volume(0.4)
        self.sfx[keys.good_reward].set_volume(0.4)
        self.sfx[keys.mid_reward].set_volume(0.4)
        self.sfx[keys.bad_reward].set_volume(0.4)

    def Weapons_Effects(self):
        weapon_effects ={
            keys.sword_impact_wall : pygame.mixer.Sound('data/sounds/weapons/sword_impact_wall.wav'),
            keys.bow_draw : pygame.mixer.Sound('data/sounds/weapons/bow_draw.wav'),
            keys.arrow_shot : pygame.mixer.Sound('data/sounds/weapons/arrow_shot.wav'),
            keys.torch_fire_ball : pygame.mixer.Sound('data/sounds/weapons/torch_fire_ball.wav'),
            keys.projectile_impact : pygame.mixer.Sound('data/sounds/weapons/projectile_impact.wav'),
            keys.stab_attack_impact : pygame.mixer.Sound('data/sounds/weapons/stab_attack_impact.wav'),
            keys.torch_attack : pygame.mixer.Sound('data/sounds/weapons/torch_attack.wav'),
            keys.torch_equipped : pygame.mixer.Sound('data/sounds/weapons/torch_equipped.wav'),
            keys.sword_swing : pygame.mixer.Sound('data/sounds/weapons/sword_swing.wav'),
            keys.weapon_break : pygame.mixer.Sound('data/sounds/weapons/weapon_break.wav'),
            keys.enemy_hit : pygame.mixer.Sound('data/sounds/weapons/enemy_hit.wav'),
            keys.player_hit : pygame.mixer.Sound('data/sounds/weapons/player_hit.wav'),
            keys.projectile_hit : pygame.mixer.Sound('data/sounds/weapons/projectile_hit.wav'),
        }

        self.sfx.update(weapon_effects)

        self.sfx[keys.sword_impact_wall].set_volume(0.2)
        self.sfx[keys.bow_draw].set_volume(0.3)
        self.sfx[keys.arrow_shot].set_volume(0.4)
        self.sfx[keys.torch_fire_ball].set_volume(0.2)
        self.sfx[keys.projectile_impact].set_volume(0.3)
        self.sfx[keys.stab_attack_impact].set_volume(0.2)
        self.sfx[keys.torch_attack].set_volume(0.2)
        self.sfx[keys.torch_equipped].set_volume(0.2)
        self.sfx[keys.sword_swing].set_volume(0.2)
        self.sfx[keys.weapon_break].set_volume(0.2)
        self.sfx[keys.enemy_hit].set_volume(0.2)
        self.sfx[keys.player_hit].set_volume(0.2)
        self.sfx[keys.projectile_hit].set_volume(0.2)

    def Magic_Effects(self):
        weapon_effects ={
            keys.electric_ball : pygame.mixer.Sound('data/sounds/magic/electric/electric_ball.wav'),
            keys.electric_explosion : pygame.mixer.Sound('data/sounds/magic/electric/electric_explosion.wav'),
            keys.fire_ball : pygame.mixer.Sound('data/sounds/magic/fire/fire_ball.wav'),
            keys.fire_explosion : pygame.mixer.Sound('data/sounds/magic/fire/fire_explosion.wav'),
            keys.fire_particle : pygame.mixer.Sound('data/sounds/magic/fire/fire_particle.wav'),
            keys.frozen_explosion : pygame.mixer.Sound('data/sounds/magic/frozen/frozen_explosion.wav'),
            keys.frozen_projectile : pygame.mixer.Sound('data/sounds/magic/frozen/frozen_projectile.wav'),
            keys.poison_cloud : pygame.mixer.Sound('data/sounds/magic/poison/poison_cloud.wav'),
            keys.poison_plume : pygame.mixer.Sound('data/sounds/magic/poison/poison_plume.wav'),
            keys.vampiric_ball : pygame.mixer.Sound('data/sounds/magic/vampiric/vampiric_ball.wav'),
            keys.vampiric_explosion : pygame.mixer.Sound('data/sounds/magic/vampiric/vampiric_explosion.wav'),
            keys.vampiric_projectile : pygame.mixer.Sound('data/sounds/magic/vampiric/vampiric_projectile.wav'),
        }

        self.sfx.update(weapon_effects)

        self.sfx[keys.electric_ball].set_volume(0.2)
        self.sfx[keys.electric_explosion].set_volume(0.3)
        self.sfx[keys.fire_ball].set_volume(0.4)
        self.sfx[keys.fire_explosion].set_volume(0.2)
        self.sfx[keys.fire_particle].set_volume(0.3)
        self.sfx[keys.frozen_explosion].set_volume(0.2)
        self.sfx[keys.frozen_projectile].set_volume(0.2)
        self.sfx[keys.poison_cloud].set_volume(0.2)
        self.sfx[keys.poison_plume].set_volume(0.2)
        self.sfx[keys.vampiric_ball].set_volume(0.2)
        self.sfx[keys.vampiric_explosion].set_volume(0.2)
        self.sfx[keys.vampiric_projectile].set_volume(0.2)


    def Loot_Effects(self):
        weapon_effects ={
            keys.bell : pygame.mixer.Sound('data/sounds/loot/items/bell.wav'),
            keys.recall_scroll : pygame.mixer.Sound('data/sounds/loot/items/recall_scroll.wav'),
            keys.faded_hourglass : pygame.mixer.Sound('data/sounds/loot/items/faded_hourglass.wav'),
            keys.ethereal_chains : pygame.mixer.Sound('data/sounds/loot/items/ethereal_chains.wav'),
            keys.item_pickup : pygame.mixer.Sound('data/sounds/loot/general/item_pickup.wav'),
            keys.item_placedown : pygame.mixer.Sound('data/sounds/loot/general/item_placedown.wav'),
        }

        self.sfx.update(weapon_effects)

        self.sfx[keys.bell].set_volume(0.2)
        self.sfx[keys.recall_scroll].set_volume(0.3)
        self.sfx[keys.faded_hourglass].set_volume(0.3)
        self.sfx[keys.ethereal_chains].set_volume(0.3)
        self.sfx[keys.item_pickup].set_volume(0.5)
        self.sfx[keys.item_placedown].set_volume(0.3)

    
    def Effect_Effects(self):
        weapon_effects ={
            keys.healing : pygame.mixer.Sound('data/sounds/effects/healing.wav'),
            # keys.slow : pygame.mixer.Sound('data/sounds/effects/slow.wav'),
            keys.speed : pygame.mixer.Sound('data/sounds/effects/speed.wav'),
            keys.generic_effect : pygame.mixer.Sound('data/sounds/effects/general_effect.wav'),
        }

        self.sfx.update(weapon_effects)

        self.sfx[keys.healing].set_volume(0.2)
        # self.sfx[keys.slow].set_volume(0.1)
        self.sfx[keys.speed].set_volume(0.3)
        self.sfx[keys.generic_effect].set_volume(0.2)

    def Awakening_Effects(self):
        weapon_effects ={
            keys.awakening_increase : pygame.mixer.Sound('data/sounds/awakening/awakening_increase.wav'),
            keys.buff : pygame.mixer.Sound('data/sounds/awakening/buff.wav'),
            keys.debuff : pygame.mixer.Sound('data/sounds/awakening/debuff.wav'),
            keys.enemy_spawning : pygame.mixer.Sound('data/sounds/awakening/enemy_spawning.wav'),
            keys.awakening_1 : pygame.mixer.Sound('data/sounds/awakening/awakening_1.wav'),
            keys.awakening_2 : pygame.mixer.Sound('data/sounds/awakening/awakening_2.wav'),
            keys.awakening_3 : pygame.mixer.Sound('data/sounds/awakening/awakening_3.wav'),
        }

        self.sfx.update(weapon_effects)

        self.sfx[keys.awakening_increase].set_volume(0.2)
        self.sfx[keys.buff].set_volume(0.2)
        self.sfx[keys.debuff].set_volume(0.2)
        self.sfx[keys.enemy_spawning].set_volume(0.2)
        self.sfx[keys.awakening_1].set_volume(0.2)
        self.sfx[keys.awakening_2].set_volume(0.2)
        self.sfx[keys.awakening_3].set_volume(0.2)

    def Trap_Effects(self):
        trap_effects ={
            keys.rubble : pygame.mixer.Sound('data/sounds/traps/rubble.wav'),
            keys.pressure_plate : pygame.mixer.Sound('data/sounds/traps/pressure_plate.wav'),
        }

        self.sfx.update(trap_effects)

        self.sfx[keys.rubble].set_volume(0.4)
        self.sfx[keys.pressure_plate].set_volume(1)
    
    
    def Menu_Effects(self):
        menu_effects ={
            keys.hover : pygame.mixer.Sound('data/sounds/menu/hover.wav'),
            keys.click : pygame.mixer.Sound('data/sounds/menu/button_click.wav'),
        }

        self.sfx.update(menu_effects)

        self.sfx[keys.hover].set_volume(0.05)
        self.sfx[keys.click].set_volume(0.4)
    