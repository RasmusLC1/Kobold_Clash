from scripts.engine.keys.keys import keys
from scripts.entities.moving_entities.enemies.attribute_profile import Attribute_Profile
from scripts.entities.moving_entities.enemies.enemy_base_state import Enemy_Base_State


# 1. The Source of Truth - All stats in one place
ENEMY_STATS = {
    # [Undead / Crypt]
    keys.skeleton_warrior: {
        keys.health: 70,
        keys.souls: 10,
        keys.size: (32, 32),
        keys.max_weapon_charge: 0.8,
        keys.strength: 3,
        keys.speed: 3,
        keys.agility: 2,
        keys.intelligence: 2,
        keys.stamina: 2,
        keys.behavior: keys.direct_attack,
        keys.ability: keys.dash,
        keys.idle_animation: 1,
        keys.run_animation: 1,
        keys.attack_animation: 1
    },

    keys.skeleton_ranger: {
        keys.health: 40,
        keys.souls: 15,
        keys.size: (32, 32),
        keys.max_weapon_charge: 1.2,
        keys.strength: 2,
        keys.speed: 4,
        keys.agility: 2,
        keys.intelligence: 2,
        keys.stamina: 2,
        keys.behavior: keys.long_range,
        keys.ability: keys.dash,
        keys.idle_animation: 1,
        keys.run_animation: 1,
        keys.attack_animation: 1
    },

    keys.skeleton_cleric: {
        keys.health: 40,
        keys.souls: 20,
        keys.size: (32, 32),
        keys.max_weapon_charge: 1.1,
        keys.strength: 1,
        keys.speed: 2,
        keys.agility: 2,
        keys.intelligence: 2,
        keys.stamina: 2,
        keys.behavior: keys.medium_range,
        keys.ability: keys.dash,
        keys.idle_animation: 1,
        keys.run_animation: 1,
        keys.attack_animation: 1
    },

    keys.skeleton_bell_toller: {
        keys.health: 60,
        keys.souls: 15,
        keys.size: (32, 32),
        keys.max_weapon_charge: 1.2,
        keys.strength: 3,
        keys.speed: 3,
        keys.agility: 2,
        keys.intelligence: 2,
        keys.stamina: 2,
        keys.behavior: keys.short_range,
        keys.ability: keys.dash,
        keys.idle_animation: 1,
        keys.run_animation: 1,
        keys.attack_animation: 1
    },

    keys.skeleton_undertaker: {
        keys.health: 110,
        keys.souls: 40,
        keys.size: (32, 32),
        keys.max_weapon_charge: 0.8,
        keys.strength: 5,
        keys.speed: 2,
        keys.agility: 2,
        keys.intelligence: 2,
        keys.stamina: 2,
        keys.behavior: keys.short_range,
        keys.ability: keys.dash,
        keys.idle_animation: 1,
        keys.run_animation: 1,
        keys.attack_animation: 1
    },

    keys.skeleton_guardian: {
        keys.health: 120,
        keys.souls: 15,
        keys.size: (32, 32),
        keys.max_weapon_charge: 1.2,
        keys.strength: 4,
        keys.speed: 1,
        keys.agility: 2,
        keys.intelligence: 2,
        keys.stamina: 2,
        keys.behavior: keys.direct_attack,
        keys.ability: keys.dash,
        keys.idle_animation: 1,
        keys.run_animation: 1,
        keys.attack_animation: 1
    },

    keys.skeleton_warlock: {
        keys.health: 40,
        keys.souls: 40,
        keys.size: (32, 32),
        keys.max_weapon_charge: 1.0,
        keys.strength: 1,
        keys.speed: 1,
        keys.agility: 2,
        keys.intelligence: 5,
        keys.stamina: 2,
        keys.behavior: keys.medium_range,
        keys.ability: keys.dash,
        keys.idle_animation: 1,
        keys.run_animation: 1,
        keys.attack_animation: 1
    },

    keys.wight_king: {
        keys.health: 200,
        keys.souls: 55,
        keys.size: (32, 32),
        keys.max_weapon_charge: 0.6,
        keys.strength: 6,
        keys.speed: 4,
        keys.agility: 6,
        keys.intelligence: 5,
        keys.stamina: 5,
        keys.behavior: keys.hit_and_run,
        keys.ability: keys.dash,
        keys.idle_animation: 1,
        keys.run_animation: 1,
        keys.attack_animation: 1
    },

    keys.skeleton_banner_bearer: {
        keys.health: 50,
        keys.souls: 15,
        keys.size: (32, 32),
        keys.max_weapon_charge: 1.0,
        keys.strength: 1,
        keys.speed: 2,
        keys.agility: 2,
        keys.intelligence: 2,
        keys.stamina: 2,
        keys.behavior: keys.medium_range,
        keys.ability: keys.dash,
        keys.idle_animation: 1,
        keys.run_animation: 1,
        keys.attack_animation: 1
    },

    keys.phantom: {
        keys.health: 20,
        keys.souls: 30,
        keys.size: (32, 32),
        keys.max_weapon_charge: 0.6,
        keys.strength: 5,
        keys.speed: 6,
        keys.agility: 2,
        keys.intelligence: 2,
        keys.stamina: 2,
        keys.behavior: keys.direct_attack,
        keys.ability: keys.dash,
        keys.idle_animation: 1,
        keys.run_animation: 1,
        keys.attack_animation: 1
    },

    keys.wraith: {
        keys.health: 50,
        keys.souls: 25,
        keys.size: (32, 32),
        keys.max_weapon_charge: 1.0,
        keys.strength: 3,
        keys.speed: 4,
        keys.agility: 2,
        keys.intelligence: 2,
        keys.stamina: 2,
        keys.behavior: keys.direct_attack,
        keys.ability: keys.dash,
        keys.idle_animation: 1,
        keys.run_animation: 1,
        keys.attack_animation: 1
    },

    keys.shade: {
        keys.health: 50,
        keys.souls: 20,
        keys.size: (32, 32),
        keys.max_weapon_charge: 1.0,
        keys.strength: 3,
        keys.speed: 1,
        keys.agility: 2,
        keys.intelligence: 2,
        keys.stamina: 2,
        keys.behavior: keys.direct_attack,
        keys.ability: keys.dash,
        keys.idle_animation: 1,
        keys.run_animation: 1,
        keys.attack_animation: 1
    },

    keys.vampire: {
        keys.health: 150,
        keys.souls: 60,
        keys.size: (32, 32),
        keys.max_weapon_charge: 0.5,
        keys.strength: 4,
        keys.speed: 3,
        keys.agility: 3,
        keys.intelligence: 2,
        keys.stamina: 2,
        keys.behavior: keys.retreat_when_damaged,
        keys.ability: keys.dash,
        keys.idle_animation: 1,
        keys.run_animation: 1,
        keys.attack_animation: 1
    },

    keys.ghoul: {
        keys.health: 80,
        keys.souls: 20,
        keys.size: (32, 32),
        keys.max_weapon_charge: 0.8,
        keys.strength: 6,
        keys.speed: 6,
        keys.agility: 2,
        keys.intelligence: 2,
        keys.stamina: 2,
        keys.behavior: keys.hit_and_run,
        keys.ability: keys.dash,
        keys.idle_animation: 1,
        keys.run_animation: 1,
        keys.attack_animation: 1
    },

    # [Crystal Caverns]
    keys.fire_spirit: {
        keys.health: 40,
        keys.souls: 20,
        keys.size: (32, 32),
        keys.max_weapon_charge: 0.8,
        keys.strength: 4,
        keys.speed: 4,
        keys.agility: 4,
        keys.intelligence: 2,
        keys.stamina: 2,
        keys.behavior: keys.short_range,
        keys.ability: None,
        keys.idle_animation: 1,
        keys.run_animation: 1,
        keys.attack_animation: 1
    },

    keys.ice_spirit: {
        keys.health: 50,
        keys.souls: 20,
        keys.size: (32, 32),
        keys.max_weapon_charge: 0.9,
        keys.strength: 7,
        keys.speed: 3,
        keys.agility: 3,
        keys.intelligence: 2,
        keys.stamina: 2,
        keys.behavior: keys.medium_range,
        keys.ability: None,
        keys.idle_animation: 1,
        keys.run_animation: 1,
        keys.attack_animation: 1
    },

    keys.earth_elemental: {
        keys.health: 40,
        keys.souls: 30,
        keys.size: (32, 32),
        keys.max_weapon_charge: 2.0,
        keys.strength: 5,
        keys.speed: 2,
        keys.agility: 4,
        keys.intelligence: 7,
        keys.stamina: 2,
        keys.behavior: keys.hit_and_run,
        keys.ability: keys.invisibility,
        keys.idle_animation: 1,
        keys.run_animation: 1,
        keys.attack_animation: 1
    },

    keys.electric_elemental: {
        keys.health: 50,
        keys.souls: 30,
        keys.size: (32, 32),
        keys.max_weapon_charge: 3.0,
        keys.strength: 4,
        keys.speed: 2,
        keys.agility: 3,
        keys.intelligence: 2,
        keys.stamina: 2,
        keys.behavior: keys.medium_range,
        keys.ability: None,
        keys.idle_animation: 1,
        keys.run_animation: 1,
        keys.attack_animation: 1
    },

    keys.poison_elemental: {
        keys.health: 20,
        keys.souls: 10,
        keys.size: (32, 32),
        keys.max_weapon_charge: 0.1,
        keys.strength: 4,
        keys.speed: 4,
        keys.agility: 3,
        keys.intelligence: 2,
        keys.stamina: 2,
        keys.behavior: keys.direct_attack,
        keys.ability: None,
        keys.idle_animation: 1,
        keys.run_animation: 1,
        keys.attack_animation: 1
    },

    keys.medusa: {
        keys.health: 20,
        keys.souls: 60,
        keys.size: (32, 32),
        keys.max_weapon_charge: 0.9,
        keys.strength: 4,
        keys.speed: 4,
        keys.agility: 3,
        keys.intelligence: 2,
        keys.stamina: 2,
        keys.behavior: keys.short_range,
        keys.ability: None,
        keys.idle_animation: 1,
        keys.run_animation: 1,
        keys.attack_animation: 1
    },

    keys.minotaur: {
        keys.health: 20,
        keys.souls: 55,
        keys.size: (32, 32),
        keys.max_weapon_charge: 0.7,
        keys.strength: 4,
        keys.speed: 4,
        keys.agility: 3,
        keys.intelligence: 2,
        keys.stamina: 2,
        keys.behavior: keys.hybrid,
        keys.ability: keys.rage,
        keys.idle_animation: 1,
        keys.run_animation: 1,
        keys.attack_animation: 1
    },

    keys.spider: {
        keys.health: 60,
        keys.souls: 20,
        keys.size: (32, 32),
        keys.max_weapon_charge: 0.9,
        keys.strength: 4,
        keys.speed: 6,
        keys.agility: 3,
        keys.intelligence: 5,
        keys.stamina: 2,
        keys.behavior: keys.hit_and_run,
        keys.ability: keys.jump,
        keys.idle_animation: 1,
        keys.run_animation: 1,
        keys.attack_animation: 1
    },
}
class Attribute_Distributor:
    HP_GROWTH_PER_FLOOR = 0.30 
    STR_GROWTH_PER_FLOOR = 0.20
    SOUL_GROWTH_PER_FLOOR = 0.10
    ELITE_MULTIPLIER = 2.0
    
    @staticmethod
    def Get_Enemy_Profile(enemy_type, depth=1, is_elite=False):
        base_state = ENEMY_STATS.get(enemy_type)
        if not base_state:
            return None

        # Scale stats using the base_state object attributes
        scaled_health = Attribute_Distributor.Calculate_Health(base_state, depth, is_elite)
        scaled_strength = Attribute_Distributor.Calculate_Strength(base_state, depth, is_elite)
        scaled_souls = Attribute_Distributor.Calculate_Souls(base_state, depth, is_elite)

        return Attribute_Profile(
            health=scaled_health,
            souls=scaled_souls,
            max_weapon_charge=base_state.max_weapon_charge,
            strength=scaled_strength,
            speed=base_state.speed,
            agility=base_state.agility,
            intelligence=base_state.intelligence,
            stamina=base_state.stamina,
            behavior=base_state.behavior,
            ability=base_state.ability,
            # We pass these along so the Enemy class can access them from the profile
            idle_animation=base_state.idle_animation,
            run_animation=base_state.run_animation,
            attack_animation=base_state.attack_animation,
            size=base_state.size
        )

    @staticmethod
    def Calculate_Health(base_state, depth, is_elite):
        multiplier = Attribute_Distributor.ELITE_MULTIPLIER if is_elite else 1.0
        return int(base_state.health * (1 + (Attribute_Distributor.HP_GROWTH_PER_FLOOR * (depth - 1))) * multiplier)

    @staticmethod
    def Calculate_Strength(base_state, depth, is_elite):
        multiplier = Attribute_Distributor.ELITE_MULTIPLIER if is_elite else 1.0
        return int(base_state.strength * (1 + (Attribute_Distributor.STR_GROWTH_PER_FLOOR * (depth - 1))) * multiplier)

    @staticmethod
    def Calculate_Souls(base_state, depth, is_elite):
        multiplier = Attribute_Distributor.ELITE_MULTIPLIER if is_elite else 1.0
        return int(base_state.souls * (1 + (Attribute_Distributor.SOUL_GROWTH_PER_FLOOR * (depth - 1))) * multiplier)