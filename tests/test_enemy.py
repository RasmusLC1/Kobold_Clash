import pytest
from unittest.mock import MagicMock, patch, call
from collections import deque
import pygame

from scripts.entities.moving_entities.enemies.enemy_spawner import Enemy_Spawner
from scripts.entities.moving_entities.enemies.enemy_pathfinding_handler import Enemy_Pathfinding_Handler
from scripts.entities.moving_entities.enemies.enemy_handler import Enemy_Handler
from scripts.engine.keys.keys import keys

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
    game.dungeon_type = keys.ancient_crypt
    game.entities_render = MagicMock()
    return game


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
    handler.patrol_queue.append(mock_enemy)  # Seed inside fallback queue
    
    handler.Add_To_Pathfinding_Queue(mock_enemy, destination=(500, 500))
    
    assert mock_enemy in handler.pathfinding_queue
    assert mock_enemy not in handler.patrol_queue  # Cleared out cleanly
    mock_enemy.Set_Target.assert_called_once_with((500, 500))
    mock_enemy.Set_Locked_On_Target.assert_called_once_with(30)


def test_update_pathfinding_queue_pops_and_evaluates_if_cooldown_clear(mock_game, mock_enemy):
    handler = Enemy_Pathfinding_Handler(mock_game)
    handler.pathfinding_queue_cooldown = 0.0
    handler.pathfinding_queue.append(mock_enemy)
    
    # Register enemy as alive inside the active framework registry
    mock_game.enemy_handler.enemies = [mock_enemy]
    
    handler.Update_Pathfinding_Queue(delta_time=0.016)
    
    assert len(handler.pathfinding_queue) == 0
    mock_enemy.Find_New_Path.assert_called_once()
    assert handler.pathfinding_queue_cooldown == 0.5  # Throttling engaged


def test_sort_pathfinding_queue_by_player_distance(mock_game):
    handler = Enemy_Pathfinding_Handler(mock_game)
    mock_game.player.pos = [0.0, 0.0]
    
    far_enemy = MagicMock()
    far_enemy.pos = [100.0, 100.0]  # Distance ~141
    
    near_enemy = MagicMock()
    near_enemy.pos = [10.0, 0.0]    # Distance 10
    
    # Append out of order
    handler.pathfinding_queue.append(far_enemy)
    handler.pathfinding_queue.append(near_enemy)
    
    handler.Sort_Pathfinding_Queue()
    
    # Nearest actor should have escalated to head of processing queue
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
    # Flood registry with mock elements to break threshold limits (> 50)
    handler.enemies = [MagicMock() for _ in range(51)]
    
    result = handler.Enemy_Spawner(pos=(100, 100), type="kobold")
    assert result is True  # Early abort conditional return


def test_enemy_spawner_truncates_generation_variants(mock_game, mock_enemy):
    handler = Enemy_Handler(mock_game)
    mock_spawner = MagicMock()
    handler.enemy_spawner = mock_spawner
    
    # Stub instantiation function callback 
    mock_spawn_fn = MagicMock(return_value=mock_enemy)
    mock_spawner.Get_Spawn_Function.return_value = mock_spawn_fn
    
    # Passing variant instance 'kobold_warrior_3'
    handler.Enemy_Spawner(pos=(20, 20), type="kobold_warrior_3")
    
    # Spawner check must truncate variant digit suffix to identify structural base layout mapping
    mock_spawner.Get_Spawn_Function.assert_called_once_with("kobold_warrior")
    assert mock_enemy in handler.enemies


def test_delete_enemy_safely_detaches_references(mock_game, mock_enemy):
    handler = Enemy_Handler(mock_game)
    handler.enemies.append(mock_enemy)
    handler.pathfinding_handler.pathfinding_queue.append(mock_enemy)
    handler.pathfinding_handler.patrol_queue.append(mock_enemy)
    
    handler.Delete_Enemy(mock_enemy)
    
    mock_game.entities_render.Remove_Entity.assert_called_once_with(mock_enemy)
    assert mock_enemy not in handler.enemies
    assert mock_enemy not in handler.pathfinding_handler.pathfinding_queue
    assert mock_enemy not in handler.pathfinding_handler.patrol_queue


