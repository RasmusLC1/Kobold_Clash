import pytest
from unittest.mock import MagicMock
from scripts.engine.lights.light_handler import Light_Handler
from scripts.engine.lights.lights import Light

@pytest.fixture
def mock_game():
    game = MagicMock()
    # Mocking the tilemap structure expected by Light
    game.tilemap.tile_size = 32
    game.tilemap.Current_Tile = MagicMock()
    return game

@pytest.fixture
def mock_tile():
    tile = MagicMock()
    tile.translucent = True
    tile.light_level = 0
    return tile

def test_light_creation_adds_contribution(mock_game, mock_tile):
    """Ensure a new light automatically registers its contribution to a tile."""
    # Setup the current tile returned by the game
    mock_game.tilemap.Current_Tile.return_value = mock_tile
    
    light = Light(mock_game, (32, 32), 100, mock_tile)
    
    # Verify the tile's lighting component was updated
    mock_tile.Add_Light_Contribution.assert_called()
    assert len(light.tiles) > 0

def test_light_handler_adds_and_removes(mock_game):
    handler = Light_Handler(mock_game)
    
    # Create a proper mock for the tile
    tile = MagicMock()
    # Explicitly configure light_level as an integer
    tile.light_level = 0 
    tile.translucent = True
    
    # Ensure the game's map returns our configured tile
    mock_game.tilemap.Current_Tile.return_value = tile
    
    # Now this will work because tile.light_level is an integer 0
    light = handler.Add_Light((0, 0), 50, tile)
    
    assert light in handler.lights
    handler.Remove_Light(light)
    assert light not in handler.lights

def test_light_deletion_clears_tile_contributions(mock_game, mock_tile):
    """Ensure that deleting a light removes its contribution from all affected tiles."""
    mock_game.tilemap.Current_Tile.return_value = mock_tile
    
    light = Light(mock_game, (32, 32), 100, mock_tile)
    light.Delete_Light()
    
    # Verify the tile was told to remove this specific light ID
    mock_tile.Remove_Light_Contribution.assert_called_with(light.id)

def test_light_initialization_levels(mock_game):
    handler = Light_Handler(mock_game)
    # Test lower bound clamping
    assert handler.Initialise_Light_Level(None) == 50
    
    # Mock a tile with low light
    tile = MagicMock()
    tile.light_level = 1
    assert handler.Initialise_Light_Level(tile) == 50
    
    # Mock a tile with high light
    tile.light_level = 20
    assert handler.Initialise_Light_Level(tile) == 255