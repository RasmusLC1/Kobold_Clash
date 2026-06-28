"""
test_abilities.py
-----------------
Unit tests for the ability system: passive abilities, active abilities,
the Ability_Handler lifecycle, and concrete ability implementations.

Extracted from test_enemy_ai.py so AI behaviour tests (pathfinding, movement
strategies, behavior manager) live separately in test_enemy_ai.py.
"""

import pytest
import pygame
from unittest.mock import MagicMock, patch

from scripts.engine.keys.keys import keys

# ---------------------------------------------------------------------------
# Force all @register_ability decorators to run before any test resolves a
# registry key.  Importing these modules is enough — the decorator fires at
# import time and writes the class into ABILITY_REGISTRY.
# ---------------------------------------------------------------------------
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.gloom_stalker import Gloom_Stalker
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.damage_reduction.ethereal import Ethereal
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.crystal_scale import Crystal_Scale
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.explode_on_impact import Explode_On_Impact
from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.movement.jump_attack import Jump_Attack
from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.movement.dash import Dash
from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.support_nearby_enemies.support_nearby_entities import Support_Nearby_Entities
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.bone_seeker.bone_eater import Bone_Eater
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.bone_seeker.bone_ressurector import Bone_Resurrector
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.healing.galvanic_skin import Galvanic_Skin
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.healing.adaptability import Adaptability
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.damage_reduction.anti_magic import Anti_Magic
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.clatter.echo_shard import Echo_Shard
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.clatter.echo_teleport import Echo_Teleport
from scripts.entities.moving_entities.enemies.behavior.abilities.ability_handler import Ability_Handler


# ==============================================================================
# REGISTRY SMOKE TEST
# ==============================================================================

def test_ability_registry_is_populated():
    """
    Fails immediately if any ability module was not imported (decorator never
    ran).  Extend this list whenever you add a new ability.
    """
    from scripts.entities.moving_entities.enemies.behavior.abilities import registry
    expected_keys = [
        keys.crystal_scale,
        keys.gloom_stalker,
        keys.explode_on_impact,
    ]
    for key in expected_keys:
        assert key in registry.ABILITY_REGISTRY, (
            f"'{key}' missing from ABILITY_REGISTRY — import its module at the "
            f"top of this file so the @register_ability decorator runs."
        )


# ==============================================================================
# SHARED FIXTURES
# ==============================================================================

@pytest.fixture
def mock_game():
    game = MagicMock()
    game.tilemap.tile_size = 32
    game.player = MagicMock()
    game.player.pos = [200.0, 200.0]
    game.player.active_ability = None
    game.clatter = MagicMock()
    game.ray_caster = MagicMock()
    return game


@pytest.fixture
def mock_entity():
    entity = MagicMock()
    entity.pos = [64.0, 64.0]
    entity.target = [250.0, 250.0]
    entity.distance_to_player = 100.0
    entity.active_ability = None
    entity.size = (32, 32)
    entity.intelligence = 5
    entity.agility = 5
    entity.health = 100
    entity.damaged = False
    entity.saved_data = {}
    return entity


@pytest.fixture
def mock_ability_instance():
    """A fully configured mock of an active ability."""
    ability = MagicMock()
    ability.name = "mock_dash"
    ability.is_passive = False
    ability.cooldown = 0
    ability.Get_Cooldown.return_value = 0
    ability.Update_Cooldown.return_value = True
    ability.Check_Trigger_Cooldown.return_value = True
    ability.Check_If_Trigger.return_value = True
    ability.Activate.return_value = True
    ability.Check_If_Attack_Allowed.return_value = True
    return ability


# ==============================================================================
# 1. ABILITY_HANDLER LIFECYCLE TESTS
# ==============================================================================

def test_ability_handler_lazy_loading_via_getattr(mock_game, mock_entity):
    """__getattr__ should intercept registry keys and cache the instance.

    ABILITY_REGISTRY is a @property that forwards to registry.ABILITY_REGISTRY,
    so we patch the underlying module dict rather than assigning to the property.
    """
    handler = Ability_Handler(mock_game, mock_entity)

    mock_ability_cls = MagicMock()
    with patch(
        "scripts.entities.moving_entities.enemies.behavior.abilities.registry.ABILITY_REGISTRY",
        {"dash": mock_ability_cls},
    ):
        resolved_ability = handler.dash

    assert resolved_ability is not None
    mock_ability_cls.assert_called_once_with(mock_game, mock_entity, "dash")
    assert getattr(handler, "dash") == resolved_ability


