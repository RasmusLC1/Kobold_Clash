from scripts.engine.keys.keys import keys
from dataclasses import replace
from scripts.entities.moving_entities.enemies.attribute_distributor.skeleton_stats import SKELETON_STATS
from scripts.entities.moving_entities.enemies.attribute_distributor.void_spawn_stats import VOID_SPAWN_STATS
from scripts.entities.moving_entities.enemies.attribute_distributor.dweller_stats import DWELLER_STATS
from scripts.entities.moving_entities.enemies.attribute_distributor.elemental_stats import ELEMENTAL_STATS
from scripts.entities.moving_entities.enemies.attribute_distributor.mythicals_stats import MYTHICALS_STATS



# 1. The Source of Truth - All stats in one place
ENEMY_STATS = {
        **SKELETON_STATS,
        **VOID_SPAWN_STATS,
        **DWELLER_STATS,
        **ELEMENTAL_STATS,
        **MYTHICALS_STATS
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

        # Return a NEW Enemy_Base_State with the updated values
        return replace(
            base_state, 
            health=scaled_health, 
            strength=scaled_strength, 
            souls=scaled_souls
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