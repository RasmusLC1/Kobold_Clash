# tests/test_pathfinding.py
# Tests for the game-facing layer: map building, tile coordinates, map selection,
# and the Find_Path / flood fill API. The algorithms themselves are tested in
# test_a_star.py and test_flood_fill.py.
import pytest
from unittest.mock import MagicMock

from scripts.engine.keys.keys import keys
from scripts.engine.pathfinding.pathfinding import (
    Pathfinding, GridMap, FLOOR, WALL, LAVA, DOOR, TRAP, BOSS_ROOM,
)


# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────

def open_grid(w, h):
    """All-floor custom map of size w × h (indexed grid[x][y])."""
    return [[FLOOR for _ in range(h)] for _ in range(w)]


def make_mock_tile(type_val, sub_type_val="ancient_tomb_floor",
                   touching_wall=False, trap=None, physics=False):
    """
    Build a tile mock that mirrors what Tilemap.Generate_Tile produces.
    type      → raw key e.g. keys.floor  (what the map rules must check)
    sub_type  → prefixed e.g. "ancient_tomb_floor" (deliberately different from type)
    """
    tile = MagicMock()
    tile.type = type_val
    tile.sub_type = sub_type_val
    tile.touching_wall = touching_wall
    tile.trap = trap
    tile.physics = physics
    return tile


def floor_tile(**kwargs):
    return make_mock_tile(keys.floor, "ancient_tomb_floor", **kwargs)


def wall_tile():
    return make_mock_tile("wall", "ancient_tomb_wall")


def row_of_floor(x_start, x_end, y):
    """Floor tiles at (x_start..x_end, y), inclusive."""
    return {(x, y): floor_tile() for x in range(x_start, x_end + 1)}


def game_with_tiles(tiles_by_pos):
    """A mock game whose tilemap returns a fixed set of tiles."""
    game = MagicMock()
    game.tilemap.Get_Pos.return_value = list(tiles_by_pos)
    game.tilemap.Current_Tile.side_effect = lambda pos: tiles_by_pos.get(pos)
    return game


def build_from_tiles(tiles_by_pos):
    pathfinding = Pathfinding(game_with_tiles(tiles_by_pos))
    pathfinding.Setup_Map_From_Game()
    return pathfinding


def cell(pathfinding, which_map, x=0, y=0):
    return pathfinding.maps[which_map].cells[x][y]


@pytest.fixture
def pathfinding():
    return Pathfinding(MagicMock())


# ─────────────────────────────────────────────
#  1. GridMap coordinate conversion
# ─────────────────────────────────────────────

class TestGridMap:

    def test_default_origin_is_zero(self):
        grid_map = GridMap([[0]])
        assert (grid_map.min_x, grid_map.min_y) == (0, 0)
        assert grid_map.to_local((3, 4)) == (3, 4)

    def test_conversion_round_trip(self):
        grid_map = GridMap([[0]], min_x=10, min_y=5)
        assert grid_map.to_local((12, 7)) == (2, 2)
        assert grid_map.to_tile((2, 2)) == (12, 7)


# ─────────────────────────────────────────────
#  2. Custom-map setup
# ─────────────────────────────────────────────

class TestCustomMapSetup:

    def test_stored_under_the_custom_key_with_its_dimensions(self, pathfinding):
        pathfinding.Setup_Custom_Map(open_grid(6, 4))
        cells = pathfinding.maps[keys.custom].cells
        assert len(cells) == 6
        assert len(cells[0]) == 4

    def test_custom_map_origin_is_zero(self, pathfinding):
        pathfinding.Setup_Custom_Map(open_grid(3, 3))
        grid_map = pathfinding.maps[keys.custom]
        assert (grid_map.min_x, grid_map.min_y) == (0, 0)

    def test_does_not_create_any_other_map(self, pathfinding):
        pathfinding.Setup_Custom_Map(open_grid(3, 3))
        assert set(pathfinding.maps) == {keys.custom}

    def test_floor_cells_are_zero(self, pathfinding):
        pathfinding.Setup_Custom_Map(open_grid(3, 3))
        cells = pathfinding.maps[keys.custom].cells
        assert all(cells[x][y] == 0 for x in range(3) for y in range(3))

    def test_wall_cells_are_one(self, pathfinding):
        pathfinding.Setup_Custom_Map([[WALL] * 3 for _ in range(3)])
        cells = pathfinding.maps[keys.custom].cells
        assert all(cells[x][y] == 1 for x in range(3) for y in range(3))

    @pytest.mark.parametrize("value", [LAVA, DOOR, TRAP, BOSS_ROOM])
    def test_everything_except_walls_is_passable(self, pathfinding, value):
        pathfinding.Setup_Custom_Map([[value] * 2 for _ in range(2)])
        cells = pathfinding.maps[keys.custom].cells
        assert all(cells[x][y] == 0 for x in range(2) for y in range(2))

    def test_mixed_grid_converted_correctly(self, pathfinding):
        pathfinding.Setup_Custom_Map([
            [FLOOR, WALL],
            [LAVA,  FLOOR],
        ])
        cells = pathfinding.maps[keys.custom].cells
        assert cells[0][0] == 0   # FLOOR
        assert cells[0][1] == 1   # WALL
        assert cells[1][0] == 0   # LAVA
        assert cells[1][1] == 0   # FLOOR

    def test_unknown_tile_value_raises(self, pathfinding):
        with pytest.raises(KeyError):
            pathfinding.Setup_Custom_Map([[99]])


