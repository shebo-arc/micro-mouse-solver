import heapq

# Directions for moving in the maze: Right, Down, Left, Up
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def heuristic(a, b):
    """Calculate the Manhattan distance between two points."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(maze, start, goal):
    """A* algorithm to find the shortest path from start to goal in the maze."""
    rows, cols = len(maze), len(maze[0])

    # Priority queue (min-heap) for A* search
    open_set = []
    heapq.heappush(open_set, (0, start))  # (priority, (row, col))

    # Dictionaries to store the cost and path
    g_score = {start: 0}
    came_from = {}

    while open_set:
        # Get the node with the lowest f_score
        _, current = heapq.heappop(open_set)

        # If the goal is reached, reconstruct the path
        if current == goal:
            return reconstruct_path(came_from, current)

        # Explore neighbors
        for direction in DIRECTIONS:
            neighbor = (current[0] + direction[0], current[1] + direction[1])

            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and maze[neighbor[0]][neighbor[1]] != '1':
                # Calculate g score for the neighbor
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    # This path to neighbor is better
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, neighbor))

    return None  # Return None if no path is found


def reconstruct_path(came_from, current):
    """Reconstruct the path from the goal to the start."""
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.reverse()
    path.pop()
    return path


def run_astar(maze, start, end):
    if start and end:
        # Run A* algorithm to find the shortest path
        path = astar(maze, start, end)

        if path:
            print("Path found in a star")
            return path
        else:
            print("No path found.")
            return None
    else:
        print("Start or end point not found in the maze.")
        return None