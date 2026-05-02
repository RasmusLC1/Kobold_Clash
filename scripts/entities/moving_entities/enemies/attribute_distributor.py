from scripts.engine.keys.keys import keys
from scripts.entities.moving_entities.enemies.attribute_profile import Attribute_Profile


# 1. The Source of Truth - All stats in one place
ENEMY_STATS = {
    # [Undead / Crypt]
    keys.skeleton_warrior:        {keys.health: 70,  keys.souls: 10, keys.max_weapon_charge: 0.8,  keys.strength: 3, keys.speed: 3, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2, keys.behavior: keys.direct_attack, keys.ability: keys.dash},
    keys.skeleton_ranger:         {keys.health: 40,  keys.souls: 15, keys.max_weapon_charge: 1.2,  keys.strength: 2, keys.speed: 4, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2, keys.behavior: keys.long_range, keys.ability: keys.dash},
    keys.skeleton_cleric:         {keys.health: 40,  keys.souls: 20, keys.max_weapon_charge: 1.1,  keys.strength: 1, keys.speed: 2, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2, keys.behavior: keys.medium_range, keys.ability: keys.dash},
    keys.skeleton_bell_toller:    {keys.health: 60,  keys.souls: 15, keys.max_weapon_charge: 1.2,  keys.strength: 3, keys.speed: 3, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2, keys.behavior: keys.short_range, keys.ability: keys.dash},
    keys.skeleton_undertaker:     {keys.health: 110, keys.souls: 40, keys.max_weapon_charge: 0.8,  keys.strength: 5, keys.speed: 2, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2, keys.behavior: keys.short_range, keys.ability: keys.dash},
    keys.skeleton_guardian:       {keys.health: 120, keys.souls: 15, keys.max_weapon_charge: 1.2,  keys.strength: 4, keys.speed: 1, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2, keys.behavior: keys.direct_attack, keys.ability: keys.dash},
    keys.skeleton_warlock:        {keys.health: 40,  keys.souls: 40, keys.max_weapon_charge: 1.0,  keys.strength: 1, keys.speed: 1, keys.agility: 2, keys.intelligence: 5, keys.stamina: 2, keys.behavior: keys.medium_range, keys.ability: keys.dash},
    keys.wight_king:              {keys.health: 200, keys.souls: 55, keys.max_weapon_charge: 0.6,  keys.strength: 6, keys.speed: 4, keys.agility: 6, keys.intelligence: 5, keys.stamina: 5, keys.behavior: keys.hit_and_run, keys.ability: keys.dash},
    keys.skeleton_banner_bearer:  {keys.health: 50,  keys.souls: 15, keys.max_weapon_charge: 1.0, keys.strength: 1, keys.speed: 2, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2, keys.behavior: keys.medium_range, keys.ability: keys.dash},
    keys.phantom:                 {keys.health: 20,  keys.souls: 30, keys.max_weapon_charge: 0.6, keys.strength: 5, keys.speed: 6, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2, keys.behavior: keys.direct_attack, keys.ability: keys.dash},
    keys.wraith:                  {keys.health: 50,  keys.souls: 25, keys.max_weapon_charge: 1.0,  keys.strength: 3, keys.speed: 4, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2, keys.behavior: keys.direct_attack, keys.ability: keys.dash},
    keys.shade:                   {keys.health: 50,  keys.souls: 20, keys.max_weapon_charge: 1.0,  keys.strength: 3, keys.speed: 1, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2, keys.behavior: keys.direct_attack, keys.ability: keys.dash},
    keys.vampire:                 {keys.health: 150, keys.souls: 60, keys.max_weapon_charge: 0.5,  keys.strength: 4, keys.speed: 3, keys.agility: 3, keys.intelligence: 2, keys.stamina: 2, keys.behavior: keys.retreat_when_damaged, keys.ability: keys.dash},
    keys.ghoul:                   {keys.health: 80,  keys.souls: 20, keys.max_weapon_charge: 0.8,  keys.strength: 6, keys.speed: 6, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2, keys.behavior: keys.hit_and_run, keys.ability: keys.dash},

    # [Crystal Caverns]
    keys.fire_spirit:             {keys.health: 40, keys.souls: 20, keys.max_weapon_charge: 1.4,  keys.strength: 4, keys.speed: 4, keys.agility: 4, keys.intelligence: 2, keys.stamina: 2, keys.behavior: keys.short_range, keys.ability: keys.dash},
    keys.ice_spirit:              {keys.health: 50, keys.souls: 20, keys.max_weapon_charge: 1.6,  keys.strength: 7, keys.speed: 3, keys.agility: 3, keys.intelligence: 2, keys.stamina: 2, keys.behavior: keys.medium_range, keys.ability: keys.dash},
    keys.earth_elemental:         {keys.health: 40, keys.souls: 30, keys.max_weapon_charge: 2.0,  keys.strength: 5, keys.speed: 2, keys.agility: 2, keys.intelligence: 8, keys.stamina: 2, keys.behavior: keys.hit_and_run, keys.ability: keys.invincible},
    keys.electric_elemental:      {keys.health: 50, keys.souls: 30, keys.max_weapon_charge: 3.0,  keys.strength: 4, keys.speed: 2, keys.agility: 3, keys.intelligence: 2, keys.stamina: 2, keys.behavior: keys.medium_range, keys.ability: keys.dash},
    keys.poison_elemental:        {keys.health: 20, keys.souls: 10, keys.max_weapon_charge: 0.1, keys.strength: 4, keys.speed: 4, keys.agility: 3, keys.intelligence: 2, keys.stamina: 2, keys.behavior: keys.direct_attack, keys.ability: keys.dash},
    keys.medusa:                  {keys.health: 20, keys.souls: 60, keys.max_weapon_charge: 0.9,  keys.strength: 4, keys.speed: 4, keys.agility: 3, keys.intelligence: 2, keys.stamina: 2, keys.behavior: keys.short_range, keys.ability: keys.dash},
    keys.minotaur:                {keys.health: 20, keys.souls: 55, keys.max_weapon_charge: 0.7,  keys.strength: 4, keys.speed: 4, keys.agility: 3, keys.intelligence: 2, keys.stamina: 2, keys.behavior: keys.hybrid, keys.ability: keys.dash},
    keys.spider:                  {keys.health: 60, keys.souls: 20, keys.max_weapon_charge: 0.9,  keys.strength: 4, keys.speed: 6, keys.agility: 3, keys.intelligence: 5, keys.stamina: 2, keys.behavior: keys.hit_and_run, keys.ability: keys.dash},
}