# ─────────────────────────────────────────────
#  3. Map building from the game tilemap
#     (the critical regression tests)
# ─────────────────────────────────────────────

class TestStandardMapBuild:
    """
    These tests guard against the sub_type vs type bug that caused the standard
    map to mark every tile as blocked (all 1s).

    The rule must use  t.type == keys.floor  NOT  t.sub_type == keys.floor,
    because sub_type is a dungeon-prefixed string like "ancient_tomb_floor".
    """

    def test_floor_tile_is_passable_when_type_is_floor_key(self):
        p = build_from_tiles({(0, 0): floor_tile()})
        assert cell(p, keys.standard) == 0, (
            "Floor tile should be passable (0). "
            "If this is 1, the standard rule is checking sub_type instead of type."
        )

    def test_wall_tile_is_impassable(self):
        p = build_from_tiles({(0, 0): wall_tile()})
        assert cell(p, keys.standard) == 1

    def test_floor_touching_wall_is_impassable(self):
        p = build_from_tiles({(0, 0): floor_tile(touching_wall=True)})
        assert cell(p, keys.standard) == 1

    def test_trapped_floor_tile_is_impassable(self):
        p = build_from_tiles({(0, 0): floor_tile(trap=MagicMock())})
        assert cell(p, keys.standard) == 1

    def test_standard_map_not_all_blocked_for_valid_floor(self):
        """Catches the exact symptom: every cell being 1."""
        tiles = {(x, y): floor_tile() for x in range(3) for y in range(3)}
        p = build_from_tiles(tiles)
        assert all(cell(p, keys.standard, x, y) == 0 for x in range(3) for y in range(3))

    def test_crystal_cavern_floor_also_passable(self):
        """A different dungeon prefix must not break the rule."""
        p = build_from_tiles({(0, 0): make_mock_tile(keys.floor, "crystal_cavern_floor")})
        assert cell(p, keys.standard) == 0

    def test_builds_all_three_game_maps(self):
        p = build_from_tiles({(0, 0): floor_tile()})
        assert set(p.maps) == {keys.standard, keys.ignore_lava, keys.void_spawn}


class TestOtherMapRules:

    def test_ignore_lava_map_allows_lava_that_standard_blocks(self):
        p = build_from_tiles({(0, 0): make_mock_tile(keys.lava_env, "ancient_tomb_lava")})
        assert cell(p, keys.standard) == 1
        assert cell(p, keys.ignore_lava) == 0

    def test_ignore_lava_map_still_blocks_wall_touching_tiles(self):
        p = build_from_tiles({(0, 0): floor_tile(touching_wall=True)})
        assert cell(p, keys.ignore_lava) == 1

    def test_void_spawn_map_allows_wall_touching_tiles(self):
        p = build_from_tiles({(0, 0): floor_tile(touching_wall=True)})
        assert cell(p, keys.standard) == 1
        assert cell(p, keys.void_spawn) == 0


