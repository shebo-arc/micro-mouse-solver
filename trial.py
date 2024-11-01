from collections import deque

# BFS to fill the grid with distances
def fill_distances(start,end):
    # Initial grid setup with "S" and "E" and walls marked as -1
    rows, cols = 20, 20
    grid = [[-1 for _ in range(rows)] for _ in range(cols)]  # Unexplored cells

    n, m = len(grid), len(grid[0])
    queue = deque([(end, 0)])  # Queue of (position, distance)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        (x, y), dist = queue.popleft()

        # Update distance for the cell
        grid[x][y] = dist

        # Explore neighbors
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and grid[nx][ny] == -1:
                queue.append(((nx, ny), dist + 1))

    # Print the result
    for row in grid:
        print(" ".join(map(str, row)))


# Fill distances starting from "E"
start = (0, 0)
exit_pos = (9, 9)
fill_distances(start, exit_pos)
