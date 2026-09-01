import pytest
import pygame
from unittest.mock import MagicMock, patch, call

from scripts.entities.moving_entities.enemies.enemy_spawner import Enemy_Spawner
from scripts.entities.moving_entities.enemies.enemy_pathfinding_handler import Enemy_Pathfinding_Handler
from scripts.entities.moving_entities.enemies.enemy_handler import Enemy_Handler
from scripts.engine.keys.keys import keys
from scripts.entities.moving_entities.enemies.behavior.abilities.ability_handler import Ability_Handler
from scripts.entities.moving_entities.enemies.behavior.abilities.distance_functions import DISTANCE_REGISTRY

# ---------------------------------------------------------------------------
# WHY THIS IMPORT BLOCK EXISTS
# ---------------------------------------------------------------------------
# The @register_ability decorator only fires when Python actually executes the
# ability module.  ability_handler.py imports the registry *dict*, but nothing
# in the production path forces the individual ability files to be imported,
# so ABILITY_REGISTRY stays empty at test time and Create_New_Ability silently
# returns None.  Importing every concrete ability here guarantees the decorator
# runs before any test tries to resolve a key from the registry.
# ---------------------------------------------------------------------------
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.crystal_scale import Crystal_Scale          # noqa: F401
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.gloom_stalker import Gloom_Stalker          # noqa: F401
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.explode_on_impact import Explode_On_Impact  # noqa: F401


# ==============================================================================
# REGISTRY SMOKE TEST — catches the "empty dict" bug at collection time
# ==============================================================================

def test_ability_registry_is_populated():
    """
    Fails immediately if any ability module forgot to import (and therefore
    its @register_ability decorator never ran).  Add every key you expect to
    be present so a missing import surfaces here rather than as a silent None
    inside Create_New_Ability.
    """
    from scripts.entities.moving_entities.enemies.behavior.abilities import registry
    expected_keys = [
        keys.crystal_scale,
        keys.gloom_stalker,
        keys.explode_on_impact,
    ]
    for key in expected_keys:
        assert key in registry.ABILITY_REGISTRY, (
            f"'{key}' is missing from ABILITY_REGISTRY — "
            f"did you forget to import its module?"
        )


# ==============================================================================
# FIXTURES & MOCKING CONTEXTS
# ==============================================================================

@pytest.fixture
def mock_game():
    """Sets up standard engine sub-system hooks."""
    game = MagicMock()
    game.player = MagicMock()
    game.player.pos = [100.0, 100.0]
    game.tilemap = MagicMock()
    game.tilemap.tile_size = 32         
    game.dungeon_type = keys.ancient_crypt
    game.entities_render = MagicMock()
    return game


@pytest.fixture
def mock_game_and_entity():
    """Sets up a paired mock game and mock entity context for distance strategy tests."""
    game = MagicMock()
    entity = MagicMock()
    entity.distance_to_target = 200
    game.player.velocity = [0.0, 0.0]
    return game, entity


@pytest.fixture
def dummy_base_state():
    state = MagicMock()
    state.health = 100
    state.strength = 10
    state.souls = 5
    return state


@pytest.fixture
def mock_enemy():
    """Returns a basic mocked enemy with normal state metrics."""
    enemy = MagicMock()
    enemy.ID = "enemy_123"
    enemy.health = 50
    enemy.pos = [150.0, 150.0]
    return enemy


# ==============================================================================
# 1. ENEMY_SPAWNER TESTS
# ==============================================================================

def test_spawner_returns_exact_mapped_spawn_function(mock_game):
    mock_spawn_fn = MagicMock()
    spawn_methods = {"kobold_warrior": mock_spawn_fn}
    spawner = Enemy_Spawner(mock_game, spawn_methods, {"kobold_warrior": 1.0})

    resolved_fn = spawner.Get_Spawn_Function("kobold_warrior")
    assert resolved_fn == mock_spawn_fn


def test_spawner_returns_none_for_unmapped_keys(mock_game):
    spawner = Enemy_Spawner(mock_game, {}, {})
    assert spawner.Get_Spawn_Function("unknown_ghost") is None


# ==============================================================================
# 2. ENEMY_PATHFINDING_HANDLER TESTS
# ==============================================================================