class TestMapBounds:

    def test_positions_without_a_tile_stay_blocked(self):
        p = build_from_tiles({(10, 5): floor_tile(), (12, 5): floor_tile()})
        cells = p.maps[keys.standard].cells
        assert len(cells) == 3 and len(cells[0]) == 1
        assert [cells[0][0], cells[1][0], cells[2][0]] == [0, 1, 0]

    def test_gap_in_the_tilemap_blocks_the_path(self):
        p = build_from_tiles({(10, 5): floor_tile(), (12, 5): floor_tile()})
        assert p.Find_Path((10, 5), (12, 5)) == []


# ─────────────────────────────────────────────
#  4. Tile coordinates in and out
#     (replaces the old min_x / min_y offset tests)
# ─────────────────────────────────────────────

class TestTileCoordinates:

    def test_origin_is_taken_from_the_tilemap_bounds(self):
        p = build_from_tiles(row_of_floor(10, 11, 5))
        grid_map = p.maps[keys.standard]
        assert (grid_map.min_x, grid_map.min_y) == (10, 5)

    def test_find_path_takes_and_returns_tile_coordinates(self):
        p = build_from_tiles(row_of_floor(10, 14, 5))
        assert p.Find_Path((10, 5), (14, 5)) == [(10, 5), (11, 5), (12, 5), (13, 5), (14, 5)]

    def test_find_path_across_a_two_dimensional_block(self):
        tiles = {(x, y): floor_tile() for x in range(10, 13) for y in range(5, 8)}
        p = build_from_tiles(tiles)
        assert p.Find_Path((10, 5), (12, 7)) == [(10, 5), (11, 6), (12, 7)]

    def test_path_points_are_tuples(self):
        p = build_from_tiles(row_of_floor(10, 12, 5))
        assert all(isinstance(point, tuple) for point in p.Find_Path([10, 5], [12, 5]))

    def test_coordinates_outside_the_map_return_empty(self):
        """Tile (0, 0) is outside a map that starts at (10, 5). Nothing to subtract
        by hand any more, it is simply out of bounds."""
        p = build_from_tiles(row_of_floor(10, 11, 5))
        assert p.Find_Path((0, 0), (1, 0)) == []

    def test_start_on_a_blocked_tile_returns_empty(self):
        tiles = row_of_floor(10, 12, 5)
        tiles[(10, 5)] = floor_tile(touching_wall=True)
        p = build_from_tiles(tiles)
        assert p.Find_Path((10, 5), (12, 5)) == []


# ─────────────────────────────────────────────
#  5. Map selection (replaces the Set_Map tests)
# ─────────────────────────────────────────────

class TestMapSelection:

    def test_find_path_uses_the_requested_map(self, pathfinding):
        pathfinding.maps[keys.standard] = GridMap([[1, 1], [1, 1]])  # all blocked
        pathfinding.Setup_Custom_Map(open_grid(2, 2))                # all open

        assert pathfinding.Find_Path((0, 0), (1, 1), which_map=keys.custom)
        assert pathfinding.Find_Path((0, 0), (1, 1), which_map=keys.standard) == []

    def test_default_map_is_standard(self, pathfinding):
        pathfinding.maps[keys.standard] = GridMap([[1, 1], [1, 1]])
        pathfinding.Setup_Custom_Map(open_grid(2, 2))
        assert pathfinding.Find_Path((0, 0), (1, 1)) == []

    def test_no_state_leaks_between_calls(self, pathfinding):
        pathfinding.maps[keys.standard] = GridMap([[1, 1], [1, 1]])
        pathfinding.Setup_Custom_Map(open_grid(2, 2))

        assert pathfinding.Find_Path((0, 0), (1, 1), which_map=keys.custom)
        assert pathfinding.Find_Path((0, 0), (1, 1)) == []          # still standard
        assert pathfinding.Find_Path((0, 0), (1, 1), which_map=keys.custom)

    def test_unknown_map_raises_instead_of_falling_back(self, pathfinding):
        pathfinding.Setup_Custom_Map(open_grid(2, 2))
        with pytest.raises(KeyError):
            pathfinding.Find_Path((0, 0), (1, 1), which_map="nonexistent_map_key")

    def test_querying_before_any_setup_raises(self, pathfinding):
        with pytest.raises(KeyError):
            pathfinding.Find_Path((0, 0), (1, 1))


# ─────────────────────────────────────────────
#  6. Find_Path / Has_Path
# ─────────────────────────────────────────────

