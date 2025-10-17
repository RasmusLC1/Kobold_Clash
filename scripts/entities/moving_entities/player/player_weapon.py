from scripts.engine.keys.keys import keys


class Player_Weapon_Handler():
    def __init__(self, game, player) -> None:
        self.game = game
        self.player = player
        self.active_weapon = None
        self.inventory_interaction = 0
        self.active_weapon_cooldown = 0
        self.attack_lock = False



    def Update(self, delta_time, offset = (0, 0)):
        self.Update_Weapon(delta_time, offset)

    def Set_Active_Weapon(self, weapon):  
          
        equipped_weapon = weapon
        equipped_weapon.Move(self.player.pos)
        self.active_weapon = equipped_weapon
        return

    def Set_Attack_Lock(self, state):
        self.attack_lock = state
    

    # Function to update the player's weapons
    def Update_Weapon(self, delta_time, offset=(0, 0)):

        if not self.active_weapon:
            return
        
        if self.inventory_interaction:
            self.Set_Inventory_Interaction(self.inventory_interaction - 1)
            self.active_weapon.Reset_Charge()
            return
        self.active_weapon.Set_Equipped_Position(self.player.direction_y_holder)
        # Set the attack lock above the update to prevent attacks
        if self.attack_lock:
            return

        self.active_weapon.Update(delta_time, offset)
        if not self.active_weapon:
            return
        self.active_weapon.Update_Attack(delta_time)
        return
    

    def Set_Inventory_Interaction(self, state):
        self.inventory_interaction = state

    def Remove_Active_Weapon(self):
        if self.active_weapon:
            self.active_weapon.Disable_Gem_Effect()
            self.active_weapon.Unequip()
            self.active_weapon = None

    def Check_If_Weapon_Should_Be_Removed(self, weapon):
        if not self.active_weapon:
            return False
        
        if not self.Check_If_Weapon_Is_Equipped(weapon):
            return False
        
        self.Remove_Active_Weapon()
        return True

    def Check_If_Weapon_Is_Equipped(self, weapon):
        if not self.active_weapon:
            return False
        return self.active_weapon.ID == weapon.ID
        
    def Update_Weapon_Animation(self, animation_num):
        if not self.active_weapon:
            return
        
        self.active_weapon.Update_Player_Animation(animation_num)

    def Render_Weapons(self, surf, offset):
        if self.active_weapon:
            self.active_weapon.Render_Equipped(surf, offset)