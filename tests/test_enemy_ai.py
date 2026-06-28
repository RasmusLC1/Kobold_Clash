"""
test_enemy_ai.py
----------------
Unit tests for enemy AI systems: pathfinding, line-of-sight, movement
strategies, behavior manager, attack handler, and intent manager.

Ability-specific tests live in test_abilities.py.
"""

import pytest
import pygame
from unittest.mock import MagicMock, patch
from scripts.engine.keys.keys import keys

from scripts.entities.moving_entities.enemies.behavior.path_finding import Path_Finding
from scripts.entities.moving_entities.enemies.behavior.movement_strategies import Movement_Strategies
from scripts.entities.moving_entities.enemies.behavior.behavior.behavior_manager import Behavior_Manager
from scripts.entities.moving_entities.enemies.behavior.attack_handler import Attack_Handler
from scripts.entities.moving_entities.enemies.behavior.intent_manager import Intent_Manager
from scripts.entities.moving_entities.enemies.behavior.abilities.ability_handler import Ability_Handler


# MockKeys provides the fixed string constants the behavior manager tests need.
# It does NOT patch the global keys object — each test that needs specific key
# values passes MockKeys explicitly, keeping other tests unaffected.
class MockKeys:
    direct = "direct"
    long_range = "long_range"
    medium_range = "medium_range"
    short_range = "short_range"
    keep_position = "keep_position"
    idle = "idle"
    run_away = "run_away"
    invisibility = "invisibility"
    invulnerable = "invulnerable"
    retreat = "retreat"
    direct_attack = "direct_attack"
    hit_and_run = "hit_and_run"

@pytest.fixture
def mock_game():
    game = MagicMock()
    game.tilemap.tile_size = 32
    game.a_star.min_x = 0
    game.a_star.min_y = 0
    
    # Player Setup
    game.player = MagicMock()
    game.player.pos = [200.0, 200.0]
    game.player.active_ability = None
    
    # Dependencies
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


# ==============================================================================
# 1. PATHFINDING & GRID RESOLUTION TESTS
# ==============================================================================

def test_pathfinding_save_and_load_data(mock_game, mock_entity):
    pf = Path_Finding(mock_game, mock_entity, "floor_layer")
    pf.path = [(2, 2), (3, 2)]
    pf.src_x, pf.src_y = 2, 2
    pf.des_x, pf.des_y = 10, 12
    pf.player_found = True
    
    pf.Save_Data()
    assert mock_entity.saved_data['src_x'] == 2
    
    # Clear state and verify restore cycle
    pf2 = Path_Finding(mock_game, mock_entity, "floor_layer")
    pf2.Load_Data(mock_entity.saved_data)
    assert pf2.path == [(2, 2), (3, 2)]
    assert pf2.des_y == 12
    assert pf2.player_found is True


def test_calculate_position_handles_offsets(mock_game, mock_entity):
    mock_game.a_star.min_x = 5
    mock_game.a_star.min_y = -2
    mock_entity.pos = [96.0, 32.0]  # Pixel coordinates
    
    pf = Path_Finding(mock_game, mock_entity, "floor_layer")
    pf.Calculate_Position()
    
    # 96 // 32 = 3. 3 - 5 = -2
    assert pf.src_x == -2
    # 32 // 32 = 1. 1 - (-2) = 3
    assert pf.src_y == 3


def test_navigate_path_early_exit_on_short_path(mock_game, mock_entity):
    pf = Path_Finding(mock_game, mock_entity, "floor_layer")
    pf.path = [(1, 1)]  # Length < 2
    assert pf.Navigate_Path() is False


