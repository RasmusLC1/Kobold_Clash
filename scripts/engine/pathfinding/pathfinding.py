from dataclasses import dataclass
from scripts.engine.keys.keys import keys
from .a_star import pathfinding_search
from .flood_fill import flood_distances, label_regions
from .directions import CARDINAL, DIAGONAL

FLOOR, WALL, LAVA, DOOR, TRAP, BOSS_ROOM = range(6)
CUSTOM_CONVERSION = {FLOOR: 0, WALL: 1, LAVA: 0, DOOR: 0, TRAP: 0, BOSS_ROOM: 0}

# One rule per map: a tile is passable if the rule returns True
MAP_RULES = {
    keys.standard: lambda t: t.type == keys.floor and not t.trap and not t.touching_wall,
    keys.ignore_lava: lambda t: not t.touching_wall and (
        t.type == keys.floor or keys.lava_env in t.type or keys.fire in t.type),
    keys.void_spawn: lambda t: t.type is not None,
}


@dataclass
class GridMap:
    cells: list          # cells[x][y], 0 = passable
    min_x: int = 0       # tile coordinate of cells[0][0]
    min_y: int = 0

    def to_local(self, pos):
        return (pos[0] - self.min_x, pos[1] - self.min_y)

    def to_tile(self, pos):
        return (pos[0] + self.min_x, pos[1] + self.min_y)


class Pathfinding:
    def __init__(self, game):
        self.game = game
        self.maps = {}

    # ---- setup ------------------------------------------------------------
    def Clear_Maps(self):
        self.maps.clear()

    def Setup_Map_From_Game(self):
        tilemap = self.game.tilemap
        positions = tilemap.Get_Pos()
        xs = [p[0] for p in positions]
        ys = [p[1] for p in positions]
        min_x, min_y = min(xs), min(ys)
        width, height = max(xs) - min_x + 1, max(ys) - min_y + 1

        for name, rule in MAP_RULES.items():
            cells = [[1] * height for _ in range(width)]
            for x, y in positions:
                tile = tilemap.Current_Tile((x, y))
                if tile and rule(tile):
                    cells[x - min_x][y - min_y] = 0
            self.maps[name] = GridMap(cells, min_x, min_y)

    def Setup_Custom_Map(self, custom_map):
        """custom_map[x][y] uses the FLOOR/WALL/... constants. Origin is (0, 0)."""
        cells = [[CUSTOM_CONVERSION[v] for v in col] for col in custom_map]
        self.maps[keys.custom] = GridMap(cells)

    def Save_Data(self):
        return {"maps": dict(self.maps)}

    def Load_Data(self, data):
        self.maps = dict(data["maps"])

    # ---- queries (all in tile coordinates) ------------------------------------
    def Find_Path(self, start, goal, which_map=keys.standard, diagonals=True):
        grid = self.maps[which_map]
        local = pathfinding_search(grid.cells, grid.to_local(start), grid.to_local(goal),
                              DIAGONAL if diagonals else CARDINAL)
        return [grid.to_tile(p) for p in local]

    def Has_Path(self, start, goal, which_map=keys.standard, diagonals=True):
        return bool(self.Find_Path(start, goal, which_map, diagonals))

    def Flood_Distances(self, start, which_map=keys.standard, diagonals=True, max_steps=None):
        grid = self.maps[which_map]
        dist = flood_distances(grid.cells, grid.to_local(start),
                               DIAGONAL if diagonals else CARDINAL, max_steps)
        return {grid.to_tile(p): d for p, d in dist.items()}

    def Flood_Reachable(self, start, which_map=keys.standard, diagonals=True):
        return set(self.Flood_Distances(start, which_map, diagonals))

    def Label_Regions(self, which_map=keys.standard, diagonals=True):
        grid = self.maps[which_map]
        labels, sizes = label_regions(grid.cells, DIAGONAL if diagonals else CARDINAL)
        return {grid.to_tile(p): r for p, r in labels.items()}, sizes