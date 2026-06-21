from scripts.engine.keys.enemy import Enemy as enemy_keys
from scripts.entities.moving_entities.enemies.attribute_distributor.enemy_base_state import Enemy_Base_State

MYTHICALS_STATS = {
    enemy_keys.medusa: Enemy_Base_State(
        health=20,
        souls=60,
        size=(64, 64),
        max_weapon_charge=0.9,
        strength=4,
        speed=4,
        agility=3,
        intelligence=2,
        stamina=2,
        behavior=enemy_keys.short_range,
        ability=None,
        idle_animation=5,
        run_animation=3,
        attack_animation=5,
        sub_category=enemy_keys.mythical
    ),

    enemy_keys.minotaur: Enemy_Base_State(
        health=20,
        souls=55,
        size=(64, 64),
        max_weapon_charge=0.7,
        strength=4,
        speed=4,
        agility=3,
        intelligence=2,
        stamina=2,
        behavior=enemy_keys.hybrid,
        ability=enemy_keys.rage,
        idle_animation=3,
        run_animation=3,
        attack_animation=5,
        sub_category=enemy_keys.mythical
    ),
}