def test_ability_handler_getattr_raises_error_on_missing_key(mock_game, mock_entity):
    handler = Ability_Handler(mock_game, mock_entity)

    with patch(
        "scripts.entities.moving_entities.enemies.behavior.abilities.registry.ABILITY_REGISTRY",
        {"dash": MagicMock()},
    ):
        with pytest.raises(AttributeError, match="has no registry or attribute mapping for 'unregistered_spell'"):
            _ = handler.unregistered_spell


def test_passive_ability_updates_independently(mock_game, mock_entity):
    """Passive abilities must update every frame regardless of active ability state."""
    handler = Ability_Handler(mock_game, mock_entity)
    mock_passive = MagicMock()
    mock_passive.is_passive = True

    handler.passive_abilities["crystal_scale"] = mock_passive
    handler.Update(delta_time=0.016)

    mock_passive.Update.assert_called_once_with(0.016)


def test_active_ability_execution_lifecycle_flow(mock_game, mock_entity, mock_ability_instance):
    """Full trigger path: check → activate → set running state."""
    handler = Ability_Handler(mock_game, mock_entity)
    handler.active_ability = mock_ability_instance
    mock_entity.active_ability = None

    triggered = handler.Update(delta_time=0.1)

    assert triggered is True
    assert handler.is_running_ability is True
    mock_ability_instance.Activate.assert_called_once()
    mock_entity.Set_Active_Ability.assert_called_once_with("mock_dash")


def test_active_ability_removal_on_cooldown_detection(mock_game, mock_entity, mock_ability_instance):
    """Once an ability sets its cooldown the handler must drop back to idle state."""
    handler = Ability_Handler(mock_game, mock_entity)
    handler.active_ability = mock_ability_instance
    handler.is_running_ability = True

    mock_ability_instance.Get_Cooldown.return_value = 3.5

    handler.Update(delta_time=0.1)

    assert handler.is_running_ability is False
    assert mock_ability_instance in handler.abilities_on_cooldown
    mock_entity.Remove_Active_Ability.assert_called_once()


def test_ability_handler_save_and_load_data_restoration(mock_game, mock_entity):
    """Complete Save → Load round-trip should restore all ability references."""
    handler = Ability_Handler(mock_game, mock_entity)
    mock_entity.saved_data = {}

    mock_active = MagicMock()
    mock_active.name = "dash"
    handler.active_ability = mock_active

    mock_passive = MagicMock()
    handler.passive_abilities["gloom_stalker"] = mock_passive

    handler.Save_Data()
    assert mock_entity.saved_data['active_ability_key'] == "dash"
    assert "gloom_stalker" in mock_entity.saved_data['passive_abilities_keys']
    mock_active.Save_Data.assert_called_once()
    mock_passive.Save_Data.assert_called_once()

    mock_data = {
        'active_ability_key': 'dash',
        'passive_abilities_keys': ['gloom_stalker'],
        'cooldown_keys': ['dash'],
        'is_running_ability': True,
        'cooldown': 10,
        'trigger_cooldown': 0,
    }

    with patch.object(handler, 'Get_Ability') as mock_get:
        handler.Load_Data(mock_data)
        assert handler.is_running_ability is True
        assert mock_get.call_count == 2  # 1 active + 1 passive


# ==============================================================================
# 2. ETHEREAL PASSIVE — PHYSICAL IMMUNITY
# ==============================================================================

def test_ethereal_passive_damage_mitigation(mock_game, mock_entity):
    mock_entity.is_ethereal = False
    def set_ethereal(val): mock_entity.is_ethereal = val
    mock_entity.Set_Ethereal = set_ethereal

    ethereal_passive = Ethereal(mock_game, mock_entity, "ethereal")
    assert mock_entity.is_ethereal is True

    assert ethereal_passive.Damage_Taken(15, ("slash",), (1, 0), None) == 0
    assert ethereal_passive.Damage_Taken(22, ("blunt",), (0, 1), None) == 0
    assert ethereal_passive.Damage_Taken(10, ("electric",), (0, 0), None) == 10