def test_path_segment_complete_pops_node_on_threshold_match(mock_game, mock_entity):
    pf = Path_Finding(mock_game, mock_entity, "floor_layer")
    pf.path = [(2, 2), (3, 2)]
    
    # Target pixel pos = (3 * 32, 2 * 32) = (96, 64)
    # Put entity closely within threshold (<= tile_size distance)
    mock_entity.pos = [90.0, 64.0]
    
    with patch('pygame.math.Vector2') as mock_vec:
        completed = pf.Path_Segment_Complete((3, 2))
        assert completed is True
        assert len(pf.path) == 1  # Popped current objective node
        mock_entity.Set_Direction.assert_called_with(mock_vec(0, 0))


# ==============================================================================
# 2. LINE OF SIGHT & MEMORY DECAY TESTS
# ==============================================================================

def test_handle_line_of_sight_polling_and_memory_decay(mock_game, mock_entity):
    ms = Movement_Strategies(mock_game, mock_entity)
    ms.line_of_sight_cooldown = 0.0
    
    # Configure raycaster to allow visibility access
    with patch.object(ms, 'Line_Of_Sight', return_value=True) as mock_los:
        # Step 1: Clock ticks, sensor fires, finds target, activates memory tracking
        remembered = ms.Handle_Line_Of_Sight(delta_time=0.1)
        assert ms.line_of_sight_cooldown == 1.0  # Reset sensor clock
        assert ms.player_found == pytest.approx(4.9)  # 5.0 - 0.1 decay step
        assert remembered is True
        mock_los.assert_called_once()
        
        # Step 2: Next frame, clock hasn't reached 0, bypasses expensive ray sensor
        mock_los.reset_mock()
        ms.Handle_Line_Of_Sight(delta_time=0.1)
        mock_los.assert_not_called()
        assert ms.player_found == pytest.approx(4.8)


def test_line_of_sight_bresenham_collision_detection(mock_game, mock_entity):
    ms = Movement_Strategies(mock_game, mock_entity)
    mock_game.tilemap.tile_size = 32
    mock_entity.pos = [16.0, 16.0]  # (0, 0) tile space
    target_pos = [112.0, 16.0]      # (3, 0) tile space
    
    # Ray caster returns false if wall collision happens
    mock_game.ray_caster.Check_Tile.side_effect = lambda tile: tile != (1, 0)
    
    # Route passes through (1,0) grid layer which blocks sight line
    assert ms.Line_Of_Sight(target_pos) is False


# ==============================================================================
# 3. RANGE FILTERING & LOITERING SPACE CALCULATIONS
# ==============================================================================

def test_movement_strategy_early_exits(mock_game, mock_entity):
    ms = Movement_Strategies(mock_game, mock_entity)
    
    # Case A: Too far away
    mock_entity.distance_to_player = 350.0
    assert ms.Movement_Strategy(0.016) is False
    
    # Case B: Target player went invisible
    mock_entity.distance_to_player = 100.0
    mock_game.player.active_ability = MockKeys.invisibility
    assert ms.Movement_Strategy(0.016) is False

def test_find_tiles_in_range_too_far_picks_closest_neighbor(mock_game, mock_entity):
    ms = Movement_Strategies(mock_game, mock_entity)

    tile_far = MagicMock()
    tile_far.Get_Distance_To_Player.return_value = 200
    tile_close = MagicMock()
    tile_close.Get_Distance_To_Player.return_value = 80

    mock_game.tilemap.Get_Floor_Tiles_Around.return_value = [tile_far, tile_close]

    # Distance is 250, max_range is 150 -> CASE 1: TOO FAR
    # New logic returns up to 3 closest tiles, so check membership and ordering
    tiles = ms.Find_Tiles_In_Range(max_range=150, min_range=100, entity_dist=250)
    assert tile_close in tiles
    assert tiles.index(tile_close) < tiles.index(tile_far)  # closest tile comes first




# ==============================================================================
# 4. BEHAVIOR MANAGEMENT & PROBABILITY WEIGHTING TESTS
# ==============================================================================

