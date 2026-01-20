import math
import heapq
from scripts.engine.keys.keys import keys
FLOOR = 0
WALL = 1
LAVA = 2
DOOR = 3
TRAP = 4
BOSS_ROOM = 5


class A_Star:
    def __init__(self, game):
        # Parent coords and costs
        self.game = game
        self.parent_x = 0
        self.parent_y = 0
        self.f = float('inf')
        self.g = float('inf')
        self.h = 0

        # Offsets, dimensions
        self.min_x = 0
        self.min_y = 0
        self.width = 0   # number of cells in X dimension
        self.height = 0  # number of cells in Y dimension

        self.saved_data = {}

        # Various maps
        self.standard_map = []
        self.ignore_lava_map = []
        self.void_spawn_map = []
        self.custom_map = []
        self.map = []  # Will point to whichever map is in use

    # ========== CLEAR / SETUP ==========

    def Clear_Maps(self):
        self.standard_map.clear()
        self.ignore_lava_map.clear()
        self.void_spawn_map.clear()
        self.custom_map.clear()

    def Save_Data(self):
        self.saved_data['min_x'] = self.min_x
        self.saved_data['min_y'] = self.min_y
        self.saved_data['width'] = self.width
        self.saved_data['height'] = self.height
        self.saved_data['standard_map'] = self.standard_map 
        self.saved_data['ignore_lava_map'] = self.ignore_lava_map 
        self.saved_data['void_spawn_map'] = self.void_spawn_map 
        self.saved_data['custom_map'] = self.custom_map 
        self.saved_data['map'] = self.map 

    def Load_Data(self, data):
        self.min_x = data['min_x']
        self.min_y = data['min_y']
        self.width = data['width']
        self.height = data['height']
        self.standard_map = data['standard_map'] 
        self.ignore_lava_map = data['ignore_lava_map'] 
        self.void_spawn_map = data['void_spawn_map'] 
        self.custom_map = data['custom_map'] 
        self.map = data['map'] 

    def Setup_Custom_Map(self, custom_map, size_x, size_y):
        """
        custom_map is a 2D array in the form custom_map[x][y].
        size_x, size_y are its dimensions (width, height).
        We'll store converted values through map_conversion: self.custom_map[x][y].
        """
        map_conversion = {
            FLOOR: 0,
            WALL: 1,
            LAVA: 0,
            DOOR: 0,
            TRAP: 0,
            BOSS_ROOM: 0,
        }
        # Convert and copy the map using the conversion dictionary
        self.custom_map = [[map_conversion[val] for val in col] for col in custom_map]
        self.width = size_x
        self.height = size_y

    # def Update_Level_Configuration_Map(self, game):



    def Set_Map(self, which_map):
        """Select which map array (standard, ignore_lava, custom) to use for pathfinding."""
        if which_map == keys.standard:
            self.map = self.standard_map
        elif which_map == keys.ignore_lava:
            self.map = self.ignore_lava_map
        elif which_map == keys.void_spawn:
            self.map = self.void_spawn_map
        elif which_map == keys.custom:
            self.map = self.custom_map
        else:
            self.map = self.standard_map  # fallback

    def Setup_Map_From_Game(self, game):
        """
        Example function to build standard_map and ignore_lava_map
        from your game tilemap. We assume tilemap.Get_Pos() returns
        (x, y) for each tile, and we want map[x][y].
        """
        self.Extract_Map_Bounds(game)
        self.Build_Standard_Map(game)
        self.Build_IgnoreLava_Map(game)
        self.Build_Void_Spawn_Map(game)

    def Extract_Map_Bounds(self, game):
        """Determine min_x, max_x, min_y, max_y from the tile positions."""
        all_positions = game.tilemap.Get_Pos()  # each is (x, y)
        x_coords = [p[0] for p in all_positions]
        y_coords = [p[1] for p in all_positions]
        self.min_x, max_x = min(x_coords), max(x_coords)
        self.min_y, max_y = min(y_coords), max(y_coords)
        self.width = max_x - self.min_x + 1
        self.height = max_y - self.min_y + 1

    def Build_Standard_Map(self, game):
        """
        Create a 2D list standard_map[x][y].
        Mark passable tiles with 0 and blocked tiles with 1.
        """
        # Initialize everything as blocked = 1
        self.standard_map = [[1 for _ in range(self.height)] for _ in range(self.width)]

        # Fill passable tiles
        all_positions = game.tilemap.Get_Pos()
        for (x, y) in all_positions:
            map_x = x - self.min_x
            map_y = y - self.min_y
            if 0 <= map_x < self.width and 0 <= map_y < self.height:
                tile = game.tilemap.Current_Tile((x,y))
                if not tile:
                    continue

                tile_type = tile.sub_type
                if tile_type == keys.floor and not tile.trap:
                    self.standard_map[map_x][map_y] = 0

        

    def Build_IgnoreLava_Map(self, game):
        """
        Similar to Build_Standard_Map but ignoring Lava/Fire as blocked.
        """
        self.ignore_lava_map = [[1 for _ in range(self.height)] for _ in range(self.width)]

        all_positions = game.tilemap.Get_Pos()
        for (x, y) in all_positions:
            map_x = x - self.min_x
            map_y = y - self.min_y
            if 0 <= map_x < self.width and 0 <= map_y < self.height:
                tile_type = game.tilemap.Current_Tile_Type_Without_Offset((x, y))
                if tile_type and (tile_type == keys.floor or keys.lava_env in tile_type or keys.fire in tile_type):
                    self.ignore_lava_map[map_x][map_y] = 0

    def Build_Void_Spawn_Map(self, game):
        """
        Similar to Build_Standard_Map but ignoring Lava/Fire as blocked.
        """
        self.void_spawn_map = [[1 for _ in range(self.height)] for _ in range(self.width)]

        all_positions = game.tilemap.Get_Pos()
        for (x, y) in all_positions:
            map_x = x - self.min_x
            map_y = y - self.min_y
            if 0 <= map_x < self.width and 0 <= map_y < self.height:
                tile_type = game.tilemap.Current_Tile_Type_Without_Offset((x, y))
                if tile_type:
                    self.void_spawn_map[map_x][map_y] = 0

    # ========== UTILITY CHECKS ==========

    def is_valid(self, x, y):
        """Check that (x, y) is within the map bounds."""
        return (0 <= x < self.width) and (0 <= y < self.height)

    def is_unblocked(self, x, y):
        """Check if the cell is passable (0)."""
        return (self.map[x][y] == 0)

    def is_destination(self, x, y, dest):
        """Return True if (x, y) == dest = (dest_x, dest_y)."""
        return (x == dest[0] and y == dest[1])

    def calculate_h_value(self, x, y, dest):
        """Euclidean heuristic from (x, y) to (dest_x, dest_y)."""
        return math.sqrt((x - dest[0])**2 + (y - dest[1])**2)

    def trace_path(self, cell_details, dest):
        """
        Walk back through parents from dest to start.
        cell_details[x][y].parent_x and parent_y store the parent coords.
        Returns the path as a list of (x, y).
        """
        path = []
        node = (dest[0], dest[1])

        while True:
            path.append(node)
            px = cell_details[node[0]][node[1]].parent_x
            py = cell_details[node[0]][node[1]].parent_y
            if (px == node[0] and py == node[1]):
                break
            node = (px, py)

        path.reverse()
        return path

    # ========== A* IMPLEMENTATION ==========
    # Accepts coordinates in tile size, so downscaled to 1 : 16 scale
    def a_star_search(self, start, goal, which_map='standard'):
        """
        start, goal are (x, y) in map coordinates.
        which_map is 'standard', 'ignore_lava', or 'custom'.
        Returns the path as a list of (x, y), or empty list if no path.
        """
        self.Set_Map(which_map)


        sx, sy = start
        gx, gy = goal

        # Basic checks
        if not self.is_valid(sx, sy) or not self.is_valid(gx, gy):
            return []
        # print("VALID")
        if not self.is_unblocked(sx, sy) or not self.is_unblocked(gx, gy):
            return []
        # print("UNBLOCKED")
        if self.is_destination(sx, sy, goal):
            return [start]
        # print("DESTINATION")
        # Initialize "closed list" to mark visited
        closed_list = [[False]*self.height for _ in range(self.width)]

        # Build a 2D array of cell info (like parent_x, f, g, h)
        # cell_details[x][y] = A_Star()
        cell_details = [[A_Star(self.game) for _ in range(self.height)] for _ in range(self.width)]

        # Initialize the start cell
        cell_details[sx][sy].f = 0.0
        cell_details[sx][sy].g = 0.0
        cell_details[sx][sy].h = 0.0
        cell_details[sx][sy].parent_x = sx
        cell_details[sx][sy].parent_y = sy

        # Min-heap (priority queue) for the open list
        open_list = []
        heapq.heappush(open_list, (0.0, sx, sy))  # (f, x, y)

        # Directions: 8 neighbors (dx, dy)
        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1),
                     (-1, -1), (-1, 1), (1, -1), (1, 1)]

        while open_list:
            f_current, cx, cy = heapq.heappop(open_list)
            closed_list[cx][cy] = True

            # Explore neighbors
            for dx, dy in neighbors:
                nx, ny = cx + dx, cy + dy

                if self.is_valid(nx, ny) and not closed_list[nx][ny]:
                    if self.is_unblocked(nx, ny):
                        # If this neighbor is the destination
                        if self.is_destination(nx, ny, goal):
                            # Set its parent, then build the path
                            cell_details[nx][ny].parent_x = cx
                            cell_details[nx][ny].parent_y = cy
                            return self.trace_path(cell_details, goal)

                        # Otherwise, compute cost
                        # Straight moves cost 1, diagonal ~1.414
                        move_cost = 1.0 if (dx == 0 or dy == 0) else math.sqrt(2)
                        g_new = cell_details[cx][cy].g + move_cost
                        h_new = self.calculate_h_value(nx, ny, goal)
                        f_new = g_new + h_new

                        # If better, update cell details and push to heap
                        if cell_details[nx][ny].f > f_new:
                            cell_details[nx][ny].f = f_new
                            cell_details[nx][ny].g = g_new
                            cell_details[nx][ny].h = h_new
                            cell_details[nx][ny].parent_x = cx
                            cell_details[nx][ny].parent_y = cy

                            heapq.heappush(open_list, (f_new, nx, ny))

        # No path found
        return []


    def a_star_search_no_diagonals(self, start, goal, which_map=keys.standard):
        """
        A* search with only 4-directional movement (up, down, left, right).
        start, goal are (x, y) in map coordinates.
        which_map is 'standard', 'ignore_lava', or 'custom'.
        Returns the path as a list of (x, y), or empty list if no path.
        """
        self.Set_Map(which_map)

        sx, sy = start
        gx, gy = goal

        # Basic checks remain the same
        if not self.is_valid(sx, sy) or not self.is_valid(gx, gy):
            return []
        if not self.is_unblocked(sx, sy) or not self.is_unblocked(gx, gy):
            return []
        if self.is_destination(sx, sy, goal):
            return [start]

        closed_list = [[False]*self.height for _ in range(self.width)]
        cell_details = [[A_Star(self.game) for _ in range(self.height)] for _ in range(self.width)]

        # Initialize start cell (same as before)
        cell_details[sx][sy].f = 0.0
        cell_details[sx][sy].g = 0.0
        cell_details[sx][sy].h = 0.0
        cell_details[sx][sy].parent_x = sx
        cell_details[sx][sy].parent_y = sy

        open_list = []
        heapq.heappush(open_list, (0.0, sx, sy))

        # Modified directions: Only 4 neighbors (no diagonals)
        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while open_list:
            f_current, cx, cy = heapq.heappop(open_list)
            closed_list[cx][cy] = True

            for dx, dy in neighbors:
                nx, ny = cx + dx, cy + dy

                if self.is_valid(nx, ny) and not closed_list[nx][ny]:
                    if self.is_unblocked(nx, ny):
                        if self.is_destination(nx, ny, goal):
                            cell_details[nx][ny].parent_x = cx
                            cell_details[nx][ny].parent_y = cy
                            return self.trace_path(cell_details, goal)

                        # All moves now cost 1 (no diagonals)
                        move_cost = 1.0
                        g_new = cell_details[cx][cy].g + move_cost
                        h_new = self.calculate_h_value(nx, ny, goal)
                        f_new = g_new + h_new

                        if cell_details[nx][ny].f > f_new:
                            cell_details[nx][ny].f = f_new
                            cell_details[nx][ny].g = g_new
                            cell_details[nx][ny].h = h_new
                            cell_details[nx][ny].parent_x = cx
                            cell_details[nx][ny].parent_y = cy

                            heapq.heappush(open_list, (f_new, nx, ny))

        return []