# ==============================================================================
# 3. GLOOM STALKER — DARKNESS BUFF TOGGLE
# ==============================================================================

@pytest.fixture
def mock_gloom_stalker_entity(mock_entity):
    mock_entity.light_level = 200
    mock_entity.strength = 10
    mock_entity.max_speed_holder = 5
    mock_entity.Set_Strength = MagicMock()
    mock_entity.Set_Max_Speed = MagicMock()
    mock_entity.Set_Description = MagicMock()
    return mock_entity


def test_gloom_stalker_enters_darkness_applies_buff(mock_game, mock_gloom_stalker_entity):
    ability = Gloom_Stalker(mock_game, mock_gloom_stalker_entity, "gloom_stalker")

    mock_gloom_stalker_entity.light_level = 100
    ability.Update(delta_time=0.1)

    mock_gloom_stalker_entity.Set_Strength.assert_called_once_with(20)
    mock_gloom_stalker_entity.Set_Max_Speed.assert_called_once_with(10)
    mock_gloom_stalker_entity.Set_Description.assert_called_once()
    assert ability.light_level_holder == 100


def test_gloom_stalker_remains_in_darkness_does_not_stack(mock_game, mock_gloom_stalker_entity):
    ability = Gloom_Stalker(mock_game, mock_gloom_stalker_entity, "gloom_stalker")
    ability.light_level_holder = 100
    mock_gloom_stalker_entity.light_level = 50

    ability.Update(delta_time=0.1)

    mock_gloom_stalker_entity.Set_Strength.assert_not_called()
    mock_gloom_stalker_entity.Set_Max_Speed.assert_not_called()


def test_gloom_stalker_leaves_darkness_removes_buff(mock_game, mock_gloom_stalker_entity):
    ability = Gloom_Stalker(mock_game, mock_gloom_stalker_entity, "gloom_stalker")
    ability.light_level_holder = 100
    mock_gloom_stalker_entity.strength = 20
    mock_gloom_stalker_entity.light_level = 200

    ability.Update(delta_time=0.1)

    mock_gloom_stalker_entity.Set_Strength.assert_called_once_with(10)
    mock_gloom_stalker_entity.Set_Max_Speed.assert_called_once_with(2)
    mock_gloom_stalker_entity.Set_Description.assert_called_once()
    assert ability.light_level_holder == 200


def test_gloom_stalker_darkness_buff_toggle_boundaries(mock_game):
    """Stat changes must be stateful — strength feeds back into the next division."""
    mock_entity = MagicMock()
    mock_entity.strength = 10
    mock_entity.max_speed_holder = 4.0

    def update_strength(new_val):
        mock_entity.strength = new_val
    mock_entity.Set_Strength.side_effect = update_strength

    gloom = Gloom_Stalker(mock_game, mock_entity, "gloom_stalker")

    mock_entity.light_level = 50
    gloom.Update(0.1)
    mock_entity.Set_Strength.assert_called_with(20)
    mock_entity.Set_Max_Speed.assert_called_with(8.0)

    mock_entity.light_level = 200
    gloom.Update(0.1)
    mock_entity.Set_Strength.assert_called_with(10)


# ==============================================================================
# 4. CRYSTAL SCALE — SHIELD ABSORPTION
# ==============================================================================

def test_crystal_scale_shield_absorption_breakthrough(mock_game, mock_entity):
    mock_entity.max_health = 40
    mock_entity.pos = pygame.math.Vector2(100, 120)
    mock_game.assets = {"crystal_scale_bar": MagicMock()}

    shield = Crystal_Scale(mock_game, mock_entity, "crystal_scale")
    shield.crystal_scale_max = 10
    shield.crystal_scale = 10

    rem_damage = shield.Damage_Taken(12, "normal", (0, 0), None)
    assert shield.crystal_scale == 0
    assert rem_damage == 2


# ==============================================================================
# 5. EXPLODE ON IMPACT
# ==============================================================================

