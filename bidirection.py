import sensor

# Directions for moving in the maze: Right, Down, Left, Up
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def bidirectional_search(start, goal):
    """Bidirectional search to find a path from start to goal in the maze."""
    # Initialize the forward and backward searches
    forward_search = {start: None}
    backward_search = {goal: None}
    forward_queue = [start]
    backward_queue = [goal]

    # Dictionaries to store the path
    came_from_forward = {}
    came_from_backward = {}

    # List to store each current node and the neighbors examined
    visited_nodes = []

    while forward_queue and backward_queue:
        # Explore nodes in the forward direction
        current = forward_queue.pop(0)
        for direction in DIRECTIONS:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            det = sensor.wall(current, direction)

            # Record the current node, its neighbor, and the wall detection value
            if det is not None:
                visited_nodes.append((current, neighbor, det))

                if det != '1':  # If there's no wall
                    if neighbor not in forward_search:
                        forward_search[neighbor] = current
                        forward_queue.append(neighbor)
                        came_from_forward[neighbor] = current

                    # Check if the search from start and goal meet
                    if neighbor in backward_search:
                        # Check if the meeting point is valid
                        if sensor.wall(neighbor, (0, 0)) != '1':
                            # Add the meeting point and its four neighbors to the visited nodes list
                            for dire in DIRECTIONS:
                                neighbor_neighbor = (neighbor[0] + dire[0], neighbor[1] + dire[1])
                                det_neighbor = sensor.wall(neighbor, dire)
                                visited_nodes.append((neighbor, neighbor_neighbor, det_neighbor))

                            # Reconstruct the path using the forward and backward searches
                            path = reconstruct_path(came_from_forward, came_from_backward, neighbor)
                            return path, visited_nodes
                        else:
                            return None, visited_nodes

        # Explore nodes in the backward direction
        current = backward_queue.pop(0)
        for direction in DIRECTIONS:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            det = sensor.wall(current, direction)

            # Record the current node, its neighbor, and the wall detection value
            if det is not None:
                visited_nodes.append((current, neighbor, det))

                if det != '1':  # If there's no wall
                    if neighbor not in backward_search:
                        backward_search[neighbor] = current
                        backward_queue.append(neighbor)
                        came_from_backward[neighbor] = current

                    # Check if the search from start and goal meet
                    if neighbor in forward_search:
                        # Check if the meeting point is valid
                        if sensor.wall(neighbor, direction) != '1':
                            # Add the meeting point and its four neighbors to the visited nodes list
                            for dire in DIRECTIONS:
                                neighbor_neighbor = (neighbor[0] + dire[0], neighbor[1] + dire[1])
                                det_neighbor = sensor.wall(neighbor, dire)
                                visited_nodes.append((neighbor, neighbor_neighbor, det_neighbor))

                            # Reconstruct the path using the forward and backward searches
                            path = reconstruct_path(came_from_forward, came_from_backward, neighbor)
                            return path, visited_nodes
                        else:
                            return None, visited_nodes

    return None, visited_nodes  # Return None if no path is found, along with the visited nodes


def reconstruct_path(came_from_forward, came_from_backward, meeting_point):
    """Reconstruct the path from the start to the goal."""
    # Reconstruct the path using the forward search
    path_forward = []
    current = meeting_point
    while current is not None:
        path_forward.append(current)
        current = came_from_forward.get(current)
    path_forward.reverse()

    # Reconstruct the path using the backward search
    path_backward = []
    current = meeting_point
    while current is not None:
        path_backward.append(current)
        current = came_from_backward.get(current)

    # Combine the two paths
    path = path_forward + path_backward[1:]
    path.pop()
    path.pop(0)

    '''
    # Print the forward search path, backward search path, and the meeting point
    print("Forward search path:", path_forward)
    print("Backward search path:", path_backward)
    print("Meeting point:", meeting_point)
    print("Path:", path)
    '''

    return path


def run_bidirectional_search(start, end):
    if start and end:
        # Run bidirectional search to find the shortest path
        path, visited_nodes = bidirectional_search(start, end)

        if path:
            print("Path found using bidirectional search")
            # print("Visited nodes and neighbors examined:")
            # for current, neighbor, det in visited_nodes:
            #    print(f"Current: {current}, Neighbor: {neighbor}, Det: {det}")
            return path, visited_nodes
        else:
            print("No path found.")
            return None
    else:
        print("Start or end point not found in the maze.")
        return None
