import pytest
from unittest.mock import MagicMock, patch
import pygame
from collections import deque

# Adjust imports to point to your actual engine directory structure
from scripts.entities.entity.entities import PhysicsEntity
from scripts.entities.entity.tile_handler import Tile_Handler
from scripts.engine.keys.keys import keys

@pytest.fixture(scope="session", autouse=True)
def headless_pygame_context():
    """Initializes a headless video environment to support test-driven Surface manipulation."""
    import os
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()

@pytest.fixture(autouse=True)
def reset_entity_id_counters():
    """Resets class-level tracking states between isolated tests to guarantee predictable IDs."""
    PhysicsEntity._id_counter = 0
    PhysicsEntity._available_IDs = deque()
    yield

@pytest.fixture
def mock_game():
    """Generates a complete mock game context with pre-wired Tilemap dependencies."""
    game = MagicMock()
    game.tilemap.tile_size = 32
    
    # Setup mock tile nodes
    mock_tile = MagicMock()
    mock_tile.pos = (0, 0)
    mock_tile.light_level = 5
    mock_tile.scaled_pos = (0, 0)
    
    game.tilemap.Current_Tile.return_value = mock_tile
    game.tilemap.Get_Random_Tile_With_Path_To_Player.return_value = mock_tile
    return game



### 1. Identity Lifecycle & Recycling Tests

def test_entity_id_generation_and_recycling(mock_game):
    """Verifies incremental allocation and proper stack recycling of entity IDs via Delete()."""
    entity_a = PhysicsEntity(mock_game, "kobold", "monster", (0, 0), (32, 32))
    entity_b = PhysicsEntity(mock_game, "goblin", "monster", (32, 0), (32, 32))
    
    assert entity_a.ID == 0
    assert entity_b.ID == 1
    
    # Delete first entity to queue its ID for reclamation
    entity_a.Delete()
    assert 0 in PhysicsEntity._available_IDs
    
    # Next instantiation should pull from recycled pool rather than incrementing counter
    entity_c = PhysicsEntity(mock_game, "spider", "monster", (64, 0), (32, 32))
    assert entity_c.ID == 0



### 2. Component Logic and Spatial Registration Tests

def test_tile_handler_registration_on_init(mock_game):
    """Ensures initialization successfully executes components to bind spatial map links."""
    mock_tile = MagicMock()
    mock_tile.pos = (1, 2)
    mock_game.tilemap.Current_Tile.return_value = mock_tile

    # Positioning at coordinates (32, 64) over a 32px grid matches key index (1, 2)
    entity = PhysicsEntity(mock_game, "kobold", "monster", (32, 64), (32, 32))
    
    mock_game.tilemap.Current_Tile.assert_called_with((1, 2))
    assert entity.tile == mock_tile
    mock_game.tilemap.Add_Entity_To_Tile.assert_called_with(mock_tile, entity)

def test_tile_handler_crosses_boundaries(mock_game):
    """Validates that modifying entity positions re-allocates active tiles across update steps."""
    tile_start = MagicMock(pos=(0, 0))
    tile_destination = MagicMock(pos=(1, 0))
    
    # Orchestrate safe multi-stage tile handoffs
    mock_game.tilemap.Current_Tile.side_effect = [tile_start, tile_destination]
    
    entity = PhysicsEntity(mock_game, "kobold", "monster", (0, 0), (32, 32))
    assert entity.tile == tile_start
    
    # Walk right into adjacent tile coordinate workspace boundaries
    entity.pos = pygame.Vector2(32, 0)
    
    # Trigger spatial refresh block (Must bypass initial cooldown delay)
    has_changed = entity.Update_Tile(delta_time=0.2)
    
    assert has_changed is True
    assert entity.tile == tile_destination
    tile_start.Remove_Entity.assert_called_once_with(entity.ID)



### 3. State Management & Light Calculation Tests

def test_light_level_clamping(mock_game):
    """Guarantees illumination thresholds clamp perfectly within array bounds."""
    entity = PhysicsEntity(mock_game, "kobold", "monster", (0, 0), (32, 32))
    
    # Test maximum values clamp to byte max limit (255)
    entity.Set_Light_Level(500)
    assert entity.light_level == 255
    assert entity.render_needs_update is True
    
    # Test minimal bounds fallback to structural minimums
    entity.Set_Light_Level(10)
    assert entity.light_level == entity.min_light_level

def test_light_level_interpolation_steps(mock_game):
    """Checks that entity lighting interpolates incrementally toward ambient tile values."""
    mock_tile = MagicMock()
    mock_tile.light_level = 2 # Target light = 2 * LIGHT_ALPHA_SCALE (30) = 60
    mock_game.tilemap.Current_Tile.return_value = mock_tile
    
    entity = PhysicsEntity(mock_game, "kobold", "monster", (0, 0), (32, 32))
    entity.light_level = 40 # Set default flat floor baseline
    
    # Execute single tick of lighting updates
    entity.Update_Light_Level()
    assert entity.light_level == 45
    assert entity.render_needs_update is True



### 4. Serialization Integrity Tests

def test_entity_serialization_loop(mock_game):
    """Ensures structural metrics store and restore cleanly across save/load state routines."""
    entity = PhysicsEntity(mock_game, "kobold", "monster", (10, 20), (16, 24))
    entity.ID = 77
    entity.light_level = 120
    entity.active = 50
    
    serialized_dump = entity.Save_Data()
    
    # Spawn completely un-configured object frame
    blank_entity = PhysicsEntity(mock_game, "placeholder", "temp", (0, 0), (32, 32))
    blank_entity.Load_Data(serialized_dump)
    
    assert blank_entity.ID == 77
    assert blank_entity.category == "monster"
    assert blank_entity.type == "kobold"
    assert blank_entity.pos == pygame.Vector2(10, 20)
    assert blank_entity.size == [16, 24]
    assert blank_entity.active == 50
    assert blank_entity.light_level == 120
    
    # Ensure ID allocation updates system counters safely to avoid overlapping IDs
    assert PhysicsEntity._id_counter == 78