@pytest.fixture
def mock_poison_elemental_entity(mock_entity):
    mock_entity.distance_to_player = 100.0
    mock_entity.pushed_entities = []
    mock_entity.health = 10
    mock_entity.Delete = MagicMock(return_value=True)
    return mock_entity


def test_explode_on_impact_skips_when_far_from_player(mock_game, mock_poison_elemental_entity):
    mock_poison_elemental_entity.distance_to_player = 61.0
    mock_poison_elemental_entity.pushed_entities = ["some_entity"]

    ability = Explode_On_Impact(mock_game, mock_poison_elemental_entity, "explode_on_impact")
    result = ability.Update(delta_time=0.1)

    assert result is False
    assert mock_poison_elemental_entity.health > 0
    mock_poison_elemental_entity.Delete.assert_not_called()


def test_explode_on_impact_skips_when_no_impact_registered(mock_game, mock_poison_elemental_entity):
    mock_poison_elemental_entity.distance_to_player = 30.0
    mock_poison_elemental_entity.pushed_entities = []

    ability = Explode_On_Impact(mock_game, mock_poison_elemental_entity, "explode_on_impact")
    result = ability.Update(delta_time=0.1)

    assert result is False
    assert mock_poison_elemental_entity.health > 0
    mock_poison_elemental_entity.Delete.assert_not_called()


def test_explode_on_impact_detonates_successfully(mock_game, mock_poison_elemental_entity):
    mock_poison_elemental_entity.distance_to_player = 45.0
    mock_poison_elemental_entity.pushed_entities = ["player_hitbox"]

    ability = Explode_On_Impact(mock_game, mock_poison_elemental_entity, "explode_on_impact")
    result = ability.Update(delta_time=0.1)

    assert result is True
    assert mock_poison_elemental_entity.health == 0
    mock_poison_elemental_entity.Delete.assert_called_once_with(generate_soul=False)


# ==============================================================================
# 6. GALVANIC SKIN — ELEMENTAL ABSORPTION & HEALING
# ==============================================================================

@pytest.fixture
def mock_galvanic_entity(mock_entity):
    mock_entity.Set_Effect = MagicMock()
    return mock_entity


def test_healing_from_damage_type_absorbs_and_heals(mock_game, mock_galvanic_entity):
    keys.healing = "healing"
    keys.electric = "electric"

    galvanic = Galvanic_Skin(mock_game, mock_galvanic_entity, "galvanic_skin")

    final_damage = galvanic.Damage_Taken(
        damage=10,
        effect=(keys.electric, 5),
        direction=(1, 0),
        attacker=None,
    )

    assert final_damage == 0
    mock_galvanic_entity.Set_Effect.assert_any_call(keys.healing, 5)
    mock_galvanic_entity.Set_Effect.assert_any_call("electric_resistance", 2)


def test_healing_from_damage_type_ignores_null_effects(mock_game, mock_galvanic_entity):
    galvanic = Galvanic_Skin(mock_game, mock_galvanic_entity, "galvanic_skin")

    final_damage = galvanic.Damage_Taken(
        damage=15,
        effect=(None, 0),
        direction=(0, 1),
        attacker=None,
    )

    assert final_damage == 15
    mock_galvanic_entity.Set_Effect.assert_not_called()


def test_healing_from_damage_type_handles_odd_numbered_damage_flooring(mock_game, mock_galvanic_entity):
    keys.healing = "healing"
    keys.electric = "electric"

    galvanic = Galvanic_Skin(mock_game, mock_galvanic_entity, "galvanic_skin")
    final_damage = galvanic.Damage_Taken(15, (keys.electric, 3), (0, 0), None)

    assert final_damage == 0
    mock_galvanic_entity.Set_Effect.assert_any_call(keys.healing, 7)


# ==============================================================================
# 7. ADAPTABILITY — REACTIVE ELEMENT SHIFTING
# ==============================================================================

def test_adaptability_takes_damage_first_then_adapts(mock_game, mock_galvanic_entity):
    keys.fire = "fire"
    keys.healing = "healing"

    ability = Adaptability(mock_game, mock_galvanic_entity, "adaptability")
    assert ability.effect_name is None

    first_hit_damage = ability.Damage_Taken(20, (keys.fire, 5), (1, 0), None)

    assert first_hit_damage == 20
    assert ability.effect_name == keys.fire
    mock_galvanic_entity.Set_Effect.assert_not_called()


