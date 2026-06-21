# tests/test_initialization.py
import pytest
from scripts.game.game_initialiser import Game_Initialiser

class SkeletonGame:
    """A barebones representation of your main Game class 
    to hold state dynamically during an integration test.
    """
    def __init__(self):
        self.state_machine = None

def test_game_initialiser_attaches_engine_components():
    game = SkeletonGame()
    initialiser = Game_Initialiser(game)
    
    # Run the initialization sequence
    initialiser.Initialise_Game()
    
    # Assert that all your core engines were successfully bound to the game instance
    assert game.render_scale == 2
    assert game.screen_width == 1500
    assert game.mouse is not None
    assert game.ray_caster is not None
    assert game.tilemap is not None
    assert game.dungeon_generator is not None