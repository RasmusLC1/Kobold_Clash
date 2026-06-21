# tests/conftest.py
import pytest
import pygame
from unittest.mock import MagicMock

# Force Pygame to run headless (no window, no sound drivers needed)
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

@pytest.fixture(scope="session", autouse=True)
def init_pygame():
    """Initializes Pygame once for the entire test session."""
    pygame.init()
    pygame.display.set_mode((1, 1)) # Smallest possible dummy surface
    yield
    pygame.quit()

@pytest.fixture
def mock_game():
    """Provides a completely fake game instance with mocked attributes.
    Perfect for unit testing isolated components.
    """
    game = MagicMock()
    game.screen_width = 1500
    game.screen_height = 1000
    game.render_scale = 2
    game.display = pygame.Surface((750, 500))
    game.scroll = [0, 0]
    game.render_scroll = (0, 0)
    game.assets = {'background': pygame.Surface((10, 10))}
    return game