def test_add_to_pathfinding_queue_locks_target_and_swaps_queues(mock_game, mock_enemy):
    handler = Enemy_Pathfinding_Handler(mock_game)
    handler.patrol_queue.append(mock_enemy)

    handler.Add_To_Pathfinding_Queue(mock_enemy, destination=(500, 500))

    assert mock_enemy in handler.pathfinding_queue
    assert mock_enemy not in handler.patrol_queue
    mock_enemy.Set_Target.assert_called_once_with((500, 500))


def test_update_pathfinding_queue_pops_and_evaluates_if_cooldown_clear(mock_game, mock_enemy):
    handler = Enemy_Pathfinding_Handler(mock_game)
    handler.pathfinding_queue_cooldown = 0.0
    handler.pathfinding_queue.append(mock_enemy)

    mock_game.enemy_handler.enemies = [mock_enemy]

    handler.Update_Pathfinding_Queue(delta_time=0.016)

    assert len(handler.pathfinding_queue) == 0
    mock_enemy.Find_New_Path.assert_called_once()
    assert handler.pathfinding_queue_cooldown == 0.5


def test_sort_pathfinding_queue_by_player_distance(mock_game):
    handler = Enemy_Pathfinding_Handler(mock_game)
    mock_game.player.pos = [0.0, 0.0]

    far_enemy = MagicMock()
    far_enemy.pos = [100.0, 100.0]

    near_enemy = MagicMock()
    near_enemy.pos = [10.0, 0.0]

    handler.pathfinding_queue.append(far_enemy)
    handler.pathfinding_queue.append(near_enemy)

    handler.Sort_Pathfinding_Queue()

    assert handler.pathfinding_queue[0] == near_enemy
    assert handler.pathfinding_queue[1] == far_enemy


# ==============================================================================
# 3. ENEMY_HANDLER TESTS
# ==============================================================================

def test_clear_enemies_wipes_all_collections_and_latches(mock_game, mock_enemy):
    handler = Enemy_Handler(mock_game)
    handler.enemies.append(mock_enemy)
    handler.pathfinding_handler.pathfinding_queue.append(mock_enemy)
    handler.should_sort_queue = True

    handler.Clear_Enemies()

    assert len(handler.enemies) == 0
    assert len(handler.pathfinding_handler.pathfinding_queue) == 0
    assert handler.should_sort_queue is False


def test_enemy_spawner_respects_hard_cap_threshold(mock_game):
    handler = Enemy_Handler(mock_game)
    handler.enemies = [MagicMock() for _ in range(51)]

    result = handler.Enemy_Spawner(pos=(100, 100), type="kobold")
    assert result is True


mock_chosen_item = MagicMock()
mock_chosen_item.pos = [0.0, 0.0]


@patch('random.choice', return_value=mock_chosen_item)
@patch('random.randint', return_value=1)
def test_enemy_spawner_truncates_generation_variants(mock_randint, mock_choice, mock_game, mock_enemy, dummy_base_state):
    handler = Enemy_Handler(mock_game)
    mock_spawner = MagicMock()
    handler.enemy_spawner = mock_spawner

    mock_spawn_fn = MagicMock(return_value=mock_enemy)
    mock_spawner.Get_Spawn_Function.return_value = mock_spawn_fn

    mock_stats = {"kobold_warrior": dummy_base_state}
    with patch('scripts.entities.moving_entities.enemies.attribute_distributor.attribute_distributor.ENEMY_STATS', mock_stats):
        handler.Enemy_Spawner(pos=(20, 20), type="kobold_warrior_3")

    mock_spawner.Get_Spawn_Function.assert_called_once_with("kobold_warrior")
    assert mock_enemy in handler.enemies


@patch('random.choice', return_value=mock_chosen_item)
@patch('random.randint', return_value=1)
def test_enemy_spawner_handles_missing_digit_variants_gracefully(mock_randint, mock_choice, mock_game, mock_enemy, dummy_base_state):
    handler = Enemy_Handler(mock_game)
    mock_spawner = MagicMock()
    handler.enemy_spawner = mock_spawner

    mock_spawn_fn = MagicMock(return_value=mock_enemy)
    mock_spawner.Get_Spawn_Function.return_value = mock_spawn_fn

    mock_stats = {"skeleton": dummy_base_state}
    with patch('scripts.entities.moving_entities.enemies.attribute_distributor.attribute_distributor.ENEMY_STATS', mock_stats):
        handler.Enemy_Spawner(pos=(0, 0), type="skeleton")

    mock_spawner.Get_Spawn_Function.assert_called_once_with("skeleton")