class Attribute_Distributor:
    HP_GROWTH_PER_FLOOR = 0.30 
    STR_GROWTH_PER_FLOOR = 0.20
    SOUL_GROWTH_PER_FLOOR = 0.10
    ELITE_MULTIPLIER = 2.0
    
    @staticmethod
    def Get_Enemy_Profile(enemy_type, depth=1, is_elite=False):
        """
        Returns a fully initialized Attribute_Profile object.
        """
        # Get base stats dictionary
        enemy_data = ENEMY_STATS.get(enemy_type, {}).copy()
        if not enemy_data:
            return None

        # Apply scaling to fields
        enemy_data[keys.health] = Attribute_Distributor.Calculate_Health(enemy_type, depth, is_elite)
        enemy_data[keys.strength] = Attribute_Distributor.Calculate_Strength(enemy_type, depth, is_elite)
        enemy_data[keys.souls] = Attribute_Distributor.Calculate_Souls(enemy_type, depth, is_elite)

        # Create and return the Profile object
        return Attribute_Profile(
            health=enemy_data[keys.health],
            souls=enemy_data[keys.souls],
            max_weapon_charge=enemy_data.get(keys.max_weapon_charge, 1.0),
            strength=enemy_data[keys.strength],
            speed=enemy_data.get(keys.speed, 1),
            agility=enemy_data.get(keys.agility, 1),
            intelligence=enemy_data.get(keys.intelligence, 1),
            stamina=enemy_data.get(keys.stamina, 1),
            behavior=enemy_data.get(keys.behavior, keys.direct_attack),
            ability=enemy_data.get(keys.ability, None)
        )

    @staticmethod
    def Calculate_Health(enemy_type, depth, is_elite):
        base = ENEMY_STATS[enemy_type].get(keys.health, 10)
        multiplier = Attribute_Distributor.ELITE_MULTIPLIER if is_elite else 1.0
        return int(base * (1 + (Attribute_Distributor.HP_GROWTH_PER_FLOOR * (depth - 1))) * multiplier)

    @staticmethod
    def Calculate_Strength(enemy_type, depth, is_elite):
        base = ENEMY_STATS[enemy_type].get(keys.strength, 1)
        multiplier = Attribute_Distributor.ELITE_MULTIPLIER if is_elite else 1.0
        return int(base * (1 + (Attribute_Distributor.STR_GROWTH_PER_FLOOR * (depth - 1))) * multiplier)

    @staticmethod
    def Calculate_Souls(enemy_type, depth, is_elite):
        base = ENEMY_STATS[enemy_type].get(keys.souls, 5)
        multiplier = Attribute_Distributor.ELITE_MULTIPLIER if is_elite else 1.0
        return int(base * (1 + (Attribute_Distributor.SOUL_GROWTH_PER_FLOOR * (depth - 1))) * multiplier)