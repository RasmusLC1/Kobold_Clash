from scripts.engine.keys.keys import keys

LONG_RANGE = 1
MEDIUM_RANGE = 2
SHORT_RANGE = 3
HIT_AND_RUN = 4
HYBRID = 5
PLACE_HOLDER6 = 6
PLACE_HOLDER7 = 7
PLACE_HOLDER8 = 8
RETREAT_WHEN_DAMAGED = 9
DIRECT_ATTACK = 10


# 1. The Source of Truth - All stats in one place
ENEMY_STATS = {
    # [Undead / Crypt]
    keys.skeleton_warrior:        {keys.health: 70,  keys.souls: 10, keys.max_weapon_charge: 0.8,  keys.strength: 3, keys.speed: 3, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2, keys.behavior: DIRECT_ATTACK,},
    keys.skeleton_ranger:         {keys.health: 40,  keys.souls: 15, keys.max_weapon_charge: 1.2,  keys.strength: 2, keys.speed: 4, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2, keys.behavior: LONG_RANGE,},
    keys.skeleton_cleric:         {keys.health: 40,  keys.souls: 20, keys.max_weapon_charge: 1.1,  keys.strength: 1, keys.speed: 2, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2, keys.behavior: MEDIUM_RANGE,},
    keys.skeleton_bell_toller:    {keys.health: 60,  keys.souls: 15, keys.max_weapon_charge: 1.2,  keys.strength: 3, keys.speed: 3, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2, keys.behavior: SHORT_RANGE,},
    keys.skeleton_undertaker:     {keys.health: 110, keys.souls: 40, keys.max_weapon_charge: 0.8,  keys.strength: 5, keys.speed: 2, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2, keys.behavior: SHORT_RANGE,},
    keys.skeleton_guardian:       {keys.health: 120, keys.souls: 15, keys.max_weapon_charge: 1.2,  keys.strength: 4, keys.speed: 1, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2, keys.behavior: DIRECT_ATTACK,},
    keys.skeleton_warlock:        {keys.health: 40,  keys.souls: 40, keys.max_weapon_charge: 1.0,  keys.strength: 1, keys.speed: 1, keys.agility: 2, keys.intelligence: 5, keys.stamina: 2, keys.behavior: MEDIUM_RANGE,},
    keys.wight_king:              {keys.health: 200, keys.souls: 55, keys.max_weapon_charge: 0.6,  keys.strength: 6, keys.speed: 4, keys.agility: 6, keys.intelligence: 5, keys.stamina: 5, keys.behavior: HIT_AND_RUN,},
    keys.skeleton_banner_bearer:  {keys.health: 50,  keys.souls: 15, keys.max_weapon_charge: 1.0, keys.strength: 1, keys.speed: 2, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2, keys.behavior: MEDIUM_RANGE, },
    keys.phantom:                 {keys.health: 20,  keys.souls: 30, keys.max_weapon_charge: 0.6, keys.strength: 5, keys.speed: 6, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2, keys.behavior: DIRECT_ATTACK, },
    keys.wraith:                  {keys.health: 50,  keys.souls: 25, keys.max_weapon_charge: 1.0,  keys.strength: 3, keys.speed: 4, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2, keys.behavior: DIRECT_ATTACK,},
    keys.shade:                   {keys.health: 50,  keys.souls: 20, keys.max_weapon_charge: 1.0,  keys.strength: 3, keys.speed: 1, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2, keys.behavior: DIRECT_ATTACK,},
    keys.vampire:                 {keys.health: 150, keys.souls: 60, keys.max_weapon_charge: 0.5,  keys.strength: 4, keys.speed: 3, keys.agility: 3, keys.intelligence: 2, keys.stamina: 2, keys.behavior: RETREAT_WHEN_DAMAGED,},
    keys.ghoul:                   {keys.health: 80,  keys.souls: 20, keys.max_weapon_charge: 0.8,  keys.strength: 6, keys.speed: 6, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2, keys.behavior: HIT_AND_RUN,},

    # [Crystal Caverns]
    keys.fire_spirit:             {keys.health: 40, keys.souls: 20, keys.max_weapon_charge: 1.4,  keys.strength: 4, keys.speed: 4, keys.agility: 4, keys.intelligence: 2, keys.stamina: 2, keys.behavior: SHORT_RANGE,},
    keys.ice_spirit:              {keys.health: 50, keys.souls: 20, keys.max_weapon_charge: 1.6,  keys.strength: 7, keys.speed: 3, keys.agility: 3, keys.intelligence: 2, keys.stamina: 2, keys.behavior: MEDIUM_RANGE,},
    keys.earth_elemental:         {keys.health: 80, keys.souls: 30, keys.max_weapon_charge: 2.0,  keys.strength: 5, keys.speed: 2, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2, keys.behavior: HIT_AND_RUN,},
    keys.electric_elemental:      {keys.health: 50, keys.souls: 30, keys.max_weapon_charge: 3.0,  keys.strength: 4, keys.speed: 2, keys.agility: 3, keys.intelligence: 2, keys.stamina: 2, keys.behavior: MEDIUM_RANGE,},
    keys.poison_elemental:        {keys.health: 20, keys.souls: 10, keys.max_weapon_charge: 0.1, keys.strength: 4, keys.speed: 4, keys.agility: 3, keys.intelligence: 2, keys.stamina: 2, keys.behavior: DIRECT_ATTACK, },
    keys.medusa:                  {keys.health: 20, keys.souls: 60, keys.max_weapon_charge: 0.9,  keys.strength: 4, keys.speed: 4, keys.agility: 3, keys.intelligence: 2, keys.stamina: 2, keys.behavior: SHORT_RANGE,},
    keys.minotaur:                {keys.health: 20, keys.souls: 55, keys.max_weapon_charge: 0.7,  keys.strength: 4, keys.speed: 4, keys.agility: 3, keys.intelligence: 2, keys.stamina: 2, keys.behavior: HYBRID,},
    keys.spider:                  {keys.health: 60, keys.souls: 20, keys.max_weapon_charge: 0.9,  keys.strength: 4, keys.speed: 6, keys.agility: 3, keys.intelligence: 5, keys.stamina: 2, keys.behavior: HIT_AND_RUN,},
}