def test_find_nearby_enemies_long_distance_filtering(mock_game, mock_enemy):
    handler = Enemy_Handler(mock_game)

    searching_entity = MagicMock()
    searching_entity.ID = "player_hero"
    searching_entity.pos = [0.0, 0.0]

    in_range = MagicMock()
    in_range.ID = "enemy_near"
    in_range.pos = [30.0, 40.0]  # Distance = 50px

    out_of_range = MagicMock()
    out_of_range.ID = "enemy_far"
    out_of_range.pos = [100.0, 100.0]  # Distance = ~141.4px

    handler.enemies = [in_range, out_of_range]

    # max_distance is in tiles; tile_size=32px -> threshold=64px, which sits
    # between the two fixture distances (50px in-range, 141.4px out-of-range)
    found = handler.Find_Nearby_Enemies_Long_Distance(searching_entity, max_distance=2)

    assert in_range in found
    assert out_of_range not in found


def test_update_loop_triggers_deferred_sorting_latch(mock_game):
    handler = Enemy_Handler(mock_game)
    handler.should_sort_queue = True

    with patch.object(handler.pathfinding_handler, 'Sort_Pathfinding_Queue') as mock_sort, \
         patch.object(handler.pathfinding_handler, 'Update') as mock_update:

        handler.Update(delta_time=0.016)

        mock_sort.assert_called_once()
        assert handler.should_sort_queue is False
        mock_update.assert_called_once_with(0.016)


# ==============================================================================
# 4. EDGE CASE & FAULT TOLERANCE TESTS
# ==============================================================================

def test_add_to_pathfinding_queue_deduplicates_existing_requests(mock_game, mock_enemy):
    handler = Enemy_Pathfinding_Handler(mock_game)
    handler.pathfinding_queue.append(mock_enemy)

    handler.Add_To_Pathfinding_Queue(mock_enemy, destination=(200, 200))

    assert len(handler.pathfinding_queue) == 1
    assert mock_enemy.Set_Target.call_count == 0


def test_update_pathfinding_queue_drops_dead_or_deleted_enemies(mock_game, mock_enemy):
    handler = Enemy_Pathfinding_Handler(mock_game)
    handler.pathfinding_queue_cooldown = 0.0
    handler.pathfinding_queue.append(mock_enemy)

    mock_game.enemy_handler.enemies = []
    handler.Update_Pathfinding_Queue(delta_time=0.016)
    assert len(handler.pathfinding_queue) == 0
    mock_enemy.Find_New_Path.assert_not_called()

    handler.pathfinding_queue.append(mock_enemy)
    mock_game.enemy_handler.enemies = [mock_enemy]
    mock_enemy.health = 0

    handler.Update_Pathfinding_Queue(delta_time=0.016)
    assert len(handler.pathfinding_queue) == 0
    mock_enemy.Find_New_Path.assert_not_called()


def test_initialise_aborts_gracefully_on_empty_spawner_layouts(mock_game):
    handler = Enemy_Handler(mock_game)

    mock_game.tilemap.extract.return_value = []

    with patch.object(handler, 'Set_Spawner_Type') as mock_set_spawner:
        handler.Initialise()
        mock_set_spawner.assert_called_once()
        assert len(handler.enemies) == 0


def test_find_nearby_enemies_redirects_short_distances_to_tilemap(mock_game, mock_enemy):
    handler = Enemy_Handler(mock_game)

    searching_entity = MagicMock()
    searching_entity.pos = [50.0, 50.0]
    searching_entity.ID = "source_id"

    handler.Find_Nearby_Enemies(searching_entity, max_distance=8)

    mock_game.tilemap.Search_Nearby_Tiles.assert_called_once_with(
        8, searching_entity.pos, keys.enemy, searching_entity.ID
    )


def test_find_nearby_enemies_long_distance_ignores_self(mock_game, mock_enemy):
    handler = Enemy_Handler(mock_game)

    searching_entity = MagicMock()
    searching_entity.ID = "enemy_123"
    searching_entity.pos = [150.0, 150.0]

    handler.enemies = [mock_enemy]

    found = handler.Find_Nearby_Enemies_Long_Distance(searching_entity, max_distance=100)

    assert len(found) == 0


