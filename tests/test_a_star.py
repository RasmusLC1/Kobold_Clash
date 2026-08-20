# tests/test_a_star.py
import pytest
from unittest.mock import MagicMock, patch
from scripts.engine.a_star import A_Star
from scripts.engine.keys.keys import keys

FLOOR, WALL, LAVA = 0, 1, 2


# ─────────────────────────────────────────────
#  Fixtures
# ─────────────────────────────────────────────

@pytest.fixture
def mock_game():
    game = MagicMock()
    return game


@pytest.fixture
def astar(mock_game):
    return A_Star(mock_game)


def open_grid(w, h):
    """All-floor grid of size w × h."""
    return [[FLOOR for _ in range(h)] for _ in range(w)]


def apply_custom(astar, grid, w, h):
    astar.Setup_Custom_Map(grid, w, h)
    astar.Set_Map('custom')


def make_mock_tile(type_val, sub_type_val, touching_wall=False, trap=None, physics=False):
    """
    Build a tile mock that mirrors what Tilemap.Generate_Tile produces.
    type      → raw key e.g. keys.floor  (what Build_Standard_Map must check)
    sub_type  → prefixed e.g. "crypt_floor" (what sub_type actually contains)
    """
    tile = MagicMock()
    tile.type = type_val
    tile.sub_type = sub_type_val          # deliberately different from type
    tile.touching_wall = touching_wall
    tile.trap = trap
    tile.physics = physics
    return tile


# ─────────────────────────────────────────────
#  1. Custom-map setup
# ─────────────────────────────────────────────

class TestCustomMapSetup:

    def test_dimensions_stored(self, astar):
        apply_custom(astar, open_grid(6, 4), 6, 4)
        assert astar.width == 6
        assert astar.height == 4

    def test_floor_cells_are_zero(self, astar):
        apply_custom(astar, open_grid(3, 3), 3, 3)
        assert all(astar.map[x][y] == 0 for x in range(3) for y in range(3))

    def test_wall_cells_are_one(self, astar):
        grid = [[WALL for _ in range(3)] for _ in range(3)]
        apply_custom(astar, grid, 3, 3)
        assert all(astar.map[x][y] == 1 for x in range(3) for y in range(3))

    def test_lava_treated_as_floor_in_custom(self, astar):
        """Lava maps to 0 in Setup_Custom_Map (passable)."""
        grid = [[LAVA for _ in range(3)] for _ in range(3)]
        apply_custom(astar, grid, 3, 3)
        assert all(astar.map[x][y] == 0 for x in range(3) for y in range(3))

    def test_mixed_grid_converted_correctly(self, astar):
        grid = [
            [FLOOR, WALL],
            [LAVA,  FLOOR],
        ]
        apply_custom(astar, grid, 2, 2)
        assert astar.map[0][0] == 0   # FLOOR → 0
        assert astar.map[0][1] == 1   # WALL  → 1
        assert astar.map[1][0] == 0   # LAVA  → 0
        assert astar.map[1][1] == 0   # FLOOR → 0


# ─────────────────────────────────────────────
#  2. Standard-map build — the critical regression tests
# ─────────────────────────────────────────────