def test_adaptability_absorbs_same_element_on_subsequent_hits(mock_game, mock_galvanic_entity):
    keys.fire = "fire"
    keys.healing = "healing"

    ability = Adaptability(mock_game, mock_galvanic_entity, "adaptability")
    ability.effect_name = keys.fire

    second_hit_damage = ability.Damage_Taken(20, (keys.fire, 5), (1, 0), None)

    assert second_hit_damage == 0
    mock_galvanic_entity.Set_Effect.assert_any_call(keys.healing, 10)
    mock_galvanic_entity.Set_Effect.assert_any_call("fire_resistance", 2)


def test_adaptability_shifts_learning_when_hit_by_new_element(mock_game, mock_galvanic_entity):
    keys.fire = "fire"
    keys.ice = "ice"

    ability = Adaptability(mock_game, mock_galvanic_entity, "adaptability")
    ability.effect_name = keys.fire

    hit_damage = ability.Damage_Taken(30, (keys.ice, 2), (1, 0), None)

    assert hit_damage == 30
    assert ability.effect_name == keys.ice


# ==============================================================================
# 8. ANTI-MAGIC — ELEMENTAL BLOCKING
# ==============================================================================

def test_anti_magic_blocks_elements_retains_melee(mock_game, mock_entity):
    ability = Anti_Magic(mock_game, mock_entity, "anti_magic")

    assert ability.Damage_Taken(15, keys.slash, (1, 0), None) == 15
    assert ability.Damage_Taken(12, keys.blunt, (1, 0), None) == 12
    assert ability.Damage_Taken(45, "fire_magic", (1, 0), None) == 0
    assert ability.Damage_Taken(99, "lightning", (1, 0), None) == 0


# ==============================================================================
# 9. BONE SEEKER ABILITIES
# ==============================================================================

def test_bone_seeker_delta_time_throttling_and_cleanup(mock_game, mock_entity):
    mock_game.tilemap = MagicMock()
    mock_game.enemy_handler = MagicMock()

    bone_seeker = Bone_Resurrector(mock_game, mock_entity, "bone_resurrector")

    destroyed_bone = MagicMock()
    destroyed_bone.is_destroyed = True
    bone_seeker.target_bones = destroyed_bone
    bone_seeker.target_bones_collision_cooldown = 0

    bone_seeker.Update(delta_time=0.1)
    assert bone_seeker.target_bones is None


def test_bone_seeker_collision_and_consumption_trigger(mock_game, mock_entity):
    mock_game.particle_handler = MagicMock()

    bone_seeker = Bone_Eater(mock_game, mock_entity, "bone_eater")
    mock_bone = MagicMock()
    mock_bone.is_destroyed = False
    bone_seeker.target_bones = mock_bone
    bone_seeker.target_bones_collision_cooldown = 0

    mock_entity.rect = MagicMock(return_value=pygame.Rect(0, 0, 32, 32))
    mock_bone.rect = MagicMock(return_value=pygame.Rect(10, 10, 32, 32))

    bone_seeker.Update(delta_time=0.1)

    mock_bone.Consume.assert_called_once()
    assert bone_seeker.target_bones is None


# ==============================================================================
# 10. SUPPORT NEARBY ENTITIES
# ==============================================================================

def test_support_nearby_entities_empty_or_failed_activation(mock_game, mock_entity):
    mock_game.enemy_handler.Find_Nearby_Enemies.return_value = []

    support_spell = Support_Nearby_Entities(
        mock_game, mock_entity, "rally", "strength_buff", "rally_particle", radius=100
    )

    success = support_spell.Activate()
    assert success is True
    mock_game.particle_handler.Activate_Particles.assert_not_called()


# ==============================================================================
# 11. JUMP ATTACK
# ==============================================================================

def test_jump_attack_movement_reduction_gate(mock_game, mock_entity):
    jump_attack = Jump_Attack(mock_game, mock_entity, "jump")
    jump_attack.wait_before_jump_cooldown = 1.5
    jump_attack.jump_trigged = False

    jump_attack.Update(delta_time=0.5)

    mock_entity.Reduce_Movement.assert_called_with(10000)
    assert jump_attack.jump_trigged is False


