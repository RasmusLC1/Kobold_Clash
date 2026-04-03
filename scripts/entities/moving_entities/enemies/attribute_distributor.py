from scripts.engine.keys.keys import keys

# 1. The Source of Truth - All stats in one place
ENEMY_STATS = {
    # [Undead / Crypt]
    keys.skeleton_warrior:        {keys.health: 70,  keys.souls: 10, keys.max_weapon_charge: 0.8, keys.aggression: 7,  keys.strength: 3, keys.speed: 3, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2},
    keys.skeleton_ranger:         {keys.health: 40,  keys.souls: 15, keys.max_weapon_charge: 1.2, keys.aggression: 4,  keys.strength: 2, keys.speed: 4, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2},
    keys.skeleton_cleric:         {keys.health: 40,  keys.souls: 20, keys.max_weapon_charge: 1.1, keys.aggression: 2,  keys.strength: 1, keys.speed: 2, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2},
    keys.skeleton_bell_toller:    {keys.health: 60,  keys.souls: 15, keys.max_weapon_charge: 1.2, keys.aggression: 3,  keys.strength: 3, keys.speed: 3, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2},
    keys.skeleton_undertaker:     {keys.health: 110, keys.souls: 40, keys.max_weapon_charge: 0.8,  keys.aggression: 5, keys.strength: 5, keys.speed: 2, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2},
    keys.skeleton_guardian:       {keys.health: 120, keys.souls: 15, keys.max_weapon_charge: 1.2, keys.aggression: 7,  keys.strength: 4, keys.speed: 1, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2},
    keys.skeleton_warlock:        {keys.health: 40,  keys.souls: 40, keys.max_weapon_charge: 1.0, keys.aggression: 6,  keys.strength: 1, keys.speed: 1, keys.agility: 2, keys.intelligence: 5, keys.stamina: 2},
    keys.wight_king:              {keys.health: 200, keys.souls: 55, keys.max_weapon_charge: 0.6, keys.aggression: 6,  keys.strength: 6, keys.speed: 4, keys.agility: 6, keys.intelligence: 5, keys.stamina: 5},
    keys.skeleton_banner_bearer:  {keys.health: 50,  keys.souls: 15, keys.max_weapon_charge: 1.0, keys.aggression: 2,  keys.strength: 1, keys.speed: 2, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2},
    keys.phantom:                 {keys.health: 20,  keys.souls: 30, keys.max_weapon_charge: 0.6, keys.aggression: 10, keys.strength: 5, keys.speed: 6, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2},
    keys.wraith:                  {keys.health: 50,  keys.souls: 25, keys.max_weapon_charge: 1.0, keys.aggression: 8,  keys.strength: 3, keys.speed: 4, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2},
    keys.shade:                   {keys.health: 50,  keys.souls: 20, keys.max_weapon_charge: 1.0, keys.aggression: 9,  keys.strength: 3, keys.speed: 1, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2},
    keys.vampire:                 {keys.health: 150, keys.souls: 60, keys.max_weapon_charge: 0.5, keys.aggression: 6,  keys.strength: 4, keys.speed: 3, keys.agility: 3, keys.intelligence: 2, keys.stamina: 2},
    keys.ghoul:                   {keys.health: 80,  keys.souls: 20, keys.max_weapon_charge: 0.8, keys.aggression: 8,  keys.strength: 6, keys.speed: 6, keys.agility: 2, keys.intelligence: 2, keys.stamina: 2},

    # [Crystal Caverns]
    keys.fire_spirit:             {keys.health: 40, keys.souls: 20, keys.max_weapon_charge: 1.4, keys.aggression: 7,  keys.strength: 4, keys.speed: 4, keys.agility: 4, keys.intelligence: 2, keys.stamina: 2},
    keys.ice_spirit:              {keys.health: 50, keys.souls: 20, keys.max_weapon_charge: 1.6, keys.aggression: 5,  keys.strength: 7, keys.speed: 3, keys.agility: 3, keys.intelligence: 2, keys.stamina: 2},
    keys.earth_elemental:         {keys.health: 80, keys.souls: 30, keys.max_weapon_charge: 1.6, keys.aggression: 8,  keys.strength: 7, keys.speed: 2, keys.agility: 3, keys.intelligence: 2, keys.stamina: 2},
    keys.electric_elemental:      {keys.health: 50, keys.souls: 30, keys.max_weapon_charge: 3.0, keys.aggression: 3,  keys.strength: 4, keys.speed: 2, keys.agility: 3, keys.intelligence: 2, keys.stamina: 2},
    keys.poison_elemental:        {keys.health: 20, keys.souls: 10, keys.max_weapon_charge: 0.1, keys.aggression: 10, keys.strength: 4, keys.speed: 4, keys.agility: 3, keys.intelligence: 2, keys.stamina: 2},
    keys.medusa:                  {keys.health: 20, keys.souls: 60, keys.max_weapon_charge: 0.9, keys.aggression: 6,  keys.strength: 4, keys.speed: 4, keys.agility: 3, keys.intelligence: 2, keys.stamina: 2},
    keys.minotaur:                {keys.health: 20, keys.souls: 55, keys.max_weapon_charge: 0.7, keys.aggression: 8,  keys.strength: 4, keys.speed: 4, keys.agility: 3, keys.intelligence: 2, keys.stamina: 2},
    keys.spider:                  {keys.health: 60, keys.souls: 20, keys.max_weapon_charge: 0.9, keys.aggression: 1,  keys.strength: 4, keys.speed: 6, keys.agility: 3, keys.intelligence: 5, keys.stamina: 2},
}

