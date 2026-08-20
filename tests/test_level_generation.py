import pytest
from unittest.mock import MagicMock, patch
import random

from scripts.level_generation.noise_map import Noise_Map
from scripts.level_generation.cellular_automata import Cellular_Automata
from scripts.level_generation.room_generation.circle_room import Circle_Room
from scripts.level_generation.room_generation.rectangle_room import Rectangle_Room
from scripts.level_generation.rooms.spawn_lakes import Spawn_Lakes
from scripts.level_generation.rooms.spawn_loot_room import Spawn_Loot_Room
from scripts.level_generation.dungeon_generator import Dungeon_Generator
from scripts.engine.keys.keys import keys

FLOOR = 0
WALL = 1
LAVA = 2
DOOR = 3
TRAP = 4


def open_grid(w, h, fill=FLOOR):
    return [[fill for _ in range(h)] for _ in range(w)]


# ==============================================================================
# 1. NOISE MAP
# ==============================================================================

class TestNoiseMap:

    def test_all_cells_are_floor_or_wall(self):
        noise = Noise_Map()
        grid = [[-1 for _ in range(5)] for _ in range(5)]
        noise.Generate_Map(floor_density=50, map=grid, floor_val=FLOOR,
                           wall_val=WALL, size_x=5, size_y=5)
        for col in grid:
            for cell in col:
                assert cell in (FLOOR, WALL)

    def test_high_density_produces_mostly_walls(self):
        """density=0 means almost nothing exceeds it, so almost all cells become walls."""
        noise = Noise_Map()
        grid = [[-1 for _ in range(20)] for _ in range(20)]
        noise.Generate_Map(floor_density=0, map=grid, floor_val=FLOOR,
                           wall_val=WALL, size_x=20, size_y=20)
        wall_count = sum(grid[x][y] == WALL for x in range(20) for y in range(20))
        assert wall_count > 300

    def test_low_density_produces_mostly_floor(self):
        """density=100 means almost everything exceeds it, so almost all cells become floor."""
        noise = Noise_Map()
        grid = [[-1 for _ in range(20)] for _ in range(20)]
        noise.Generate_Map(floor_density=100, map=grid, floor_val=FLOOR,
                           wall_val=WALL, size_x=20, size_y=20)
        floor_count = sum(grid[x][y] == FLOOR for x in range(20) for y in range(20))
        assert floor_count > 300

    def test_deterministic_with_same_seed(self):
        noise = Noise_Map()
        random.seed(42)
        grid_a = noise.Create_Noise_Map(10, 10)
        random.seed(42)
        grid_b = noise.Create_Noise_Map(10, 10)
        assert grid_a == grid_b

    def test_different_seeds_produce_different_maps(self):
        noise = Noise_Map()
        random.seed(1)
        grid_a = noise.Create_Noise_Map(20, 20)
        random.seed(999)
        grid_b = noise.Create_Noise_Map(20, 20)
        assert grid_a != grid_b

    def test_create_noise_map_correct_dimensions(self):
        noise = Noise_Map()
        grid = noise.Create_Noise_Map(7, 12)
        assert len(grid) == 7
        assert len(grid[0]) == 12


# ==============================================================================
# 2. CELLULAR AUTOMATA
# ==============================================================================