# ==============================================================================
# 5. DISTANCE STRATEGY TESTS
# ==============================================================================

def test_standard_distance_check_within_range(mock_game_and_entity):
    game, entity = mock_game_and_entity
    handler = Ability_Handler(game, entity)
    assert handler.Check_Player_Distance(max_distance=300, delta_time=0.2) is True


def test_standard_distance_check_out_of_range(mock_game_and_entity):
    game, entity = mock_game_and_entity
    handler = Ability_Handler(game, entity)
    assert handler.Check_Player_Distance(max_distance=150, delta_time=0.2) is False


def test_echo_location_player_perfectly_still(mock_game_and_entity):
    game, entity = mock_game_and_entity
    handler = Ability_Handler(game, entity)
    handler.Set_Player_Distance(keys.echo_location)

    # Must use keyboard_handler — that is what EchoLocationDistanceCheck._Check_Keyboard_Input reads
    game.keyboard_handler.is_key_pressed.return_value = False
    handler.player_distance_strategy.echo_linger_timer = 0.0
    entity.distance_to_target = 200.0

    assert handler.Check_Player_Distance(max_distance=300, delta_time=0.2) is False


def test_echo_location_player_moving(mock_game_and_entity):
    game, entity = mock_game_and_entity
    handler = Ability_Handler(game, entity)
    handler.Set_Player_Distance(keys.echo_location)

    # W key pressed → player is moving
    game.keyboard_handler.is_key_pressed.side_effect = lambda k: k == pygame.K_w
    entity.distance_to_target = 200.0

    assert handler.Check_Player_Distance(max_distance=300, delta_time=0.2) is True


def test_echo_location_player_moving_but_out_of_range(mock_game_and_entity):
    game, entity = mock_game_and_entity
    handler = Ability_Handler(game, entity)
    handler.Set_Player_Distance(keys.echo_location)

    # Player is moving, but physically too far — distance check gates first
    game.keyboard_handler.is_key_pressed.side_effect = lambda k: k in [pygame.K_w, pygame.K_a]
    entity.distance_to_target = 200.0

    assert handler.Check_Player_Distance(max_distance=100, delta_time=0.2) is False


def test_echo_location_player_moving_and_in_range(mock_game_and_entity):
    game, entity = mock_game_and_entity
    handler = Ability_Handler(game, entity)
    handler.Set_Player_Distance(keys.echo_location)

    game.keyboard_handler.is_key_pressed.side_effect = lambda k: k == pygame.K_d
    entity.distance_to_target = 200.0

    assert handler.Check_Player_Distance(max_distance=300, delta_time=0.2) is True


def test_echo_location_linger_timer_keeps_detection_after_player_stops(mock_game_and_entity):
    """
    Player was moving, stops, but the linger window hasn't expired yet.
    The strategy should still return True for the remaining linger duration.
    """
    game, entity = mock_game_and_entity
    handler = Ability_Handler(game, entity)
    handler.Set_Player_Distance(keys.echo_location)

    game.keyboard_handler.is_key_pressed.return_value = False  # Player now still
    handler.player_distance_strategy.echo_linger_timer = 3.0   # But linger window active
    entity.distance_to_target = 200.0

    assert handler.Check_Player_Distance(max_distance=300, delta_time=0.2) is True
    # Timer should have ticked down by delta_time
    assert handler.player_distance_strategy.echo_linger_timer == pytest.approx(2.8)


def test_echo_location_linger_timer_expires_and_loses_detection(mock_game_and_entity):
    """Once the linger window hits zero the entity should lose tracking."""
    game, entity = mock_game_and_entity
    handler = Ability_Handler(game, entity)
    handler.Set_Player_Distance(keys.echo_location)

    game.keyboard_handler.is_key_pressed.return_value = False
    handler.player_distance_strategy.echo_linger_timer = 0.0  # Already expired
    entity.distance_to_target = 200.0

    assert handler.Check_Player_Distance(max_distance=300, delta_time=0.2) is False


def test_fallback_to_standard_on_invalid_key(mock_game_and_entity):
    game, entity = mock_game_and_entity
    handler = Ability_Handler(game, entity)

    handler.Set_Player_Distance("invalid_sensory_key_type")

    assert type(handler.player_distance_strategy) is DISTANCE_REGISTRY[keys.standard]