class TestStandardMapBuild:
    """
    These tests guard against the sub_type vs type bug that caused
    Build_Standard_Map to mark every tile as blocked (all 1s).

    The rule must use  t.type == keys.floor  NOT  t.sub_type == keys.floor,
    because sub_type is a dungeon-prefixed string like "crypt_floor".
    """

    def _make_game_with_tiles(self, tiles_by_pos):
        """Wire up a mock game whose tilemap returns a fixed tile set."""
        game = MagicMock()
        game.tilemap.Get_Pos.return_value = list(tiles_by_pos.keys())
        game.tilemap.Current_Tile.side_effect = lambda pos: tiles_by_pos.get(pos)
        return game

    def test_floor_tile_is_passable_when_type_is_floor_key(self):
        """
        Regression: rule must hit t.type (keys.floor), not t.sub_type.
        If it checked sub_type the tile would map to 1 and this test fails.
        """
        tile = make_mock_tile(
            type_val=keys.floor,
            sub_type_val="crypt_floor",   # realistic prefixed value
            touching_wall=False,
            trap=None,
        )
        game = self._make_game_with_tiles({(0, 0): tile})
        a = A_Star(game)
        a.Setup_Map_From_Game(game)

        assert a.standard_map[0][0] == 0, (
            "Floor tile should be passable (0). "
            "If this is 1, Build_Standard_Map is checking sub_type instead of type."
        )

    def test_wall_tile_is_impassable(self):
        tile = make_mock_tile(
            type_val="wall",
            sub_type_val="crypt_wall",
            touching_wall=False,
        )
        game = self._make_game_with_tiles({(0, 0): tile})
        a = A_Star(game)
        a.Setup_Map_From_Game(game)
        assert a.standard_map[0][0] == 1

    def test_floor_touching_wall_is_impassable(self):
        tile = make_mock_tile(
            type_val=keys.floor,
            sub_type_val="crypt_floor",
            touching_wall=True,
        )
        game = self._make_game_with_tiles({(0, 0): tile})
        a = A_Star(game)
        a.Setup_Map_From_Game(game)
        assert a.standard_map[0][0] == 1

    def test_trapped_floor_tile_is_impassable(self):
        tile = make_mock_tile(
            type_val=keys.floor,
            sub_type_val="crypt_floor",
            touching_wall=False,
            trap=MagicMock(),  # any truthy trap
        )
        game = self._make_game_with_tiles({(0, 0): tile})
        a = A_Star(game)
        a.Setup_Map_From_Game(game)
        assert a.standard_map[0][0] == 1

    def test_standard_map_not_all_ones_for_valid_floor(self):
        """Catches the exact symptom: every cell being 1 (all blocked)."""
        tiles = {
            (x, y): make_mock_tile(keys.floor, "crypt_floor")
            for x in range(3) for y in range(3)
        }
        game = self._make_game_with_tiles(tiles)
        a = A_Star(game)
        a.Setup_Map_From_Game(game)

        all_blocked = all(
            a.standard_map[x][y] == 1
            for x in range(a.width)
            for y in range(a.height)
        )
        assert not all_blocked, (
            "Every cell is blocked — Build_Standard_Map rule never matched. "
            "Check that it uses t.type, not t.sub_type."
        )

    def test_crystal_cavern_floor_also_passable(self):
        """Different dungeon prefix must not break the rule."""
        tile = make_mock_tile(
            type_val=keys.floor,
            sub_type_val="crystal_cavern_floor",
        )
        game = self._make_game_with_tiles({(0, 0): tile})
        a = A_Star(game)
        a.Setup_Map_From_Game(game)
        assert a.standard_map[0][0] == 0


# ─────────────────────────────────────────────
#  3. Map selection
# ─────────────────────────────────────────────

class TestMapSelection:

    def test_set_map_standard(self, astar):
        apply_custom(astar, open_grid(2, 2), 2, 2)
        astar.standard_map = [[0, 0], [0, 0]]
        astar.Set_Map(keys.standard)
        assert astar.map is astar.standard_map

    def test_set_map_custom(self, astar):
        apply_custom(astar, open_grid(2, 2), 2, 2)
        astar.Set_Map('custom')
        assert astar.map is astar.custom_map

    def test_set_map_unknown_falls_back_to_standard(self, astar):
        astar.standard_map = [[0]]
        astar.Set_Map('nonexistent_map_key')
        assert astar.map is astar.standard_map


# ─────────────────────────────────────────────
#  4. Validity and passability helpers
# ─────────────────────────────────────────────

class TestHelpers:

    def test_is_valid_inside_bounds(self, astar):
        apply_custom(astar, open_grid(5, 5), 5, 5)
        assert astar.is_valid(0, 0)
        assert astar.is_valid(4, 4)
        assert astar.is_valid(2, 3)

    def test_is_valid_outside_bounds(self, astar):
        apply_custom(astar, open_grid(5, 5), 5, 5)
        assert not astar.is_valid(-1, 0)
        assert not astar.is_valid(0, -1)
        assert not astar.is_valid(5, 0)
        assert not astar.is_valid(0, 5)

    def test_is_unblocked_floor(self, astar):
        apply_custom(astar, open_grid(3, 3), 3, 3)
        assert astar.is_unblocked(1, 1)

    def test_is_unblocked_wall(self, astar):
        grid = [[WALL for _ in range(3)] for _ in range(3)]
        apply_custom(astar, grid, 3, 3)
        assert not astar.is_unblocked(0, 0)

    def test_heuristic_is_euclidean(self, astar):
        assert astar.calculate_h_value(0, 0, (3, 4)) == pytest.approx(5.0)
        assert astar.calculate_h_value(1, 1, (1, 1)) == pytest.approx(0.0)


# ─────────────────────────────────────────────
#  5. A* 8-directional search
# ─────────────────────────────────────────────