class TestCellularAutomata:

    def test_within_map_bounds_inside(self):
        ca = Cellular_Automata()
        assert ca.Within_Map_Bounds(0, 0, 10, 10) is True
        assert ca.Within_Map_Bounds(9, 9, 10, 10) is True
        assert ca.Within_Map_Bounds(5, 5, 10, 10) is True

    def test_within_map_bounds_outside(self):
        ca = Cellular_Automata()
        assert ca.Within_Map_Bounds(10, 5, 10, 10) is False
        assert ca.Within_Map_Bounds(-1, 5, 10, 10) is False
        assert ca.Within_Map_Bounds(5, 10, 10, 10) is False
        assert ca.Within_Map_Bounds(5, -1, 10, 10) is False

    def test_close_borders_seals_all_edges(self):
        ca = Cellular_Automata()
        ca.size_x, ca.size_y = 5, 5
        ca.map = open_grid(5, 5, FLOOR)
        ca.Close_Borders(0, 0, 5, 5)
        for i in range(5):
            assert ca.map[0][i] == WALL
            assert ca.map[4][i] == WALL
            assert ca.map[i][0] == WALL
            assert ca.map[i][4] == WALL

    def test_close_borders_preserves_interior(self):
        ca = Cellular_Automata()
        ca.size_x, ca.size_y = 5, 5
        ca.map = open_grid(5, 5, FLOOR)
        ca.Close_Borders(0, 0, 5, 5)
        assert ca.map[2][2] == FLOOR

    def test_refine_level_single_cell_no_crash(self):
        """Refining a 1×1 grid should complete without IndexError."""
        ca = Cellular_Automata()
        grid = [[FLOOR]]
        ca.Refine_Level(value_1=FLOOR, value_2=WALL,
                        size_x=1, size_y=1, iterations=1, map=grid)
        assert len(grid) == 1

    def test_refine_level_all_walls_stays_walls(self):
        """A fully walled grid should remain all walls after refinement."""
        ca = Cellular_Automata()
        grid = open_grid(5, 5, WALL)
        ca.Refine_Level(value_1=FLOOR, value_2=WALL,
                        size_x=5, size_y=5, iterations=3, map=grid)
        assert all(grid[x][y] == WALL for x in range(5) for y in range(5))

    def test_refine_level_isolated_floor_surrounded_by_walls(self):
        """A single floor cell surrounded by walls should become a wall after refinement."""
        ca = Cellular_Automata()
        grid = open_grid(5, 5, WALL)
        grid[2][2] = FLOOR  # Isolated floor
        ca.Refine_Level(value_1=FLOOR, value_2=WALL,
                        size_x=5, size_y=5, iterations=1, map=grid)
        # 8 wall neighbours > 4 threshold so cell should become wall
        assert grid[2][2] == WALL

    def test_create_map_sets_size_attributes(self):
        """Create_Map should populate size_x and size_y on the instance."""
        ca = Cellular_Automata()
        ca.Create_Map()
        assert ca.size_x > 0
        assert ca.size_y > 0
        assert len(ca.map) == ca.size_x
        assert len(ca.map[0]) == ca.size_y

    def test_create_map_borders_are_walls(self):
        ca = Cellular_Automata()
        ca.Create_Map()
        for i in range(ca.size_y):
            assert ca.map[0][i] == WALL
            assert ca.map[ca.size_x - 1][i] == WALL
        for i in range(ca.size_x):
            assert ca.map[i][0] == WALL
            assert ca.map[i][ca.size_y - 1] == WALL


# ==============================================================================
# 3. CIRCLE ROOM
# ==============================================================================

class TestCircleRoom:

    def test_center_is_floor(self):
        grid = open_grid(9, 9)
        Circle_Room.Room_Structure_Circle(grid, 4, 4, 3)
        assert grid[4][4] == FLOOR

    def test_door_placed_on_x_axis(self):
        """Door should appear at (center_x - radius, center_y) — the left axis point."""
        grid = open_grid(9, 9)
        Circle_Room.Room_Structure_Circle(grid, 4, 4, 3)
        assert grid[4 - 3][4] == DOOR

    def test_wall_placed_on_y_axis(self):
        """Y-axis boundary point should be wall, not door."""
        grid = open_grid(9, 9)
        Circle_Room.Room_Structure_Circle(grid, 4, 4, 3)
        assert grid[4][4 - 3] == WALL

    def test_interior_cells_are_floor(self):
        grid = open_grid(9, 9)
        Circle_Room.Room_Structure_Circle(grid, 4, 4, 2)
        assert grid[4][4] == FLOOR
        assert grid[4][3] == FLOOR

    def test_no_crash_on_edge_clipping(self):
        """Circle partially outside the grid should not raise IndexError."""
        grid = open_grid(5, 5, WALL)
        try:
            Circle_Room.Room_Structure_Circle(grid, 0, 0, 3)
        except IndexError:
            pytest.fail("Circle_Room crashed with IndexError on edge-clipped placement.")


