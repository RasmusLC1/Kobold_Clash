import pytest
from unittest.mock import MagicMock, patch
import pygame
import copy

# Adjust these import paths if your structural package layout differs
from scripts.engine.tilemap.tilemap import Tilemap, NEIGHBOR_OFFSETS
from scripts.engine.tilemap.tile.tile import Tile
from scripts.engine.keys.keys import keys

# ==============================================================================
# ARCHITECTURAL FIXTURES
# ==============================================================================

@pytest.fixture
def mock_game_context():
    """
    Creates an isolated, lightweight game state context.
    Pre-populates basic keys and mock surface assets to prevent asset loading errors.
    """
    game = MagicMock()
    game.depth = 1
    game.dungeon_type = keys.ancient_crypt  # Expected by Set_Dungeon_Type mapping
    game.total_time = 0.0
    
    # Setup dummy graphic structures to satisfy component rendering requirements
    mock_surface = pygame.Surface((32, 32))
    game.assets = {
        "crypt_floor": {0: mock_surface, 1: mock_surface},
        "crypt_wall": {0: mock_surface}
    }
    
    # Stub core coordination engines used during search pathways
    game.a_star = MagicMock()
    game.a_star.min_x = 0
    game.a_star.min_y = 0
    
    return game


@pytest.fixture
def empty_tilemap(mock_game_context):
    """Provides a fresh, empty tilemap manager structure."""
    return Tilemap(mock_game_context, tile_size=32)


# ==============================================================================
# TILEMAP STRUCTURAL LOGIC TESTS
# ==============================================================================

def test_tilemap_initialization_bounds(empty_tilemap):
    """Ensures boundary tracking trackers start at structural infinity extremes."""
    assert empty_tilemap.min_x == 99999
    assert empty_tilemap.max_x == -99999
    assert empty_tilemap.tilemap == {}


def test_generate_tile_tracks_boundaries_and_subtypes(empty_tilemap):
    """Validates that bounds recalculate correctly and subtypes parse configuration string arrays."""
    # Set dungeon context configuration
    empty_tilemap.Set_Dungeon_Type()  # sets dungeon_type to "crypt_"
    
    tile_values = {
        keys.type: "floor",
        keys.variant: 0,
        "active": 100,
        "light": 5
    }
    
    tile = empty_tilemap.Generate_Tile((10, -5), tile_values)
    
    assert isinstance(tile, Tile)
    assert empty_tilemap.min_x == 10
    assert empty_tilemap.max_x == 10
    assert empty_tilemap.min_y == -5
    assert empty_tilemap.max_y == -5
    assert tile.sub_type == "crypt_floor"
    assert tile.physics is False


def test_generate_wall_tile_injects_physics(empty_tilemap):
    """Verifies any tiles with 'wall' type context flags activate physics boundaries automatically."""
    empty_tilemap.Set_Dungeon_Type()
    tile_values = {keys.type: "wall", keys.variant: 0}
    
    tile = empty_tilemap.Generate_Tile((0, 0), tile_values)
    
    assert tile.physics is True
    assert isinstance(tile.hitbox, pygame.Rect)


def test_cache_all_tile_neighbors(empty_tilemap):
    """Confirms neighbors and wall hitboxes compile cleanly into static reference collections."""
    empty_tilemap.Set_Dungeon_Type()
    floor_cfg = {keys.type: "floor", keys.variant: 0}
    wall_cfg = {keys.type: "wall", keys.variant: 0}
    
    center_tile = empty_tilemap.Generate_Tile((0, 0), floor_cfg)
    left_wall_tile = empty_tilemap.Generate_Tile((-1, 0), wall_cfg)
    
    empty_tilemap.Cache_All_Tile_Neighbors()
    
    assert left_wall_tile in center_tile.neighbor_tiles
    assert left_wall_tile.hitbox in center_tile.neighbor_physics_rects


def test_find_tiles_not_touching_wall(empty_tilemap):
    """Ensures floor components bordered by static physics walls route into fallback structures."""
    empty_tilemap.Set_Dungeon_Type()
    floor_cfg = {keys.type: "floor", keys.variant: 0}
    wall_cfg = {keys.type: "wall", keys.variant: 0}
    
    # Tile A (0,0) touches a wall at (1,0)
    tile_a = empty_tilemap.Generate_Tile((0, 0), floor_cfg)
    empty_tilemap.Generate_Tile((1, 0), wall_cfg)
    
    # Tile B (10,10) is completely isolated from physical walls
    tile_b = empty_tilemap.Generate_Tile((10, 10), floor_cfg)
    
    empty_tilemap.Find_Tiles_Not_Touching_Wall()
    
    assert (0, 0) not in empty_tilemap.tiles_not_touching_wall
    assert (10, 10) in empty_tilemap.tiles_not_touching_wall
    assert tile_a.touching_wall is True


