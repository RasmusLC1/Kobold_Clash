import heapq
import math
from .directions import DIAGONAL

SQRT2 = math.sqrt(2)


def _octile(a, b):
    dx, dy = abs(a[0] - b[0]), abs(a[1] - b[1])
    return (dx + dy) + (SQRT2 - 2) * min(dx, dy)


def _manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star_search(grid, start, goal, directions=DIAGONAL):
    """grid[x][y] == 0 is passable. Returns a list of (x, y) cells, or [] if no path."""
    start, goal = (start[0], start[1]), (goal[0], goal[1])
    width = len(grid)
    height = len(grid[0]) if width else 0

    def is_open(x, y):
        return 0 <= x < width and 0 <= y < height and grid[x][y] == 0

    if not is_open(*start) or not is_open(*goal):
        return []
    if start == goal:
        return [start]

    heuristic = _octile if len(directions) > 4 else _manhattan
    g = {start: 0.0}
    parent = {start: start}
    closed = set()
    heap = [(heuristic(start, goal), start)]

    while heap:
        _, current = heapq.heappop(heap)
        if current == goal:
            return _trace_path(parent, goal)
        if current in closed:  # stale heap entry
            continue
        closed.add(current)

        cx, cy = current
        for dx, dy in directions:
            nxt = (cx + dx, cy + dy)
            if nxt in closed or not is_open(*nxt):
                continue
            step = 1.0 if dx == 0 or dy == 0 else SQRT2
            new_g = g[current] + step
            if new_g < g.get(nxt, float("inf")):
                g[nxt] = new_g
                parent[nxt] = current
                heapq.heappush(heap, (new_g + heuristic(nxt, goal), nxt))
    return []


def _trace_path(parent, goal):
    path = [goal]
    while parent[path[-1]] != path[-1]:
        path.append(parent[path[-1]])
    path.reverse()
    return path