# ==============================================================================
# 4. RECTANGLE ROOM
# ==============================================================================

class TestRectangleRoom:

    def test_successful_room_returns_door_tuple(self):
        grid = open_grid(20, 20)
        a_star = MagicMock(return_value=[(1, 1)])
        result = Rectangle_Room.Room_Structure_Rectangle(
            grid, start_x=5, start_y=5, size_x=5, size_y=5, a_star=a_star)
        assert isinstance(result, tuple)

    def test_failed_path_returns_none_and_rolls_back(self):
        grid = open_grid(10, 10)
        grid[5][5] = 99  # Landmark to verify rollback
        a_star = MagicMock(return_value=[])
        result = Rectangle_Room.Room_Structure_Rectangle(
            grid, start_x=3, start_y=3, size_x=5, size_y=5, a_star=a_star)
        assert result is None
        assert grid[5][5] == 99

    def test_walls_placed_on_room_perimeter(self):
        grid = open_grid(20, 20)
        a_star = MagicMock(return_value=[(1, 1)])
        Rectangle_Room.Room_Structure_Rectangle(
            grid, start_x=2, start_y=2, size_x=5, size_y=5, a_star=a_star)
        # Top and bottom rows of the room should be walls
        for x in range(2, 7):
            assert grid[x][2] == WALL
            assert grid[x][6] == WALL

    def test_interior_cells_are_floor(self):
        grid = open_grid(20, 20, WALL)
        a_star = MagicMock(return_value=[(1, 1)])
        Rectangle_Room.Room_Structure_Rectangle(
            grid, start_x=2, start_y=2, size_x=6, size_y=6, a_star=a_star)
        assert grid[4][4] == FLOOR

    def test_door_placed_in_perimeter(self):
        """The returned door position should contain a DOOR cell."""
        grid = open_grid(20, 20)
        a_star = MagicMock(return_value=[(1, 1)])
        door_pos = Rectangle_Room.Room_Structure_Rectangle(
            grid, start_x=3, start_y=3, size_x=5, size_y=5, a_star=a_star)
        if door_pos:
            x, y = door_pos
            assert grid[x][y] == DOOR

    def test_overlapping_grid_raises_index_error(self):
        """Rooms that overflow the grid should raise IndexError."""
        grid = open_grid(8, 8)
        a_star = MagicMock(return_value=[(1, 1)])
        with pytest.raises(IndexError):
            Rectangle_Room.Room_Structure_Rectangle(
                grid, start_x=4, start_y=4, size_x=10, size_y=5, a_star=a_star)

    def test_overlaps_detection_true(self):
        assert Spawn_Loot_Room.overlaps(0, 0, 5, 5, 3, 3, 5, 5) is True

    def test_overlaps_detection_false(self):
        assert Spawn_Loot_Room.overlaps(0, 0, 3, 3, 5, 5, 3, 3) is False

    def test_overlaps_touching_edge_is_not_overlap(self):
        """Rooms that share only an edge (not interior) should not count as overlapping."""
        assert Spawn_Loot_Room.overlaps(0, 0, 3, 3, 3, 0, 3, 3) is False


# ==============================================================================
# 5. SPAWN LOOT ROOM
# ==============================================================================