class TestFindPath:

    DIAGONAL_GAP = [[FLOOR, WALL],
                    [WALL,  FLOOR]]

    def test_straight_path(self, pathfinding):
        pathfinding.Setup_Custom_Map(open_grid(5, 5))
        path = pathfinding.Find_Path((0, 0), (4, 0), which_map=keys.custom)
        assert path[0] == (0, 0) and path[-1] == (4, 0)

    def test_start_equals_goal(self, pathfinding):
        pathfinding.Setup_Custom_Map(open_grid(3, 3))
        assert pathfinding.Find_Path((1, 1), (1, 1), which_map=keys.custom) == [(1, 1)]

    def test_fully_walled_returns_empty(self, pathfinding):
        pathfinding.Setup_Custom_Map([[WALL] * 3 for _ in range(3)])
        assert pathfinding.Find_Path((0, 0), (2, 2), which_map=keys.custom) == []

    def test_routes_around_a_wall(self, pathfinding):
        grid = [
            [FLOOR, FLOOR, FLOOR],   # x=0
            [WALL,  WALL,  FLOOR],   # x=1, only open at y=2
            [FLOOR, FLOOR, FLOOR],   # x=2
        ]
        pathfinding.Setup_Custom_Map(grid)
        path = pathfinding.Find_Path((0, 0), (2, 0), which_map=keys.custom)
        assert path and path[-1] == (2, 0)
        assert (1, 2) in path
        assert all(grid[x][y] != WALL for x, y in path)

    def test_diagonals_flag_controls_corner_cutting(self, pathfinding):
        pathfinding.Setup_Custom_Map(self.DIAGONAL_GAP)
        assert pathfinding.Find_Path((0, 0), (1, 1), which_map=keys.custom, diagonals=True)
        assert pathfinding.Find_Path((0, 0), (1, 1), which_map=keys.custom, diagonals=False) == []

    def test_four_way_path_has_no_diagonal_steps(self, pathfinding):
        pathfinding.Setup_Custom_Map(open_grid(5, 5))
        path = pathfinding.Find_Path((0, 0), (4, 4), which_map=keys.custom, diagonals=False)
        for (ax, ay), (bx, by) in zip(path, path[1:]):
            assert abs(bx - ax) + abs(by - ay) == 1

    def test_has_path_returns_a_bool(self, pathfinding):
        pathfinding.Setup_Custom_Map(self.DIAGONAL_GAP)
        assert pathfinding.Has_Path((0, 0), (1, 1), which_map=keys.custom) is True
        assert pathfinding.Has_Path((0, 0), (1, 1), which_map=keys.custom, diagonals=False) is False


# ─────────────────────────────────────────────
#  7. Flood fill API (tile coordinates)
# ─────────────────────────────────────────────

class TestFloodApi:

    def test_distances_use_tile_coordinates(self):
        p = build_from_tiles(row_of_floor(10, 12, 5))
        assert p.Flood_Distances((10, 5)) == {(10, 5): 0, (11, 5): 1, (12, 5): 2}

    def test_reachable_is_the_key_set_of_distances(self):
        p = build_from_tiles(row_of_floor(10, 12, 5))
        assert p.Flood_Reachable((10, 5)) == {(10, 5), (11, 5), (12, 5)}

    def test_start_outside_the_map_returns_empty(self):
        p = build_from_tiles(row_of_floor(10, 12, 5))
        assert p.Flood_Reachable((0, 0)) == set()

    def test_start_on_a_blocked_tile_returns_empty(self):
        tiles = row_of_floor(10, 12, 5)
        tiles[(11, 5)] = floor_tile(touching_wall=True)
        p = build_from_tiles(tiles)
        assert p.Flood_Reachable((11, 5)) == set()

    def test_max_steps_is_passed_through(self):
        p = build_from_tiles(row_of_floor(10, 14, 5))
        assert p.Flood_Distances((10, 5), max_steps=1) == {(10, 5): 0, (11, 5): 1}

    def test_diagonals_flag_is_passed_through(self, pathfinding):
        pathfinding.Setup_Custom_Map([[FLOOR, WALL],
                                      [WALL,  FLOOR]])
        assert (1, 1) in pathfinding.Flood_Reachable((0, 0), keys.custom, diagonals=True)
        assert (1, 1) not in pathfinding.Flood_Reachable((0, 0), keys.custom, diagonals=False)

    def test_region_labels_use_tile_coordinates(self):
        tiles = {**row_of_floor(10, 11, 5), (12, 5): wall_tile(), **row_of_floor(13, 14, 5)}
        p = build_from_tiles(tiles)
        labels, sizes = p.Label_Regions()

        assert sorted(sizes) == [2, 2]
        assert (12, 5) not in labels
        assert labels[(10, 5)] == labels[(11, 5)]
        assert labels[(13, 5)] == labels[(14, 5)]
        assert labels[(10, 5)] != labels[(13, 5)]