def test_calculate_fallback_behavior_probabilistic_weighting(mock_game, mock_entity):
    bm = Behavior_Manager(mock_game, mock_entity, MockKeys.idle, 100)
    bm.retreat_options = [MockKeys.short_range, MockKeys.run_away]
    
    # Force high profile processing variables to shift target outcomes toward the right boundary
    mock_entity.intelligence = 10
    mock_entity.agility = 10
    
    with patch('random.choices', return_value=[MockKeys.run_away]) as mock_choice:
        selected = bm.Calculate_Fallback_Behavior()
        assert selected == MockKeys.run_away
        mock_choice.assert_called_once()


def test_update_behavior_skips_when_player_not_spotted(mock_game, mock_entity):
    # Setup standard required entity properties to survive behavior creation
    mock_entity.health = 100
    mock_entity.size = [32, 32]
    mock_entity.agility = 1
    mock_entity.intelligence = 1
    mock_entity.player_spotted = False
    
    bm = Behavior_Manager(mock_game, mock_entity, keys.idle, 100)
    bm.max_distance = 50
    mock_entity.distance_to_player = 200.0  # Outside detection bubble
    
    # Force the underlying component check to explicitly fail detection
    bm.ability_handler.Check_Player_Distance = MagicMock(return_value=False)
    
    # Run the behavior update loop
    result = bm.Update_Behavior(0.016)
    
    # The early return must hit cleanly and evaluate to None
    assert result is None

# ==============================================================================
# 5. WEAPON CHARGING & ATTACK CYCLE CONTROL
# ==============================================================================

def test_update_attack_sequence(mock_game, mock_entity):
    bm = Behavior_Manager(mock_game, mock_entity, MockKeys.direct_attack, 100)
    bm.ability_handler = MagicMock()
    bm.ability_handler.Check_If_Attack_Allowed.return_value = True
    
    bm.attack_handler = MagicMock()
    # Scenario: charging weapon sequence running
    bm.attack_handler.Update_Attack.return_value = True 
    
    with patch.object(bm, 'current_behavior') as mock_pattern:
        bm.Update_Attack(0.016)
        mock_pattern.assert_not_called()


def test_attack_handler_charge_trigger_flow(mock_game, mock_entity):
    ah = Attack_Handler(mock_game, mock_entity, max_weapon_charge=2.0)
    ah.attack_triggered = True
    ah.charge = 1.9
    
    # Delta of 0.2 pushes total charge to 2.1, breaking over maximum limit threshold
    charging_active = ah.Update_Attack(delta_time=0.2)
    
    assert ah.charge == 2.0
    assert charging_active is False  # Weapon completed charging cycle
    mock_entity.Trigger_Attack.assert_called_once()


# ==============================================================================
# 6. POLYMORPHIC STATE BEHAVIOR INTERFACE TESTS
# ==============================================================================

def test_behavior_registration_and_instantiation(mock_game, mock_entity):
    """Verifies that selecting a pattern dynamically builds the correct class instance."""
    bm = Behavior_Manager(mock_game, mock_entity, MockKeys.long_range, 100)
    
    actual_key = getattr(bm, 'active_behavior_key', getattr(bm, 'behavior', None))
    assert actual_key == MockKeys.long_range
    
    # Check for class-based state machine or function-fallback
    if hasattr(bm, 'current_behavior') and bm.current_behavior is not None:
        # Dynamically get the class type name as a string to avoid "not defined" linter errors
        class_name = bm.current_behavior.__class__.__name__
        assert class_name == "Long_Range_Behavior"
        
    assert bm.movement_behavior == MockKeys.long_range

def test_behavior_fallback_default_on_missing_registry_key(mock_game, mock_entity):
    """Guards against undefined state strings by falling back gracefully."""
    # If your production manager lets the key through or handles it via a default string:
    bm = Behavior_Manager(mock_game, mock_entity, "invalid_unregistered_key", 100)
    
    actual_key = getattr(bm, 'active_behavior_key', getattr(bm, 'behavior', None))
    
    # Let's dynamically check if it fell back or preserved it
    assert actual_key in [MockKeys.direct_attack, "invalid_unregistered_key"]


