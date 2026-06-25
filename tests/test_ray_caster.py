# tests/test_ray_caster.py
import pytest
from unittest.mock import MagicMock
from scripts.engine.ray_caster import Ray_Caster

def test_ray_vectors_generation(mock_game):
    """Ensure vectors are initialized cleanly and cover a spread."""
    raycaster = Ray_Caster(mock_game)
    
    # Check that it generated the requested number of line vectors
    assert len(raycaster.ray_vectors) == 100
    
    # The first or last vectors should roughly mirror each other symmetrically
    first_vec = raycaster.ray_vectors[0]
    last_vec = raycaster.ray_vectors[-1]
    assert abs(first_vec[0] - last_vec[0]) < 1e-5  # x coordinates match

def test_process_tile_activity_out_of_range(mock_game):
    """Tiles beyond INACTIVE_DISTANCE should become deactivated."""
    raycaster = Ray_Caster(mock_game)
    
    # Create a mock tile that is far away from the player at (0, 0)
    mock_tile = MagicMock()
    mock_tile.active = 10
    mock_tile.scaled_pos = (2000, 2000)  # Dist squared = 8,000,000 (> 640,000)
    
    player_pos = (0, 0)
    is_active = raycaster._process_tile_activity(mock_tile, player_pos)
    
    assert is_active is False
    assert mock_tile.active == 0