# ─────────────────────────────────────────────
#  8. Clear / Save / Load
# ─────────────────────────────────────────────

class TestClearSaveLoad:

    def test_clear_maps_empties_the_store(self):
        p = build_from_tiles(row_of_floor(10, 12, 5))
        p.Clear_Maps()
        assert p.maps == {}

    def test_save_load_round_trip_preserves_maps_and_origin(self):
        p = build_from_tiles(row_of_floor(10, 12, 5))

        fresh = Pathfinding(MagicMock())
        fresh.Load_Data(p.Save_Data())

        assert fresh.maps == p.maps
        assert (fresh.maps[keys.standard].min_x, fresh.maps[keys.standard].min_y) == (10, 5)
        assert fresh.Find_Path((10, 5), (12, 5)) == p.Find_Path((10, 5), (12, 5))

    def test_clearing_a_loaded_instance_leaves_the_saved_data_alone(self):
        p = build_from_tiles(row_of_floor(10, 12, 5))
        data = p.Save_Data()

        fresh = Pathfinding(MagicMock())
        fresh.Load_Data(data)
        fresh.Clear_Maps()

        assert data["maps"]
        assert p.maps


# tests/test_a_star.py
# Tests for the pure A* algorithm. No game, no mocks, no coordinate offsets.
import heapq
import math
import random

import pytest

from scripts.engine.pathfinding.a_star import pathfinding_search
from scripts.engine.pathfinding.directions import CARDINAL, DIAGONAL
from scripts.engine.pathfinding.flood_fill import flood_distances

OPEN, BLOCKED = 0, 1


# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────

def make_grid(*rows):
    """Build grid[x][y] from text rows, written top to bottom (y) and left to right (x).
    '.' is open, '#' is blocked."""
    height = len(rows)
    width = len(rows[0])
    return [[BLOCKED if rows[y][x] == "#" else OPEN for y in range(height)]
            for x in range(width)]


def open_grid(width, height):
    return [[OPEN] * height for _ in range(width)]


def step_cost(a, b):
    return 1.0 if a[0] == b[0] or a[1] == b[1] else math.sqrt(2)


def path_cost(path):
    return sum(step_cost(a, b) for a, b in zip(path, path[1:]))


def assert_valid_path(grid, path, start, goal, directions=DIAGONAL):
    """Starts and ends in the right place, never crosses a blocked cell,
    and only takes steps the movement rules allow."""
    assert path, "expected a path, got an empty list"
    assert path[0] == tuple(start)
    assert path[-1] == tuple(goal)
    for x, y in path:
        assert grid[x][y] == OPEN, f"path crosses a blocked cell at ({x}, {y})"
    for (ax, ay), (bx, by) in zip(path, path[1:]):
        assert (bx - ax, by - ay) in directions, f"illegal step ({ax},{ay}) -> ({bx},{by})"


def dijkstra_cost(grid, start, goal, directions):
    """Reference implementation: cost of the cheapest route, or None if unreachable."""
    width, height = len(grid), len(grid[0])
    dist = {start: 0.0}
    heap = [(0.0, start)]
    while heap:
        d, cell = heapq.heappop(heap)
        if cell == goal:
            return d
        if d > dist.get(cell, float("inf")):
            continue
        x, y = cell
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and grid[nx][ny] == OPEN:
                nd = d + (1.0 if dx == 0 or dy == 0 else math.sqrt(2))
                if nd < dist.get((nx, ny), float("inf")):
                    dist[(nx, ny)] = nd
                    heapq.heappush(heap, (nd, (nx, ny)))
    return None


def random_grid(rng, size=10, wall_chance=0.3):
    return [[BLOCKED if rng.random() < wall_chance else OPEN for _ in range(size)]
            for _ in range(size)]


def grid_for_seed(seed):
    """Alternate sparse and dense walls so both reachable and unreachable goals show up."""
    rng = random.Random(seed)
    wall_chance = 0.3 if seed % 2 == 0 else 0.55
    return rng, random_grid(rng, wall_chance=wall_chance)