class Attribute_Distributor:
    # --- Difficulty Tuning Constants ---
    # 0.15 means +15% HP per floor, 0.10 means +10% Strength per floor
    HP_GROWTH_PER_FLOOR = 0.30 
    STR_GROWTH_PER_FLOOR = 0.20
    SOUL_GROWTH_PER_FLOOR = 0.10  # Players appreciate more rewards for harder fights!
    ELITE_MULTIPLIER = 2.0
    
    @staticmethod
    def Get_Enemy_Data(enemy_type, depth=1, is_elite=False):
        # Get base stats from classs, copy to prevent overwrite
        base_stats = ENEMY_STATS.get(enemy_type, {}).copy()
        
        # Only updates values which will scale with the dungeon
        base_stats[keys.health] = Attribute_Distributor.Get_Health(enemy_type, depth, is_elite)
        base_stats[keys.strength] = Attribute_Distributor.Get_Strength(enemy_type, depth, is_elite)
        base_stats[keys.souls] = Attribute_Distributor.Get_Soul_Value(enemy_type, depth, is_elite)

        return base_stats

    @staticmethod
    def Get_Stat(enemy_type, stat_key):
        # Get the sub-dictionary for the specific enemy
        enemy_data = ENEMY_STATS.get(enemy_type)
        
        if enemy_data:
            # Get the specific stat from that enemy's data
            return enemy_data.get(stat_key, 1) # Default to 1 if stat missing
            
        return 999 # Default if enemy type is totally missing
    
    @staticmethod  
    def Check_If_Elite(is_elite):
        if is_elite:
            return Attribute_Distributor.ELITE_MULTIPLIER

        return 1 # Return 1 to multiply as it will not update the value

    @staticmethod
    def Get_Health(type, dungeon_depth=1, is_elite=False):
        base_hp = Attribute_Distributor.Get_Stat(type, keys.health)
        
        # Formula: Base * (1 + (Growth * (Depth - 1)))
        # Floor 1 = 100%, Floor 2 = 115%, Floor 3 = 130%...
        scaled_hp = base_hp * (1 + (Attribute_Distributor.HP_GROWTH_PER_FLOOR * (dungeon_depth - 1)))
        
        scaled_hp *= Attribute_Distributor.Check_If_Elite(is_elite)
            
        return int(scaled_hp)

    @staticmethod
    def Get_Strength(type, dungeon_depth=1, is_elite=False):
        base_str = Attribute_Distributor.Get_Stat(type, keys.strength)
        
        scaled_str = base_str * (1 + (Attribute_Distributor.STR_GROWTH_PER_FLOOR * (dungeon_depth - 1)))
        
        # Elites hit harder too
        scaled_str *= Attribute_Distributor.Check_If_Elite(is_elite)
            
        return int(scaled_str)

    @staticmethod
    def Get_Soul_Value(type, dungeon_depth=1, is_elite=False):
        base_souls = Attribute_Distributor.Get_Stat(type, keys.souls)
        
        scaled_souls = base_souls * (1 + (Attribute_Distributor.SOUL_GROWTH_PER_FLOOR * (dungeon_depth - 1)))
        
        # Elites are worth way more
        scaled_souls *= Attribute_Distributor.Check_If_Elite(is_elite)
        
        return int(scaled_souls)

    @staticmethod
    def Convert_Behavior_To_String(value):
        behavior_dict = {
            LONG_RANGE : keys.long_range,
            MEDIUM_RANGE : keys.medium_range,
            SHORT_RANGE : keys.short_range,
            HIT_AND_RUN : keys.hit_and_run,
            HYBRID : keys.hybrid,
            PLACE_HOLDER6 : keys.place_holder,
            PLACE_HOLDER7 : keys.place_holder,
            PLACE_HOLDER8 : keys.place_holder,
            RETREAT_WHEN_DAMAGED : keys.retreat_when_damaged,
            DIRECT_ATTACK : keys.direct_attack,
        }

        return behavior_dict.get(value, keys.direct_attack)