class TestAStarSearch:

    def test_straight_line_path(self, astar):
        apply_custom(astar, open_grid(5, 5), 5, 5)
        path = astar.a_star_search([0, 0], [4, 0], 'custom')
        assert path[0] == (0, 0)
        assert path[-1] == (4, 0)

    def test_diagonal_path_used(self, astar):
        """8-directional search should cut corners — path length < manhattan distance."""
        apply_custom(astar, open_grid(5, 5), 5, 5)
        path = astar.a_star_search([0, 0], [4, 4], 'custom')
        assert len(path) == 5   # diagonal cuts: (0,0)→(1,1)→(2,2)→(3,3)→(4,4)

    def test_start_equals_goal(self, astar):
        apply_custom(astar, open_grid(3, 3), 3, 3)
        path = astar.a_star_search([1, 1], [1, 1], 'custom')
        assert len(path) == 1
        assert path[0][0] == 1 and path[0][1] == 1

    def test_fully_walled_returns_empty(self, astar):
        grid = [[WALL for _ in range(3)] for _ in range(3)]
        apply_custom(astar, grid, 3, 3)
        path = astar.a_star_search([0, 0], [2, 2], 'custom')
        assert path == []

    def test_start_on_wall_returns_empty(self, astar):
        grid = [[FLOOR, FLOOR], [WALL, FLOOR]]
        apply_custom(astar, grid, 2, 2)
        path = astar.a_star_search([1, 0], [0, 0], 'custom')
        assert path == []

    def test_goal_on_wall_returns_empty(self, astar):
        grid = [[FLOOR, FLOOR], [WALL, FLOOR]]
        apply_custom(astar, grid, 2, 2)
        path = astar.a_star_search([0, 0], [1, 0], 'custom')
        assert path == []

    def test_start_out_of_bounds_returns_empty(self, astar):
        apply_custom(astar, open_grid(3, 3), 3, 3)
        path = astar.a_star_search([-1, 0], [2, 2], 'custom')
        assert path == []

    def test_goal_out_of_bounds_returns_empty(self, astar):
        apply_custom(astar, open_grid(3, 3), 3, 3)
        path = astar.a_star_search([0, 0], [99, 99], 'custom')
        assert path == []

    def test_routes_around_wall(self, astar):
        """
        Path blocked at x=1 (full column wall), but open at the top (y=0)
        so 8-directional search can go around diagonally.

        Grid (x=col, y=row):
          x:  0     1     2
          y0: floor wall  floor
          y1: floor wall  floor
          y2: floor floor floor
        """
        grid = [
            [FLOOR, FLOOR, FLOOR],   # x=0
            [WALL,  WALL,  FLOOR],   # x=1 (wall except y=2)
            [FLOOR, FLOOR, FLOOR],   # x=2
        ]
        apply_custom(astar, grid, 3, 3)
        path = astar.a_star_search([0, 0], [2, 0], 'custom')
        assert len(path) > 0
        assert path[-1] == (2, 0)
        # Path must not pass through any wall cell
        for (x, y) in path:
            assert grid[x][y] == FLOOR

    def test_path_contains_no_wall_cells(self, astar):
        """Every cell in the returned path must be passable."""
        grid = [
            [FLOOR, FLOOR, FLOOR, FLOOR, FLOOR],
            [FLOOR, WALL,  WALL,  WALL,  FLOOR],
            [FLOOR, FLOOR, FLOOR, WALL,  FLOOR],
            [FLOOR, FLOOR, FLOOR, FLOOR, FLOOR],
        ]
        apply_custom(astar, grid, 4, 5)
        path = astar.a_star_search([0, 0], [3, 4], 'custom')
        assert path, "Expected a valid path"
        for (x, y) in path:
            assert grid[x][y] == FLOOR, f"Path passes through wall at ({x}, {y})"

    def test_path_is_connected(self, astar):
        """Each step must be adjacent (max Chebyshev distance of 1)."""
        apply_custom(astar, open_grid(6, 6), 6, 6)
        path = astar.a_star_search([0, 0], [5, 5], 'custom')
        for (ax, ay), (bx, by) in zip(path, path[1:]):
            assert max(abs(bx - ax), abs(by - ay)) == 1


# ─────────────────────────────────────────────
#  6. A* 4-directional (no diagonals) search
# ─────────────────────────────────────────────

class TestAStarNoDialogals:

    def test_no_diagonal_moves(self, astar):
        """Every step must be orthogonal (Chebyshev distance == 1, Manhattan == 1)."""
        apply_custom(astar, open_grid(5, 5), 5, 5)
        path = astar.a_star_search_no_diagonals([0, 0], [4, 4], 'custom')
        for (ax, ay), (bx, by) in zip(path, path[1:]):
            assert abs(bx - ax) + abs(by - ay) == 1, \
                f"Diagonal move detected: ({ax},{ay}) → ({bx},{by})"

    def test_manhattan_distance_path_length(self, astar):
        """On an open grid, path length == manhattan distance + 1."""
        apply_custom(astar, open_grid(5, 5), 5, 5)
        path = astar.a_star_search_no_diagonals([0, 0], [4, 0], 'custom')
        assert len(path) == 5   # 4 steps + start

    def test_corner_to_corner_no_diagonals(self, astar):
        apply_custom(astar, open_grid(3, 3), 3, 3)
        path = astar.a_star_search_no_diagonals([0, 0], [1, 1], 'custom')
        assert len(path) == 3
        assert path[1] in [(1, 0), (0, 1)]

    def test_blocked_returns_empty(self, astar):
        grid = [
            [FLOOR, WALL],
            [WALL,  FLOOR],
        ]
        apply_custom(astar, grid, 2, 2)
        path = astar.a_star_search_no_diagonals([0, 0], [1, 1], 'custom')
        assert path == []