class Attribute_Distributor:
    # --- Difficulty Tuning Constants ---
    # 0.15 means +15% HP per floor, 0.10 means +10% Strength per floor
    HP_GROWTH_PER_FLOOR = 0.15 
    STR_GROWTH_PER_FLOOR = 0.10
    SOUL_GROWTH_PER_FLOOR = 0.05  # Players appreciate more rewards for harder fights!
    ELITE_MULTIPLIER = 2.0

    @staticmethod
    def Get_Stat(enemy_type, stat_key):
        # Get the sub-dictionary for the specific enemy
        enemy_data = ENEMY_STATS.get(enemy_type)
        
        if enemy_data:
            # et the specific stat from that enemy's data
            return enemy_data.get(stat_key, 1) # Default to 1 if stat missing
            
        return 999 # Default if enemy type is totally missing

    # TODO: Add elite and depth level variance to the enemies
    # For example if we are at level 1, it's the base values
    @staticmethod
    def Get_Health(type, dungeon_depth=1, is_elite=False):
        base_hp = Attribute_Distributor.Get_Stat(type, keys.health)
        
        # Formula: Base * (1 + (Growth * (Depth - 1)))
        # Floor 1 = 100%, Floor 2 = 115%, Floor 3 = 130%...
        scaled_hp = base_hp * (1 + (Attribute_Distributor.HP_GROWTH_PER_FLOOR * (dungeon_depth - 1)))
        
        if is_elite:
            scaled_hp *= Attribute_Distributor.ELITE_MULTIPLIER
            
        return int(scaled_hp)

    @staticmethod
    def Get_Strength(type, dungeon_depth=1, is_elite=False):
        base_str = Attribute_Distributor.Get_Stat(type, keys.strength)
        
        scaled_str = base_str * (1 + (Attribute_Distributor.STR_GROWTH_PER_FLOOR * (dungeon_depth - 1)))
        
        # Elites hit harder too
        if is_elite:
            scaled_str *= 1.5
            
        return int(scaled_str)

    @staticmethod
    def Get_Soul_Value(type, dungeon_depth=1, is_elite=False):
        base_souls = Attribute_Distributor.Get_Stat(type, keys.souls)
        
        scaled_souls = base_souls * (1 + (Attribute_Distributor.SOUL_GROWTH_PER_FLOOR * (dungeon_depth - 1)))
        
        # Elites are worth way more
        if is_elite:
            scaled_souls *= Attribute_Distributor.ELITE_MULTIPLIER
            
        return int(scaled_souls)

    # The methods below do not scale
    @staticmethod
    def Get_Stamina(type):
        return Attribute_Distributor.Get_Stat(type, keys.stamina)

    @staticmethod
    def Get_Agility(type):
        return Attribute_Distributor.Get_Stat(type, keys.agility)
    

    @staticmethod
    def Get_Speed(type):
        return Attribute_Distributor.Get_Stat(type, keys.speed)
    
    @staticmethod
    def Get_Intelligence(type):
        return Attribute_Distributor.Get_Stat(type, keys.intelligence)
    
    
    @staticmethod
    def Get_Max_Weapon_Charge(type):
        return Attribute_Distributor.Get_Stat(type, keys.max_weapon_charge)
    
    @staticmethod
    def Get_Aggression(type):
        return Attribute_Distributor.Get_Stat(type, keys.aggression)