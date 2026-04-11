from scripts.entities.items.weapons.enemy_weapons.claw import Claw
from scripts.engine.keys.keys import keys
from scripts.entities.moving_entities.enemies.crystal_caverns.elementals.elemental import Elemental

PLAYER_MAX_ATTACK_DISTANCE = 200

class Electric_Elemental(Elemental):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.electric_elemental, 3, 3, 3, attack_speed = (1.5, 2), default_range=keys.short_range)
        self.intent_manager.Set_Movement_Intent([keys.short_range])

        # Equip the weapon
        self.Equip_Weapon(Claw(game, self.pos)) 
        self.active_weapon.Set_Damage(keys.electric, 2)
        self.attack_distance = 250

    def Update(self, tilemap, delta_time, movement=...):
        super().Update(tilemap, delta_time, movement)
        
        if self.effects.electric.effect:
            self.Set_Effect(keys.healing, self.effects.frozen.effect)
            self.Set_Effect(keys.frozen_resistance, 2)
        
        return True



    def Set_Attack_Triggered(self):
        self.Set_Target(self.game.player.pos)
        self.Set_Charge(0)
        
        if self.distance_to_player > PLAYER_MAX_ATTACK_DISTANCE:
            return False
        
        self.active_weapon.Entity_Hit(self.game.player)
        self.active_weapon.entity_attack_type.Set_player_Hit_Effect()
        return True

  