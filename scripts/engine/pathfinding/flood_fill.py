from collections import deque
from .directions import DIAGONAL

def flood_distances(grid, start, directions=DIAGONAL, max_steps=None):
    """BFS over grid[x][y] == 0 cells. Returns {(x, y): steps_from_start}.
    Empty dict if start is out of bounds or blocked."""
    start = (start[0], start[1])  # accept lists, always hash as a tuple
    width = len(grid)
    height = len(grid[0]) if width else 0
    sx, sy = start
    if not (0 <= sx < width and 0 <= sy < height) or grid[sx][sy] != 0:
        return {}

    dist = {start: 0}
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        steps = dist[(x, y)]
        if max_steps is not None and steps >= max_steps:
            continue
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height \
                    and grid[nx][ny] == 0 and (nx, ny) not in dist:
                dist[(nx, ny)] = steps + 1
                queue.append((nx, ny))
    return dist


def flood_reachable(grid, start, directions=DIAGONAL):
    return set(flood_distances(grid, start, directions))


def label_regions(grid, directions=DIAGONAL):
    """Returns (labels, sizes): labels[(x, y)] is a region id, sizes[id] its cell count."""
    labels, sizes = {}, []
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == 0 and (x, y) not in labels:
                cells = flood_distances(grid, (x, y), directions)
                for cell in cells:
                    labels[cell] = len(sizes)
                sizes.append(len(cells))
    return labels, sizes