# ==============================================================================
# 12. ECHO SHARD — STEALTH & CLATTER REVEAL
# ==============================================================================

@pytest.fixture
def echo_shard_context():
    game = MagicMock()
    entity = MagicMock()
    game.clatter.Check_If_Noise_Generated.return_value = None
    ability = Echo_Shard(game, entity, "echo_shard")
    return game, entity, ability


def test_echo_shard_initializes_hidden(echo_shard_context):
    game, entity, ability = echo_shard_context

    assert ability.clatter_cooldown == 0.01
    assert ability.is_revealed is False

    ability.Update(delta_time=0.016)

    assert ability.clatter_cooldown <= 0
    entity.Set_Effect.assert_called_once_with(effect=keys.invisibility, duration=6, permanent=True)


def test_clatter_detection_reveals_enemy(echo_shard_context):
    game, entity, ability = echo_shard_context
    ability.clatter_cooldown = 0.0
    ability.is_revealed = False

    ability.On_Clatter_Heard((500, 500))

    assert ability.is_revealed is True
    assert ability.clatter_cooldown == 10.0
    entity.Remove_Effect.assert_called_once_with(effect=keys.invisibility, reduce_permanent=6)


def test_subsequent_clatter_refreshes_timer_without_re_removing_effect(echo_shard_context):
    game, entity, ability = echo_shard_context
    ability.is_revealed = True
    ability.clatter_cooldown = 4.0
    entity.Remove_Effect.reset_mock()

    ability.On_Clatter_Heard((200, 200))

    assert ability.clatter_cooldown == 10.0
    entity.Remove_Effect.assert_not_called()


def test_timer_expiry_re_conceals_enemy(echo_shard_context):
    game, entity, ability = echo_shard_context
    ability.is_revealed = True
    ability.clatter_cooldown = 0.005

    ability.Update(delta_time=0.016)

    assert ability.is_revealed is False
    assert ability.clatter_cooldown <= 0
    entity.Set_Effect.assert_called_once_with(effect=keys.invisibility, duration=6, permanent=True)


# ==============================================================================
# 13. ECHO TELEPORT
# ==============================================================================
 
@pytest.fixture
def teleport_context():
    game = MagicMock()
    entity = MagicMock()
    entity.locked_on_target = False
    entity.distance_to_player = 300.0  # beyond TELEPORT_DISTANCE so Check_If_Trigger passes
    game.clatter.Check_If_Noise_Generated.return_value = None
    ability = Echo_Teleport(game, entity, "echo_teleport")
    return game, entity, ability
 
 
def test_update_ticks_cooldown_down(teleport_context):
    """Update should decrement the cooldown each frame."""
    game, entity, ability = teleport_context
    ability.teleport_cooldown = 1.0
 
    ability.Update(delta_time=0.5)
 
    assert ability.teleport_cooldown == pytest.approx(0.5)
 
 
def test_clatter_teleports_and_sets_cooldown(teleport_context):
    """On_Clatter_Heard should teleport near the clatter position and arm the cooldown."""
    game, entity, ability = teleport_context
 
    ability.On_Clatter_Heard((500, 500))
 
    entity.Set_Position.assert_called_once()
    actual_x, actual_y = entity.Set_Position.call_args[0][0]
    assert 300 <= actual_x <= 700
    assert 300 <= actual_y <= 700
    assert ability.teleport_cooldown > 0
 
 
def test_clatter_blocked_by_active_cooldown(teleport_context):
    """On_Clatter_Heard must do nothing while the cooldown is still running."""
    game, entity, ability = teleport_context
    ability.teleport_cooldown = 3.0
 
    ability.On_Clatter_Heard((500, 500))
 
    entity.Set_Position.assert_not_called()
 
 
def test_clatter_blocked_when_too_close_to_player(teleport_context):
    """Check_If_Trigger suppresses teleportation when the entity is already close."""
    game, entity, ability = teleport_context
    entity.distance_to_player = 50.0  # within TELEPORT_DISTANCE
 
    ability.On_Clatter_Heard((500, 500))
 
    entity.Set_Position.assert_not_called()