# ─────────────────────────────────────────────
#  7. Coordinate offset handling
#     (the runtime bug: world tile coords vs map-local coords)
# ─────────────────────────────────────────────

class TestCoordinateOffsets:

    def test_min_offsets_populated_after_setup_from_game(self):
        """
        Setup_Map_From_Game must store non-zero min_x/min_y when the tilemap
        does not start at (0,0).  Find_Shortest_Path subtracts these before
        calling a_star_search — if they are 0 the subtraction is a no-op and
        world coords get passed in raw, causing is_valid to fail immediately.
        """
        tile = make_mock_tile(keys.floor, "crypt_floor")
        tile.pos = (10, 5)
        tile.sub_type = "crypt_floor"
        tile.type = keys.floor
        tile.trap = None
        tile.touching_wall = False

        game = MagicMock()
        game.tilemap.Get_Pos.return_value = [(10, 5)]
        game.tilemap.Current_Tile.return_value = tile

        a = A_Star(game)
        a.Setup_Map_From_Game(game)

        assert a.min_x == 10
        assert a.min_y == 5

    def test_raw_world_coords_fail_is_valid(self):
        """
        Passing un-offset world tile coords directly to a_star_search must
        return [] — this is the exact symptom of the missing subtraction bug.
        """
        tiles = {
            (10, 5): make_mock_tile(keys.floor, "crypt_floor"),
            (11, 5): make_mock_tile(keys.floor, "crypt_floor"),
        }
        game = MagicMock()
        game.tilemap.Get_Pos.return_value = list(tiles.keys())
        game.tilemap.Current_Tile.side_effect = lambda pos: tiles.get(pos)

        a = A_Star(game)
        a.Setup_Map_From_Game(game)
        a.Set_Map(keys.standard)

        # (10, 5) is out of the map-local bounds [0..width)
        path = a.a_star_search([10, 5], [11, 5], keys.standard)
        assert path == [], "Raw world coords should fail is_valid — subtract min_x/min_y first"

    def test_offset_coords_succeed(self):
        """After subtracting min_x/min_y the same path must be found."""
        tiles = {
            (10, 5): make_mock_tile(keys.floor, "crypt_floor"),
            (11, 5): make_mock_tile(keys.floor, "crypt_floor"),
        }
        game = MagicMock()
        game.tilemap.Get_Pos.return_value = list(tiles.keys())
        game.tilemap.Current_Tile.side_effect = lambda pos: tiles.get(pos)

        a = A_Star(game)
        a.Setup_Map_From_Game(game)
        a.Set_Map(keys.standard)

        src = [10 - a.min_x, 5 - a.min_y]
        dst = [11 - a.min_x, 5 - a.min_y]
        path = a.a_star_search(src, dst, keys.standard)
        assert len(path) > 0

    def test_result_path_can_be_re_offset(self):
        """After finding a path, adding min_x/min_y back must yield world coords."""
        tiles = {(10, 5): make_mock_tile(keys.floor, "crypt_floor"),
                 (11, 5): make_mock_tile(keys.floor, "crypt_floor")}
        game = MagicMock()
        game.tilemap.Get_Pos.return_value = list(tiles.keys())
        game.tilemap.Current_Tile.side_effect = lambda pos: tiles.get(pos)

        a = A_Star(game)
        a.Setup_Map_From_Game(game)
        a.Set_Map(keys.standard)

        path = a.a_star_search([0, 0], [1, 0], keys.standard)
        world_path = [(x + a.min_x, y + a.min_y) for (x, y) in path]

        assert (10, 5) in world_path
        assert (11, 5) in world_path


# ─────────────────────────────────────────────
#  8. Save / Load round-trip
# ─────────────────────────────────────────────

class TestSaveLoad:

    def test_save_load_preserves_map(self, astar):
        apply_custom(astar, open_grid(3, 3), 3, 3)
        astar.min_x, astar.min_y = 2, 4
        astar.Save_Data()

        fresh = A_Star(MagicMock())
        fresh.Load_Data(astar.saved_data)

        assert fresh.min_x == 2
        assert fresh.min_y == 4
        assert fresh.width == 3
        assert fresh.height == 3
        assert fresh.custom_map == astar.custom_map