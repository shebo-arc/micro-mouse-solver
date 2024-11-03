from collections import deque
import sensor


def fill_distances(end):
    rows, cols = 20, 20
    grid = [[-1 for _ in range(cols)] for _ in range(rows)]  # Unexplored cells

    n, m = len(grid), len(grid)
    queue = deque([(end, 0)])  # Queue of (position, distance)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        (x, y), dist = queue.popleft()

        grid[x][y] = dist  # Update distance for the cell

        # Explore neighbors
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and grid[nx][ny] == -1:
                queue.append(((nx, ny), dist + 1))
    return grid


def flood_fill(start, end):
    distances_grid = fill_distances(end)
    n, m = 20, 20  # Assuming a fixed grid size; adjust as needed
    queue = deque([start])  # Start from "S"
    visited = set()  # Track visited nodes
    visited.add(start)
    path = []  # Track the path taken
    visited_nodes = []  # To store all visited nodes and their neighbors

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    came_from = {}  # Track path taken for backtracking

    while queue:
        x, y = queue.popleft()

        # If we reach the end position, construct the path
        if (x, y) == end:
            return reconstruct_path(came_from, start, end), visited_nodes

        # Explore neighbors based on distance values
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < n and 0 <= ny < m:
                current_distance = distances_grid[x][y]
                det = sensor.wall((x, y), (dx, dy))
                visited_nodes.append(((x, y), (nx, ny), det))  # Record current node and neighbor with wall detection

                if det != '1':  # If it's not a wall
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny))
                        path.append((nx, ny))  # Add this cell to the path
                        came_from[(nx, ny)] = (x, y)  # Set the parent node

                    elif distances_grid[nx][ny] > current_distance + 1:
                        distances_grid[nx][ny] = current_distance + 1

    print("No path to 'E' found.")
    return None, visited_nodes


def reconstruct_path(came_from, start, end):
    """Reconstructs the path from start to end using the came_from mapping."""
    current = end
    path = []

    while current != start:
        path.append(current)
        current = came_from.get(current)
        if current is None:  # If there's no valid path back to start
            return None

    path.append(start)  # Add start position at the end of the path
    return path[::-1]  # Reverse to get path from start to end


def run_flood(start, end):
    # Perform flood fill to explore the maze and find a path
    path_found, visited_nodes = flood_fill(start, end)

    # Output results
    if path_found is not None:
        print("Path found using Flood fill")
        return path_found, visited_nodes
    else:
        print("No valid path found using Flood fill.")
