from scripts.entities.moving_entities.animation.animation_handler import Animation_Handler
from scripts.engine.keys.keys import keys
import random
import pygame

ATTACK_TYPES = {
    keys.battle_axe : [keys.two_hand],
    keys.bow : [keys.bow_draw],
    keys.crossbow : [keys.crossbow_attack],
    keys.bell : [keys.stab, keys.two_hand],
    keys.halberd : [keys.stab, keys.two_hand],
    keys.hatchet : [keys.cut],
    keys.sceptre : [keys.two_hand, keys.stab],
    keys.scythe : [keys.two_hand],
    keys.spear : [keys.stab],
    keys.sword : [keys.stab, keys.cut],
    keys.torch : [keys.cut],
    keys.warhammer : [keys.two_hand],
}

class Player_Animation_Handler(Animation_Handler):
    def __init__(self, entity, animation_max=0, animation_cooldown_max=1):
        super().__init__(entity, animation_max=animation_max,
                         animation_cooldown_max=animation_cooldown_max)

        self.keyboard = self.entity.game.keyboard_handler

        self.Set_Animation_Values()

    # Add player-specific animations to unified handler self.animations
    def Set_Animation_Values(self):
        self.animations.update({
            keys.roll: {keys.num: 0, keys.num_max: 4, keys.cooldown: 0, keys.cooldown_max: 0.2},
            keys.backstep: {keys.num: 0, keys.num_max: 4, keys.cooldown: 0, keys.cooldown_max: 0.2},
        })
        # Player animation timings
        self.Set_Animation_Num_Max(keys.idle, 3)
        self.Set_Animation_Cooldown_Max(keys.idle, 0.2)
        self.Set_Animation_Num_Max(keys.run, 5)
        self.Set_Animation_Cooldown_Max(keys.run, 0.1)

        self.Set_Animation_Num_Max(keys.attack, 4)
        self.Set_Animation_Cooldown_Max(keys.attack, 0.1)

    # State Handling
    def Set_Action(self):
        if self.animation_lock:
            return
        if self.Check_Special_Animations():  # Check special first as this is priority
            return

        if self.Check_Movement():
            return

    def Set_Attack_Speed(self, attack_time):
        attack_animation = self.animations[keys.attack]
        max_animation = attack_animation[keys.num_max]
        attack_speed = attack_time / max_animation
        self.Set_Animation_Cooldown_Max(keys.attack, attack_speed)

    # Check general movement and idling
    def Check_Movement(self):
        keyboard = self.keyboard
        if not keyboard.Check_If_Movement_Enabled():
            self.Set_Animation(keys.idle)
            return False

        if keyboard.is_key_pressed(pygame.K_w):
            if keyboard.is_key_pressed(pygame.K_d):
                self.flip[0] = False
            else:
                self.flip[0] = True
            self.Set_Animation('running_up')
        else:
            self.Set_Animation('running_down')

        return True

    # Check for special animations, such as attacks and special movements
    def Check_Special_Animations(self):
        keyboard = self.keyboard
        if keyboard.is_key_pressed(pygame.K_SPACE):
            self.Set_Animation("rolling")
            self.Set_Animation_Lock(True)
            return True

        if keyboard.is_key_pressed(pygame.K_LALT):
            self.Set_Animation(keys.backstep)
            self.Set_Animation_Lock(True)
            return True

        return False

    def Trigger_Attack_Animation(self):
        self.Reset_Animation_Values()
        self.Attack_Direction_Handler()
        attack_type = self.Get_Attack_Animation_Type()
        self.Set_Animation(attack_type)
        self.Set_Animation_Lock(True)
        anim = self.animations[keys.attack]
        self.entity.weapon_handler.Update_Weapon_Animation(anim[keys.num])
        return True

    def Get_Attack_Animation_Type(self):
        weapon_type = self.entity.weapon_handler.Get_Weapon_Type()

        if not weapon_type:
            return None

        weapon_attack_types = ATTACK_TYPES.get(weapon_type)

        if not weapon_attack_types:
            print("WEAPON TYPE NOT FOUND", weapon_type, weapon_attack_types)
            return

        attack_type = random.choice(weapon_attack_types)

        return attack_type

    # NOTE: this class previously defined Set_Animation twice — the first
    # (delegating to super(), resetting the weapon's animation) was silently
    # shadowed by this second definition and never ran. Merged into one:
    # keeps this version's no-auto-lock behavior (movement needs to keep
    # re-evaluating every frame; only special/attack call sites lock
    # explicitly) but restores the weapon reset call that had gone dead.
    # Flagging in case the missing weapon reset was relied on anywhere.
    def Set_Animation(self, action):
        if self.animation_lock:
            return False
        if action == self.action:
            return False

        self.action = action
        self.animation_key = self.entity.type + '_' + self.action
        self.Reset_Animation_Values()
        self.animation = 0
        self.Set_Sprite(self.animation_key)

        weapon = self.entity.Get_Weapon()
        if weapon:
            weapon.Reset_Animation()

        return True

    # Animation Updates
    def Handle_Animation_Update(self, delta_time):
        for anim_type in self.animations.keys():
            if anim_type in self.animation_key:
                self.Update_Generic_Animation(anim_type, delta_time)
                return
        # fallback if no match
        self.Update_Generic_Animation(keys.idle, delta_time)

    def Update_Generic_Animation(self, anim_type, delta_time):
        if not super().Update_Generic_Animation(anim_type, delta_time):
            return False
        self.entity.weapon_handler.Update_Weapon_Animation(self.animation)
        return True