def random_start_goal(rng, grid):
    cells = [(x, y) for x in range(len(grid)) for y in range(len(grid[0]))
             if grid[x][y] == OPEN]
    if len(cells) < 2:
        pytest.skip("random grid had fewer than two open cells")
    return rng.sample(cells, 2)


# ─────────────────────────────────────────────
#  1. Basic paths (8-way, the default)
# ─────────────────────────────────────────────

class TestBasicPaths:

    def test_straight_line(self):
        grid = open_grid(5, 5)
        path = pathfinding_search(grid, (0, 0), (4, 0))
        assert_valid_path(grid, path, (0, 0), (4, 0))
        assert len(path) == 5

    def test_diagonal_shortcut_is_taken(self):
        path = pathfinding_search(open_grid(5, 5), (0, 0), (4, 4))
        assert path == [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]

    def test_start_equals_goal(self):
        assert pathfinding_search(open_grid(3, 3), (1, 1), (1, 1)) == [(1, 1)]

    def test_accepts_lists_and_returns_tuples(self):
        path = pathfinding_search(open_grid(3, 3), [0, 0], [2, 0])
        assert path == [(0, 0), (1, 0), (2, 0)]

    def test_default_movement_is_eight_way(self):
        grid = open_grid(3, 3)
        assert len(pathfinding_search(grid, (0, 0), (2, 2))) == 3
        assert len(pathfinding_search(grid, (0, 0), (2, 2), CARDINAL)) == 5

    def test_does_not_modify_the_grid(self):
        grid = make_grid("..#",
                         ".#.",
                         "...")
        snapshot = [column[:] for column in grid]
        pathfinding_search(grid, (0, 0), (2, 2))
        assert grid == snapshot


# ─────────────────────────────────────────────
#  2. Obstacles, blocked and invalid input
# ─────────────────────────────────────────────

class TestObstaclesAndInvalidInput:

    def test_routes_around_a_wall(self):
        grid = make_grid(".#.",
                         ".#.",
                         "...")
        path = pathfinding_search(grid, (0, 0), (2, 0))
        assert_valid_path(grid, path, (0, 0), (2, 0))
        assert (1, 2) in path  # the only gap in the wall

    def test_path_through_a_maze_stays_on_open_cells(self):
        grid = make_grid(".....",
                         ".###.",
                         "...#.",
                         ".....")
        path = pathfinding_search(grid, (0, 0), (4, 3))
        assert_valid_path(grid, path, (0, 0), (4, 3))

    def test_fully_blocked_grid_returns_empty(self):
        grid = make_grid("###",
                         "###",
                         "###")
        assert pathfinding_search(grid, (0, 0), (2, 2)) == []

    def test_goal_behind_a_full_wall_returns_empty(self):
        grid = make_grid("..#..",
                         "..#..",
                         "..#..")
        assert pathfinding_search(grid, (0, 0), (4, 0)) == []

    def test_start_on_wall_returns_empty(self):
        grid = make_grid("..",
                         "#.")
        assert pathfinding_search(grid, (0, 1), (0, 0)) == []

    def test_goal_on_wall_returns_empty(self):
        grid = make_grid("..",
                         "#.")
        assert pathfinding_search(grid, (0, 0), (0, 1)) == []

    def test_start_out_of_bounds_returns_empty(self):
        assert pathfinding_search(open_grid(3, 3), (-1, 0), (2, 2)) == []

    def test_goal_out_of_bounds_returns_empty(self):
        assert pathfinding_search(open_grid(3, 3), (0, 0), (99, 99)) == []

    def test_empty_grid_returns_empty(self):
        assert pathfinding_search([], (0, 0), (0, 0)) == []


# ─────────────────────────────────────────────
#  3. Movement rules
# ─────────────────────────────────────────────