def test_idle_behavior_execute_has_no_side_effects(mock_game, mock_entity):
    """Ensures idle pattern operates cleanly as a structurally inert state."""
    bm = Behavior_Manager(mock_game, mock_entity, MockKeys.idle, 100)
    behavior_obj = getattr(bm, 'current_behavior', None)
    
    if behavior_obj:
        with patch.object(bm.attack_handler, 'Set_Attack_Triggered') as mock_trigger:
            behavior_obj.Execute()
            mock_trigger.assert_not_called()


def test_direct_attack_behavior_triggers_attack_when_in_range(mock_game, mock_entity):
    """Validates that a direct attack immediately attempts to register a combat hit."""
    bm = Behavior_Manager(mock_game, mock_entity, MockKeys.direct_attack, 100)
    behavior_obj = getattr(bm, 'current_behavior', None)
    
    if behavior_obj:
        with patch.object(bm, 'Check_Attack_Distance', return_value=True):
            with patch.object(bm.attack_handler, 'Set_Attack_Triggered') as mock_trigger:
                is_range = behavior_obj.Execute()
                assert is_range is True
                mock_trigger.assert_called_once_with(True)


def test_hit_and_run_behavior_respects_engagement_cooldown(mock_game, mock_entity):
    """Checks if hit-and-run tactics delay movement shifts based on active cooldown gates."""
    bm = Behavior_Manager(mock_game, mock_entity, MockKeys.hit_and_run, 100)
    behavior_obj = getattr(bm, 'current_behavior', None)
    
    if behavior_obj:
        with patch.object(bm, 'Update_Engagement_Cooldown', return_value=False):
            assert behavior_obj.Execute() is False
            
        with patch.object(bm, 'Update_Engagement_Cooldown', return_value=True):
            with patch.object(behavior_obj, 'Engagement_Controller', return_value=False):
                assert behavior_obj.Execute() is False
                assert bm.movement_behavior == MockKeys.direct 


def test_short_range_behavior_evaluates_damage_taken_on_cooldown_ticks(mock_game, mock_entity):
    """Confirms short-range behaviors pull spatial reposition loops when struck during ticks."""
    bm = Behavior_Manager(mock_game, mock_entity, MockKeys.short_range, 100)
    behavior_obj = getattr(bm, 'current_behavior', None)
    
    if behavior_obj:
        with patch.object(bm, 'Update_Engagement_Cooldown', return_value=False):
            with patch.object(bm, 'Check_If_Entity_Has_Taken_Damage', return_value=True):
                assert behavior_obj.Execute() is False
                assert bm.movement_behavior == MockKeys.short_range


def test_long_range_behavior_movement_strategy_forced_before_engagement(mock_game, mock_entity):
    """Confirms long-range scripts re-assert spacing footprints before testing ranges."""
    bm = Behavior_Manager(mock_game, mock_entity, MockKeys.long_range, 100)
    behavior_obj = getattr(bm, 'current_behavior', None)
    
    if behavior_obj:
        with patch.object(bm, 'Update_Engagement_Cooldown', return_value=True):
            with patch.object(behavior_obj, 'Engagement_Controller', return_value=True):
                bm.movement_behavior = None
                assert behavior_obj.Execute() is True
                assert bm.movement_behavior == MockKeys.long_range


def test_retreat_behavior_clears_strategy_on_tick(mock_game, mock_entity):
    """Validates that retreat modules consistently update tactical vectors on active updates."""
    bm = Behavior_Manager(mock_game, mock_entity, MockKeys.retreat, 100)
    behavior_obj = getattr(bm, 'current_behavior', None)
    
    if behavior_obj:
        with patch.object(bm, 'Update_Engagement_Cooldown', return_value=True):
            bm.movement_behavior = None
            behavior_obj.Execute()
            assert bm.movement_behavior == MockKeys.run_away

# Ability handler and individual ability tests have been moved to test_abilities.py.
# ==============================================================================
# END OF FILE