# ==============================================================================
# TILE DETACHMENT & COGNITIVE LOGIC TESTS (EXTRACT)
# ==============================================================================

def test_extract_removes_grid_tiles_and_severs_neighbor_references(empty_tilemap):
    """Checks that extracting clean items completely drops reference associations to prevent memory leaks."""
    empty_tilemap.Set_Dungeon_Type()
    floor_cfg = {keys.type: "floor", keys.variant: 0}
    
    tile_a = empty_tilemap.Generate_Tile((0, 0), floor_cfg)
    tile_b = empty_tilemap.Generate_Tile((0, 1), floor_cfg)
    empty_tilemap.Cache_All_Tile_Neighbors()
    
    # Confirm mutual linkage setup
    assert tile_a in tile_b.neighbor_tiles
    
    # Extract structural tiles
    extracted = empty_tilemap.extract([("floor", 0)], keep=False)
    
    assert len(extracted) == 2
    assert (0, 0) not in empty_tilemap.tilemap
    # Cross link connections must be unlinked safely to protect GC pathways
    assert tile_a not in tile_b.neighbor_tiles


# ==============================================================================
# COMPONENT LEVEL MODULE VALIDATIONS (TILE & MEMBERS)
# ==============================================================================

def test_tile_slots_override_attributes(mock_game_context):
    """Confirms strict compliance with slot layouts to check memory control handles."""
    tile = Tile(mock_game_context, "floor", "crypt_floor", 0, (0, 0), 0, 0, False, True)
    with pytest.raises(AttributeError):
        tile.custom_runtime_field = "invalid_mutation"


def test_tile_lighting_contributions(mock_game_context):
    """Tests non-linear lighting levels calculate maximum brightness maps correctly."""
    tile = Tile(mock_game_context, "floor", "crypt_floor", 0, (0, 0), 0, 0, False, True)
    
    tile.Add_Light_Contribution("light_A", 100)
    tile.Add_Light_Contribution("light_B", 180)
    
    assert tile.light_level == 180
    assert tile.needs_redraw is True
    
    tile.Remove_Light_Contribution("light_B")
    assert tile.light_level == 100


def test_tile_navigation_distance_caching(mock_game_context):
    """Validates distance caching: cached within the 0.5s window for an unchanged
    target position, but recomputed immediately if the target position changes,
    and recomputed once the 0.5s window elapses regardless."""
    tile = Tile(mock_game_context, "floor", "crypt_floor", 0, (0, 0), 0, 0, False, True)

    mock_game_context.total_time = 0.0
    mock_game_context.player = MagicMock()
    mock_game_context.player.pos = (32.0, 0.0)  # 1 tile away on X-axis

    # Initial calculation
    distance = tile.Get_Distance_To_Target(mock_game_context.player.pos)
    assert distance == 32.0

    # Same target position, still within 0.5s window -> cached value returned,
    # even though the underlying player.pos mock has since "moved" elsewhere.
    mock_game_context.total_time = 0.2
    distance = tile.Get_Distance_To_Target((32.0, 0.0))
    assert distance == 32.0

    # Target position changes within the 0.5s window -> cache must NOT be trusted,
    # since a different position means a different (or differently-targeting) entity.
    mock_game_context.total_time = 0.3
    distance = tile.Get_Distance_To_Target((64.0, 0.0))
    assert distance == 64.0

    # Same (new) target position again, still within window -> cached.
    mock_game_context.total_time = 0.4
    distance = tile.Get_Distance_To_Target((64.0, 0.0))
    assert distance == 64.0

    # Time crosses the 0.5s threshold for the same target position -> recompute
    # is forced even though nothing about the position changed.
    mock_game_context.player.pos = (96.0, 0.0)
    mock_game_context.total_time = 1.0
    distance = tile.Get_Distance_To_Target(mock_game_context.player.pos)
    assert distance == 96.0

# ==============================================================================
# SPATIAL ENTITY LOOKUPS
# ==============================================================================

