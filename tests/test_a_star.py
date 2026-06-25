# tests/test_a_star.py
import pytest
from unittest.mock import MagicMock
from scripts.engine.a_star import A_Star

# Constants matching your map identifiers
FLOOR, WALL = 0, 1

@pytest.fixture
def clean_astar(mock_game):
    """Provides a fresh instance of A_Star for pathing checks."""
    return A_Star(mock_game)

def test_astar_straight_line_path(clean_astar):
    """Tests a simple path with no obstacles from (0,0) to (4,0)."""
    # Create a small 5x5 grid layout of open floors
    custom_grid = [[FLOOR for _ in range(5)] for _ in range(5)]
    clean_astar.Setup_Custom_Map(custom_grid, size_x=5, size_y=5)
    clean_astar.Set_Map('custom')
    
    start = (0, 0)
    goal = (4, 0)
    path = clean_astar.a_star_search(start, goal, which_map='custom')
    
    # It should find a clear straight path directly to the target
    assert len(path) > 0
    assert path[0] == start
    assert path[-1] == goal
    assert (1, 0) in path

def test_astar_blocked_by_wall(clean_astar):
    """Tests that pathfinding routes around a wall or returns empty if blocked."""
    # Build a 3x3 grid with a solid wall across column 1
    # [Floor, Wall, Floor]
    # [Floor, Wall, Floor]
    # [Floor, Wall, Floor]
    custom_grid = [
        [FLOOR, FLOOR, FLOOR],
        [WALL,  WALL,  WALL],
        [FLOOR, FLOOR, FLOOR]
    ]
    clean_astar.Setup_Custom_Map(custom_grid, size_x=3, size_y=3)
    clean_astar.Set_Map('custom')
    
    # Try to cross from left side of wall to right side
    path = clean_astar.a_star_search((0, 0), (2, 0), which_map='custom')
    
    # No open spaces exist past column 1, should fail cleanly returning an empty list
    assert path == []

def test_astar_no_diagonals_cost(clean_astar):
    """Ensures 4-directional pathing uses orthogonal movements only."""
    custom_grid = [[FLOOR for _ in range(3)] for _ in range(3)]
    clean_astar.Setup_Custom_Map(custom_grid, size_x=3, size_y=3)
    
    start = (0, 0)
    goal = (1, 1)
    
    path = clean_astar.a_star_search_no_diagonals(start, goal, which_map='custom')
    
    # To get to (1,1) without diagonals, it must step to either (1,0) or (0,1) first
    assert len(path) == 3  # (0,0) -> (1,0) -> (1,1)
    assert path[1] in [(1, 0), (0, 1)]