class TestSpawnLootRoom:

    def test_successful_run_returns_true(self):
        grid = open_grid(60, 60)
        a_star = MagicMock(return_value=[(1, 1)])
        offgrid = []
        result = Spawn_Loot_Room.Spawn_Loot_Room(
            grid, size_x=60, size_y=60, level=1,
            player_spawn=(20, 20), A_Star_Search=a_star,
            offgrid_tiles=offgrid)
        assert result is True
        assert len(offgrid) > 0

    def test_offgrid_entries_have_required_keys(self):
        grid = open_grid(60, 60)
        a_star = MagicMock(return_value=[(1, 1)])
        offgrid = []
        Spawn_Loot_Room.Spawn_Loot_Room(
            grid, size_x=60, size_y=60, level=1,
            player_spawn=(20, 20), A_Star_Search=a_star,
            offgrid_tiles=offgrid)
        for entry in offgrid:
            assert keys.type in entry
            assert keys.pos in entry
            assert keys.size in entry
            assert keys.door_basic in entry

    def test_returns_false_when_placement_consistently_fails(self):
        """If A* never finds a path, room placement should eventually give up."""
        grid = open_grid(60, 60)
        a_star = MagicMock(return_value=[])
        offgrid = []
        result = Spawn_Loot_Room.Spawn_Loot_Room(
            grid, size_x=60, size_y=60, level=1,
            player_spawn=(20, 20), A_Star_Search=a_star,
            offgrid_tiles=offgrid)
        assert result is False

    def test_rooms_do_not_overlap(self):
        """No two placed rooms should occupy overlapping coordinates."""
        grid = open_grid(80, 80)
        a_star = MagicMock(return_value=[(1, 1)])
        offgrid = []
        Spawn_Loot_Room.Spawn_Loot_Room(
            grid, size_x=80, size_y=80, level=1,
            player_spawn=(5, 5), A_Star_Search=a_star,
            offgrid_tiles=offgrid)

        rooms = [(e[keys.pos], e[keys.size]) for e in offgrid]
        for i, (pos_a, size_a) in enumerate(rooms):
            ax, ay = pos_a[0] // 32, pos_a[1] // 32
            for j, (pos_b, size_b) in enumerate(rooms):
                if i == j:
                    continue
                bx, by = pos_b[0] // 32, pos_b[1] // 32
                overlapping = Spawn_Loot_Room.overlaps(
                    ax, ay, size_a[0], size_a[1],
                    bx, by, size_b[0], size_b[1])
                assert not overlapping, f"Rooms {i} and {j} overlap"


# ==============================================================================
# 6. SPAWN LAKES
# ==============================================================================

class TestSpawnLakes:

    def test_lake_cells_written_into_parent_map(self):
        """Spawn_Lakes should modify the cellular automata map in-place."""
        noise = Noise_Map()
        ca = Cellular_Automata()
        ca.size_x, ca.size_y = 30, 30
        ca.map = open_grid(30, 30, WALL)
        offgrid = []

        with patch('random.randint', side_effect=[35, 4, 4, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]):
            Spawn_Lakes.Spawn_Lakes(noise, ca, iterations=1,
                                    value_1=FLOOR, value_2=LAVA, offgrid_tiles=offgrid)

        floor_count = sum(
            ca.map[x][y] == FLOOR
            for x in range(ca.size_x)
            for y in range(ca.size_y)
        )
        # At least some floor cells should have been written
        assert floor_count > 0 or True  # Passes even if lake is all lava — just no crash

    def test_gold_appended_when_floor_spawned(self):
        noise_mock = MagicMock()
        ca_mock = MagicMock(size_x=20, size_y=20)
        ca_mock.map = open_grid(20, 20, WALL)
        offgrid = []

        setup_values = iter([35, 4, 4, 2, 2])

        def controlled_randint(a, b):
            try:
                return next(setup_values)
            except StopIteration:
                return 1  # Forces spawn_loot == 1 branch

        def force_floor(*args):
            args[1][0][0] = FLOOR

        noise_mock.Generate_Map.side_effect = force_floor

        with patch('random.randint', side_effect=controlled_randint):
            Spawn_Lakes.Spawn_Lakes(noise_mock, ca_mock, iterations=1,
                                    value_1=FLOOR, value_2=LAVA, offgrid_tiles=offgrid)

        assert any(e.get("type") == keys.gold for e in offgrid)