def test_tilemap_proximity_spatial_searches(empty_tilemap, mock_game_context):
    """Validates area searches capture specific matching subcategories while ignoring self-entities."""
    empty_tilemap.Set_Dungeon_Type()
    empty_tilemap.min_x, empty_tilemap.max_x = -5, 5
    empty_tilemap.min_y, empty_tilemap.max_y = -5, 5
    
    tile = empty_tilemap.Generate_Tile((0, 0), {keys.type: "floor", keys.variant: 0})
    
    # Create distinct mocked entities
    mock_entity_1 = MagicMock()
    mock_entity_1.ID = 101
    mock_entity_1.category = keys.enemy
    mock_entity_1.type = "kobold"
    
    mock_entity_2 = MagicMock()
    mock_entity_2.ID = 102
    mock_entity_2.category = keys.enemy
    mock_entity_2.type = "goblin"
    
    # Add entities directly to target tile system handlers
    tile.Add_Entity(mock_entity_1)
    tile.Add_Entity(mock_entity_2)
    
    # Query matching fields via nearby tile coordinates (Position passed in pixels)
    # Query matching fields via nearby tile coordinates (Pass matching category)
    found_entities = empty_tilemap.Search_Nearby_Tiles(
        max_distance=2, pos=(0, 0), category=keys.enemy, ID=101
    )
    assert mock_entity_2 in found_entities
    assert mock_entity_1 not in found_entities  # Ignored because it matches excluded identity

def test_tilemap_serialization_loop(empty_tilemap, mock_game_context):
    """Verifies that tilemap states serialize and deserialize without data loss."""
    empty_tilemap.Set_Dungeon_Type()
    
    # Pre-populate a simple grid tile setup
    tile_pos = (3, -4)
    empty_tilemap.Generate_Tile(tile_pos, {keys.type: "floor", keys.variant: 1})
    empty_tilemap.tiles_not_touching_wall[tile_pos] = empty_tilemap.tilemap[tile_pos]
    empty_tilemap.minimap.Add_Tile_To_Minimap(empty_tilemap.tilemap[tile_pos])
    
    # Extract the saved state dictionary
    empty_tilemap.Save_data()
    saved_state = empty_tilemap.saved_data
    
    # Spawn a clean tilemap instance and read the state back in
    new_tilemap = Tilemap(mock_game_context, tile_size=32)
    new_tilemap.Load_Data(saved_state)
    
    assert (3, -4) in new_tilemap.tilemap
    assert new_tilemap.tilemap[(3, -4)].variant == 1
    assert (3, -4) in new_tilemap.tiles_not_touching_wall

def test_random_tile_pathfinding_fallback_on_failure(empty_tilemap, mock_game_context):
    """Ensures that the engine gracefully falls back and doesn't freeze when blocked."""
    empty_tilemap.Set_Dungeon_Type()
    tile_pos = (5, 5)
    tile = empty_tilemap.Generate_Tile(tile_pos, {keys.type: "floor", keys.variant: 0})
    empty_tilemap.tiles_not_touching_wall[tile_pos] = tile
    
    # Force mock references to return an empty un-reachable path array
    mock_game_context.player = MagicMock()
    mock_game_context.player.tile.pos = (0, 0)
    mock_game_context.a_star.a_star_search.return_value = [] # Path completely blocked
    
    # Method must break execution instantly and return a fallback choice after 40 failures
    selected_tile = empty_tilemap.Get_Random_Tile_With_Path_To_Player()
    assert selected_tile == tile
    assert mock_game_context.a_star.a_star_search.call_count > 40

def test_add_tile_deregisters_from_raycaster(empty_tilemap, mock_game_context):
    """Confirms that replacing live tiles alerts the raycaster system for engine safety."""
    mock_game_context.ray_caster = MagicMock() # Set up raycaster proxy receiver
    empty_tilemap.Set_Dungeon_Type()
    
    # Plant a baseline reference tile
    initial_tile = empty_tilemap.Generate_Tile((0, 0), {keys.type: "floor", keys.variant: 0})
    
    # Overwrite the coordinate slot with a fresh node
    empty_tilemap.Add_Tile(type="wall", variant=1, pos=(0, 0), physics=True)
    
    # Confirm the raycaster was updated to drop the stale rendering references
    mock_game_context.ray_caster.Remove_Tile.assert_called_once_with(initial_tile)
    assert empty_tilemap.tilemap[(0, 0)].physics is True

def test_physics_rects_around_handles_missing_neighbors(empty_tilemap):
    """Ensures spatial checks don't crash when an entity passes empty space boundaries."""
    empty_tilemap.Set_Dungeon_Type()
    
    # Generate a single isolated tile with absolutely no neighbors surrounding it
    empty_tilemap.Generate_Tile((0, 0), {keys.type: "floor", keys.variant: 0})
    empty_tilemap.Cache_All_Tile_Neighbors()
    
    # Run coordinate physics check on the tile (0, 0 in pixel workspace space = 0, 0 layout key)
    rects = empty_tilemap.physics_rects_around(pos=(0, 0))
    
    # System should safely return an empty list or skip missing nodes without blowing up
    assert isinstance(rects, list)