class TestMovementRules:

    def test_cardinal_search_never_moves_diagonally(self):
        grid = open_grid(5, 5)
        path = pathfinding_search(grid, (0, 0), (4, 4), CARDINAL)
        assert_valid_path(grid, path, (0, 0), (4, 4), CARDINAL)

    def test_cardinal_path_length_is_manhattan_distance(self):
        path = pathfinding_search(open_grid(5, 5), (0, 0), (4, 0), CARDINAL)
        assert len(path) == 5  # 4 steps plus the start

    def test_cardinal_corner_to_corner(self):
        path = pathfinding_search(open_grid(3, 3), (0, 0), (1, 1), CARDINAL)
        assert len(path) == 3
        assert path[1] in [(1, 0), (0, 1)]

    def test_cardinal_search_blocked_returns_empty(self):
        grid = make_grid(".#",
                         "#.")
        assert pathfinding_search(grid, (0, 0), (1, 1), CARDINAL) == []

    def test_diagonal_moves_can_cut_between_two_blocked_corners(self):
        """Documents current behaviour (same as the old A*). If you ever forbid
        corner cutting, this is the test to change."""
        grid = make_grid(".#",
                         "#.")
        assert pathfinding_search(grid, (0, 0), (1, 1)) == [(0, 0), (1, 1)]


# ─────────────────────────────────────────────
#  4. Cross-checks against reference implementations
#     (random grids, fixed seeds so failures are reproducible)
# ─────────────────────────────────────────────

@pytest.mark.parametrize("seed", range(25))
class TestAgainstReferences:

    def test_cardinal_matches_breadth_first_search(self, seed):
        rng, grid = grid_for_seed(seed)
        start, goal = random_start_goal(rng, grid)

        path = pathfinding_search(grid, start, goal, CARDINAL)
        reachable = flood_distances(grid, start, CARDINAL)

        if goal not in reachable:
            assert path == []
        else:
            assert_valid_path(grid, path, start, goal, CARDINAL)
            assert len(path) - 1 == reachable[goal]

    def test_diagonal_path_is_optimal(self, seed):
        rng, grid = grid_for_seed(seed)
        start, goal = random_start_goal(rng, grid)

        path = pathfinding_search(grid, start, goal, DIAGONAL)
        expected = dijkstra_cost(grid, start, goal, DIAGONAL)

        if expected is None:
            assert path == []
        else:
            assert_valid_path(grid, path, start, goal, DIAGONAL)
            assert path_cost(path) == pytest.approx(expected)

# tests/test_flood_fill.py
# Tests for the pure flood fill tool. No game, no mocks, no coordinate offsets.
import random

import pytest

from scripts.engine.pathfinding.directions import CARDINAL, DIAGONAL
from scripts.engine.pathfinding.flood_fill import (
    flood_distances, flood_reachable, label_regions,
)

OPEN, BLOCKED = 0, 1


def make_grid(*rows):
    """Build grid[x][y] from text rows, written top to bottom (y) and left to right (x).
    '.' is open, '#' is blocked."""
    height = len(rows)
    width = len(rows[0])
    return [[BLOCKED if rows[y][x] == "#" else OPEN for y in range(height)]
            for x in range(width)]


def open_grid(width, height):
    return [[OPEN] * height for _ in range(width)]


def random_grid(rng, size=12, wall_chance=0.35):
    return [[BLOCKED if rng.random() < wall_chance else OPEN for _ in range(size)]
            for _ in range(size)]


# Two open cells that only touch diagonally
DIAGONAL_GAP = make_grid(".#",
                         "#.")


# ─────────────────────────────────────────────
#  1. flood_distances
# ─────────────────────────────────────────────

