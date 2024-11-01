from collections import deque
import sensor


def fill_distances(end):
    # Initial grid setup with "S" and "E" and walls marked as -1
    rows, cols = 20, 20
    grid = [[-1 for _ in range(cols)] for _ in range(rows)]  # Unexplored cells

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
    return grid


# Flood fill function that navigates from "S" to "E" based on distance values
def flood_fill(start, end):
    distances_grid = fill_distances(end)
    n, m = 20, 20  # Assuming a fixed grid size; adjust as needed
    queue = deque([start])  # Start from "S"
    visited = set()  # Track visited nodes
    visited.add(start)
    path = []  # Track the path taken
    visited_nodes = []  # To store all visited nodes and their neighbors

    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        x, y = queue.popleft()

        # If we reach the end position, construct the path and print distances grid
        if (x, y) == end:
            print("Reached 'E'")
            return path + [(x, y)], visited_nodes

        # Explore neighbors based on distance values
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # Check if within bounds and not visited yet
            if 0 <= nx < n and 0 <= ny < m:
                current_distance = distances_grid[x][y]
                next_distance = distances_grid[nx][ny]

                # Check for wall using sensor module
                det = sensor.wall((x, y), (dx, dy))
                visited_nodes.append(((x, y), (nx, ny), det))  # Record current node and neighbor with wall detection

                # Move to next cell only if it's not a wall and has not been visited yet
                if det != '1':
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny))
                        path.append((nx, ny))  # Add this cell to the path

                    # If we find a wall but it's a valid cell in the distance grid,
                    # update its distance value if necessary.
                    elif next_distance >= current_distance:
                        distances_grid[nx][ny] = current_distance + 1

    # If we exit the loop without reaching "E"
    print("No path to 'E' found.")
    return None, visited_nodes

# Example usage:
# start = (start_x, start_y)
# end = (end_x, end_y)
# path_found, traversed_nodes_info = flood_fill(start, end)