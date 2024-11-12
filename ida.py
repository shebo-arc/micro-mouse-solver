import sensor

# Directions for moving in the maze: Right, Down, Left, Up
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def heuristic(a, b):
    """Calculate the Manhattan distance between two points."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def ida_star(start, goal):
    """IDA* algorithm to find the shortest path from start to goal in the maze."""
    threshold = heuristic(start, goal)
    path = [start]
    visited_nodes = []  # Use a list for visited nodes to store (current, neighbor, det)

    while True:
        result, new_threshold = search(start, goal, threshold, path, visited_nodes)
        if result is not None:
            return result, visited_nodes
        if new_threshold == float('inf'):
            return None, visited_nodes
        threshold = new_threshold

def search(node, goal, threshold, path, visited_nodes):
    """Recursive helper function for IDA*."""
    f_score = len(path) - 1 + heuristic(node, goal)  # Exclude start node from path length
    if f_score > threshold:
        return None, f_score
    if node == goal:
        return path, None

    min_threshold = float('inf')

    for direction in DIRECTIONS:
        neighbor = (node[0] + direction[0], node[1] + direction[1])
        det = sensor.wall(node, direction)

        if det is not None:
            # Record the current node and its neighbor along with wall detection result
            visited_nodes.append((node, neighbor, det))

            if det != '1' and neighbor not in path:  # If there's no wall and not part of current path
                new_path = path + [neighbor]
                result, new_threshold = search(neighbor, goal, threshold, new_path, visited_nodes)
                if result is not None:
                    return result, None
                min_threshold = min(min_threshold, new_threshold)

            # No need to pop; keep all visited nodes in the list

    return None, min_threshold

def run_ida_star(start, end):
    if start and end:
        # Run IDA* algorithm to find the shortest path
        path, visited_nodes = ida_star(start, end)

        if path:
            print("Path found in IDA*")
            return path, visited_nodes
        else:
            print("No path found.")
            return None
    else:
        print("Start or end point not found in the maze.")
        return None
