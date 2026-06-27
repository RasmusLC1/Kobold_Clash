import pytest
from unittest.mock import MagicMock, call
from scripts.engine.lights.light_handler import Light_Handler
from scripts.engine.lights.lights import Light


@pytest.fixture
def mock_game():
    game = MagicMock()
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
    mock_game.tilemap.Current_Tile.return_value = mock_tile
    light = Light(mock_game, (32, 32), 10, mock_tile)
    mock_tile.Add_Light_Contribution.assert_called()
    assert len(light.tiles) > 0


def test_light_handler_adds_and_removes(mock_game):
    handler = Light_Handler(mock_game)
    tile = MagicMock()
    tile.light_level = 0
    tile.translucent = True
    mock_game.tilemap.Current_Tile.return_value = tile
    light = handler.Add_Light((0, 0), 5, tile)
    assert light in handler.lights
    handler.Remove_Light(light)
    assert light not in handler.lights


def test_light_deletion_clears_tile_contributions(mock_game, mock_tile):
    mock_game.tilemap.Current_Tile.return_value = mock_tile
    light = Light(mock_game, (32, 32), 5, mock_tile)
    light.Delete_Light()
    mock_tile.Remove_Light_Contribution.assert_called_with(light.id)


def test_light_initialization_levels(mock_game):
    handler = Light_Handler(mock_game)
    assert handler.Initialise_Light_Level(None) == 50
    tile = MagicMock()
    tile.light_level = 1
    assert handler.Initialise_Light_Level(tile) == 50
    tile.light_level = 20
    assert handler.Initialise_Light_Level(tile) == 255


def test_light_does_not_penetrate_solid_tile(mock_game, mock_tile):
    """Light should stop at a solid (non-translucent) tile and not illuminate beyond it."""
    solid_tile = MagicMock()
    solid_tile.translucent = False
    solid_tile.light_level = 0

    # First tile is solid — light should stop immediately
    mock_game.tilemap.Current_Tile.return_value = solid_tile

    light = Light(mock_game, (32, 32), 5, mock_tile)

    # Solid tile should never receive a light contribution
    solid_tile.Add_Light_Contribution.assert_not_called()


def test_light_does_not_illuminate_lower_level_tiles(mock_game):
    """A tile already brighter than the incoming light should not be updated."""
    bright_tile = MagicMock()
    bright_tile.translucent = True
    bright_tile.light_level = 999  # Already very bright

    mock_game.tilemap.Current_Tile.return_value = bright_tile

    light = Light(mock_game, (32, 32), 5, bright_tile)

    # The tile is already brighter so Add_Light_Contribution should not be called on it
    bright_tile.Add_Light_Contribution.assert_not_called()


def test_light_delete_is_idempotent(mock_game, mock_tile):
    """Calling Delete_Light twice should not raise and should return False on second call."""
    mock_game.tilemap.Current_Tile.return_value = mock_tile
    light = Light(mock_game, (32, 32), 5, mock_tile)
    light.Delete_Light()
    result = light.Delete_Light()
    assert result is False


def test_light_tiles_cleared_after_deletion(mock_game, mock_tile):
    """After deletion, the light's tile list should be empty."""
    mock_game.tilemap.Current_Tile.return_value = mock_tile
    light = Light(mock_game, (32, 32), 5, mock_tile)
    light.Delete_Light()
    assert light.tiles == []


def test_move_light_resets_old_contributions(mock_game, mock_tile):
    """Moving a light should remove contributions from old tiles and apply new ones."""
    mock_game.tilemap.Current_Tile.return_value = mock_tile
    light = Light(mock_game, (32, 32), 5, mock_tile)

    new_tile = MagicMock()
    new_tile.translucent = True
    new_tile.light_level = 0
    mock_game.tilemap.Current_Tile.return_value = new_tile

    light.Move_Light((64, 64), new_tile)

    # Old tile contributions should have been removed
    mock_tile.Remove_Light_Contribution.assert_called_with(light.id)


def test_update_light_level_changes_illumination(mock_game, mock_tile):
    """Updating the light level should re-run Setup_Tile_Light with the new level."""
    mock_game.tilemap.Current_Tile.return_value = mock_tile
    light = Light(mock_game, (32, 32), 5, mock_tile)

    initial_call_count = mock_tile.Add_Light_Contribution.call_count
    light.Update_Light_Level(10)

    # Should have made additional contribution calls for the new, stronger level
    assert mock_tile.Add_Light_Contribution.call_count > initial_call_count


def test_light_handler_clear_removes_all_lights(mock_game, mock_tile):
    """Clear_Lights should remove all lights and clean up contributions."""
    mock_game.tilemap.Current_Tile.return_value = mock_tile
    handler = Light_Handler(mock_game)
    handler.Add_Light((0, 0), 5, mock_tile)
    handler.Add_Light((32, 32), 5, mock_tile)

    assert len(handler.lights) == 2
    handler.Clear_Lights()
    assert len(handler.lights) == 0


def test_each_light_has_unique_id(mock_game, mock_tile):
    """Each Light instance should have a unique ID."""
    mock_game.tilemap.Current_Tile.return_value = mock_tile
    light_a = Light(mock_game, (32, 32), 5, mock_tile)
    light_b = Light(mock_game, (64, 64), 5, mock_tile)
    assert light_a.id != light_b.id