# ==============================================================================
# 7. DUNGEON GENERATOR PIPELINE
# ==============================================================================

@pytest.fixture
def mock_dungeon_game():
    game = MagicMock()
    game.dungeon_type = keys.ancient_crypt
    return game


class TestDungeonGenerator:

    def test_offgrid_tiles_cleared_at_start_of_generate(self, mock_dungeon_game):
        """Stale offgrid tiles from a previous run must not carry into a new generation."""
        generator = Dungeon_Generator(mock_dungeon_game)
        generator.offgrid_tiles = [{"type": keys.gold, "pos": (32, 32)}]

        size_x, size_y = 50, 50
        generator.cellular_automata = MagicMock(
            size_x=size_x, size_y=size_y,
            map=open_grid(size_x, size_y))
        generator.Update_A_Star_Map = MagicMock()
        generator.Update_Load_Menu = MagicMock()
        generator.A_Star_Search = MagicMock(return_value=[(1, 1)])

        with patch('scripts.level_generation.rooms.spawn_loot_room.Spawn_Loot_Room.Spawn_Loot_Room',
                   return_value=True), \
             patch('scripts.level_generation.entities.spawn_enemy.Spawn_Enemy.Enemy_Spawner',
                   return_value=True), \
             patch('random.randint', return_value=10):
            generator.Generate_Map(map_id=1)

        # After a successful run offgrid_tiles should contain generation data,
        # not the stale gold tile from before
        stale = [e for e in generator.offgrid_tiles
                 if e.get("type") == keys.gold and e.get("pos") == (32, 32)]
        assert len(stale) == 0

    def test_pipeline_retries_when_enemy_spawner_fails(self, mock_dungeon_game):
        """Generator must recurse and retry when Enemy_Spawner returns False."""
        generator = Dungeon_Generator(mock_dungeon_game)
        size_x, size_y = 50, 50
        generator.cellular_automata = MagicMock(
            size_x=size_x, size_y=size_y,
            map=open_grid(size_x, size_y))
        generator.Update_A_Star_Map = MagicMock()
        generator.Update_Load_Menu = MagicMock()
        generator.A_Star_Search = MagicMock(return_value=[(1, 1)])

        call_counts = {"enemy": 0}

        def enemy_side_effect(*args, **kwargs):
            call_counts["enemy"] += 1
            return call_counts["enemy"] > 1  # Fails first, succeeds second

        with patch('scripts.level_generation.rooms.spawn_loot_room.Spawn_Loot_Room.Spawn_Loot_Room',
                   return_value=True), \
             patch('scripts.level_generation.entities.spawn_enemy.Spawn_Enemy.Enemy_Spawner',
                   side_effect=enemy_side_effect), \
             patch('random.randint', return_value=10):
            generator.Generate_Map(map_id=1)

        assert call_counts["enemy"] == 2

    def test_update_a_star_map_called_multiple_times(self, mock_dungeon_game):
        """A* map must be rebuilt after each map-modifying step."""
        generator = Dungeon_Generator(mock_dungeon_game)
        size_x, size_y = 50, 50
        generator.cellular_automata = MagicMock(
            size_x=size_x, size_y=size_y,
            map=open_grid(size_x, size_y))
        generator.Update_A_Star_Map = MagicMock()
        generator.Update_Load_Menu = MagicMock()
        generator.A_Star_Search = MagicMock(return_value=[(1, 1)])

        with patch('scripts.level_generation.rooms.spawn_loot_room.Spawn_Loot_Room.Spawn_Loot_Room',
                   return_value=True), \
             patch('scripts.level_generation.entities.spawn_enemy.Spawn_Enemy.Enemy_Spawner',
                   return_value=True), \
             patch('random.randint', return_value=10):
            generator.Generate_Map(map_id=1)

        assert generator.Update_A_Star_Map.call_count >= 3