def test_find_nearby_enemies_long_distance_filtering(mock_game, mock_enemy):
    handler = Enemy_Handler(mock_game)
    
    searching_entity = MagicMock()
    searching_entity.ID = "player_hero"
    searching_entity.pos = [0.0, 0.0]
    
    in_range = MagicMock()
    in_range.ID = "enemy_near"
    in_range.pos = [30.0, 40.0]  # Distance = 50
    
    out_of_range = MagicMock()
    out_of_range.ID = "enemy_far"
    out_of_range.pos = [100.0, 100.0]  # Distance = ~141
    
    handler.enemies = [in_range, out_of_range]
    
    # Search within radius of 60
    found = handler.Find_Nearby_Enemies_Long_Distance(searching_entity, max_distance=60)
    
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
    """Ensures elements already in the pathfinding queue aren't double-allocated on hot ticks."""
    handler = Enemy_Pathfinding_Handler(mock_game)
    handler.pathfinding_queue.append(mock_enemy)
    
    # Attempting to re-add the same entity should trigger an early exit guard clause
    handler.Add_To_Pathfinding_Queue(mock_enemy, destination=(200, 200))
    
    assert len(handler.pathfinding_queue) == 1
    assert mock_enemy.Set_Target.call_count == 0


def test_update_pathfinding_queue_drops_dead_or_deleted_enemies(mock_game, mock_enemy):
    """Verifies that the processing queue automatically purges dead or unindexed enemies."""
    handler = Enemy_Pathfinding_Handler(mock_game)
    handler.pathfinding_queue_cooldown = 0.0
    handler.pathfinding_queue.append(mock_enemy)
    
    # SCENARIO A: Enemy is alive but missing from the active handler's registry list
    mock_game.enemy_handler.enemies = [] 
    handler.Update_Pathfinding_Queue(delta_time=0.016)
    assert len(handler.pathfinding_queue) == 0
    mock_enemy.Find_New_Path.assert_not_called()
    
    # SCENARIO B: Enemy is in the registry list but its health has dropped to 0
    handler.pathfinding_queue.append(mock_enemy)
    mock_game.enemy_handler.enemies = [mock_enemy]
    mock_enemy.health = 0
    
    handler.Update_Pathfinding_Queue(delta_time=0.016)
    assert len(handler.pathfinding_queue) == 0
    mock_enemy.Find_New_Path.assert_not_called()


def test_initialise_aborts_gracefully_on_empty_spawner_layouts(mock_game):
    """Confirms that maps without explicit spawner pads do not crash the initialization routine."""
    handler = Enemy_Handler(mock_game)
    
    # Force the extraction array map layer to return 0 elements
    mock_game.tilemap.extract.return_value = []
    
    with patch.object(handler, 'Set_Spawner_Type') as mock_set_spawner:
        # Running initialization should return early through its guard clause safely
        handler.Initialise()
        mock_set_spawner.assert_called_once()
        assert len(handler.enemies) == 0


def test_enemy_spawner_handles_missing_digit_variants_gracefully(mock_game, mock_enemy):
    """Ensures type string normalization works cleanly even if strings lack underscores or trailing IDs."""
    handler = Enemy_Handler(mock_game)
    mock_spawner = MagicMock()
    handler.enemy_spawner = mock_spawner
    
    mock_spawn_fn = MagicMock(return_value=mock_enemy)
    mock_spawner.Get_Spawn_Function.return_value = mock_spawn_fn
    
    # Pass a flat type key that does not contain numerical variant suffixes
    handler.Enemy_Spawner(pos=(0, 0), type="skeleton")
    
    # The normalization logic should cleanly handle split loops without stripping text strings
    mock_spawner.Get_Spawn_Function.assert_called_once_with("skeleton")


def test_find_nearby_enemies_redirects_short_distances_to_tilemap(mock_game, mock_enemy):
    """Confirms short-range proximity queries optimize tracking via spatial grid matrix hooks."""
    handler = Enemy_Handler(mock_game)
    
    searching_entity = MagicMock()
    searching_entity.pos = [50.0, 50.0]
    searching_entity.ID = "source_id"
    
    handler.Find_Nearby_Enemies(searching_entity, max_distance=8)
    
    # Distance <= 10 must bypass local list loops and hand off straight to the tilemap spatial cache
    mock_game.tilemap.Search_Nearby_Tiles.assert_called_once_with(
        8, searching_entity.pos, keys.enemy, searching_entity.ID
    )


def test_find_nearby_enemies_long_distance_ignores_self(mock_game, mock_enemy):
    """Verifies that spatial proximity scans do not register the calling entity as its own target match."""
    handler = Enemy_Handler(mock_game)
    
    searching_entity = MagicMock()
    searching_entity.ID = "enemy_123"  # Same ID as mock_enemy
    searching_entity.pos = [150.0, 150.0]
    
    handler.enemies = [mock_enemy]
    
    found = handler.Find_Nearby_Enemies_Long_Distance(searching_entity, max_distance=100)
    
    # Even though position matches perfectly, matching ID must filter it out
    assert len(found) == 0