class TestFloodDistances:

    def test_start_has_distance_zero(self):
        assert flood_distances(open_grid(3, 3), (1, 1))[(1, 1)] == 0

    def test_cardinal_distances_are_manhattan(self):
        dist = flood_distances(open_grid(4, 4), (0, 0), CARDINAL)
        assert len(dist) == 16
        assert dist[(3, 3)] == 6
        assert dist[(2, 1)] == 3

    def test_diagonal_distances_count_each_step_as_one(self):
        dist = flood_distances(open_grid(4, 4), (0, 0), DIAGONAL)
        assert dist[(3, 3)] == 3
        assert dist[(3, 1)] == 3  # Chebyshev distance

    def test_default_movement_is_eight_way(self):
        assert flood_distances(open_grid(3, 3), (0, 0))[(2, 2)] == 2

    def test_walls_split_the_grid(self):
        grid = make_grid("..#..",
                         "..#..")
        assert flood_reachable(grid, (0, 0)) == {(0, 0), (1, 0), (0, 1), (1, 1)}

    def test_start_on_wall_returns_empty(self):
        grid = make_grid("#.")
        assert flood_distances(grid, (0, 0)) == {}

    def test_start_out_of_bounds_returns_empty(self):
        assert flood_distances(open_grid(3, 3), (-1, 0)) == {}
        assert flood_distances(open_grid(3, 3), (3, 0)) == {}

    def test_empty_grid_returns_empty(self):
        assert flood_distances([], (0, 0)) == {}

    def test_accepts_list_start(self):
        assert flood_reachable(open_grid(2, 2), [0, 0]) == {(0, 0), (1, 0), (0, 1), (1, 1)}

    def test_max_steps_limits_the_search(self):
        dist = flood_distances(open_grid(5, 5), (0, 0), CARDINAL, max_steps=2)
        assert set(dist) == {(0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2)}
        assert max(dist.values()) == 2

    def test_max_steps_zero_returns_only_the_start(self):
        assert flood_distances(open_grid(3, 3), (1, 1), max_steps=0) == {(1, 1): 0}

    def test_does_not_modify_the_grid(self):
        grid = make_grid("..#",
                         ".#.",
                         "...")
        snapshot = [column[:] for column in grid]
        flood_distances(grid, (0, 0))
        assert grid == snapshot


# ─────────────────────────────────────────────
#  2. flood_reachable
# ─────────────────────────────────────────────

class TestFloodReachable:

    def test_is_the_key_set_of_flood_distances(self):
        grid = make_grid("..#.",
                         ".#..",
                         "....")
        assert flood_reachable(grid, (0, 0)) == set(flood_distances(grid, (0, 0)))

    def test_diagonal_gap_is_crossed_with_eight_way_movement(self):
        assert (1, 1) in flood_reachable(DIAGONAL_GAP, (0, 0), DIAGONAL)

    def test_diagonal_gap_is_not_crossed_with_four_way_movement(self):
        assert (1, 1) not in flood_reachable(DIAGONAL_GAP, (0, 0), CARDINAL)


# ─────────────────────────────────────────────
#  3. label_regions
# ─────────────────────────────────────────────

class TestLabelRegions:

    def test_two_separate_regions(self):
        grid = make_grid("..#..",
                         "..#..")
        labels, sizes = label_regions(grid)
        assert sorted(sizes) == [4, 4]
        assert labels[(0, 0)] == labels[(1, 1)]
        assert labels[(0, 0)] != labels[(4, 1)]

    def test_blocked_cells_are_not_labelled(self):
        grid = make_grid(".#.")
        labels, _ = label_regions(grid)
        assert (1, 0) not in labels

    def test_region_ids_are_contiguous_and_match_sizes(self):
        grid = make_grid(".#.#.",
                         ".#.#.")
        labels, sizes = label_regions(grid)
        assert set(labels.values()) == set(range(len(sizes)))
        for region_id, size in enumerate(sizes):
            assert sum(1 for r in labels.values() if r == region_id) == size

    def test_diagonal_gap_joins_regions_only_with_eight_way_movement(self):
        _, sizes_diagonal = label_regions(DIAGONAL_GAP, DIAGONAL)
        _, sizes_cardinal = label_regions(DIAGONAL_GAP, CARDINAL)
        assert sizes_diagonal == [2]
        assert sizes_cardinal == [1, 1]

    def test_fully_blocked_grid_has_no_regions(self):
        assert label_regions(make_grid("##", "##")) == ({}, [])

    def test_empty_grid_has_no_regions(self):
        assert label_regions([]) == ({}, [])


# ─────────────────────────────────────────────
#  4. Consistency on random grids
# ─────────────────────────────────────────────

@pytest.mark.parametrize("seed", range(15))
class TestConsistency:

    def test_region_sizes_add_up_to_the_open_cells(self, seed):
        grid = random_grid(random.Random(seed))
        open_cells = sum(cell == OPEN for column in grid for cell in column)
        labels, sizes = label_regions(grid)
        assert len(labels) == open_cells
        assert sum(sizes) == open_cells

    def test_a_region_is_exactly_what_flood_reachable_finds(self, seed):
        grid = random_grid(random.Random(seed))
        labels, _ = label_regions(grid)
        if not labels:
            pytest.skip("random grid had no open cells")

        start = next(iter(labels))
        same_region = {cell for cell, region in labels.items() if region == labels[start]}
        assert flood_reachable(grid, start) == same_region