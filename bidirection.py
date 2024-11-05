import heapq
import sensor

# Directions for moving in the maze: Right, Down, Left, Up
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def heuristic(a, b):
    """Calculate the Manhattan distance between two points."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def bidirectional_search(start, end):
    """Bidirectional search to find the shortest path from start to end in the maze."""
    # Initialize the search from both directions
    forward_open_set = []
    heapq.heappush(forward_open_set, (0, start))
    forward_g_score = {start: 0}
    forward_came_from = {}

    backward_open_set = []
    heapq.heappush(backward_open_set, (0, end))
    backward_g_score = {end: 0}
    backward_came_from = {}

    forward_visited_nodes = []
    backward_visited_nodes = []

    while forward_open_set and backward_open_set:
        # Expand the forward search
        _, forward_current = heapq.heappop(forward_open_set)
        for direction in DIRECTIONS:
            forward_neighbor = (forward_current[0] + direction[0], forward_current[1] + direction[1])
            forward_det = sensor.wall(forward_current, direction)

            if forward_det is not None:
                forward_visited_nodes.append((forward_current, forward_neighbor, forward_det))

                if forward_det != '1':  # If there's no wall
                    tentative_g_score = forward_g_score[forward_current] + 1
                    if forward_neighbor not in forward_g_score or tentative_g_score < forward_g_score[forward_neighbor]:
                        forward_came_from[forward_neighbor] = forward_current
                        forward_g_score[forward_neighbor] = tentative_g_score
                        f_score = tentative_g_score + heuristic(forward_neighbor, end)
                        heapq.heappush(forward_open_set, (f_score, forward_neighbor))

        # Expand the backward search
        _, backward_current = heapq.heappop(backward_open_set)
        for direction in DIRECTIONS:
            backward_neighbor = (backward_current[0] + direction[0], backward_current[1] + direction[1])
            backward_det = sensor.wall(backward_current, direction)

            if backward_det is not None:
                backward_visited_nodes.append((backward_current, backward_neighbor, backward_det))

                if backward_det != '1':  # If there's no wall
                    tentative_g_score = backward_g_score[backward_current] + 1
                    if backward_neighbor not in backward_g_score or tentative_g_score < backward_g_score[
                        backward_neighbor]:
                        backward_came_from[backward_neighbor] = backward_current
                        backward_g_score[backward_neighbor] = tentative_g_score
                        f_score = tentative_g_score + heuristic(backward_neighbor, start)
                        heapq.heappush(backward_open_set, (f_score, backward_neighbor))

        # Check if the forward and backward searches have met
        meeting_point = None
        min_total_path = float('inf')

        # Find the meeting point that gives the shortest total path
        for forward_node in forward_g_score:
            if forward_node in backward_g_score:
                total_path_length = forward_g_score[forward_node] + backward_g_score[forward_node]
                if total_path_length < min_total_path:
                    min_total_path = total_path_length
                    meeting_point = forward_node

        if meeting_point:
            print("\nMeeting point found:", meeting_point)
            print("Forward g_score:", forward_g_score[meeting_point])
            print("Backward g_score:", backward_g_score[meeting_point])
            path = reconstruct_bidirectional_path(forward_came_from, backward_came_from, meeting_point)
            return path, forward_visited_nodes + backward_visited_nodes

    return None, forward_visited_nodes + backward_visited_nodes  # Return None if no path is found


def reconstruct_bidirectional_path(forward_came_from, backward_came_from, meeting_point):
    """Reconstruct the path from the start to the goal using the information from both forward and backward searches."""
    # Reconstruct the path from start to meeting point
    forward_path = []
    current = meeting_point
    while current in forward_came_from:
        forward_path.append(current)
        current = forward_came_from[current]
    forward_path.append(current)  # Add the start point
    forward_path.reverse()  # Reverse to get path from start to meeting point

    print("\nForward path before combining:", forward_path)

    # Reconstruct the path from meeting point to goal
    backward_path = []
    current = meeting_point
    while current in backward_came_from:
        current = backward_came_from[current]
        backward_path.append(current)

    print("Backward path before combining:", backward_path)
    print("Meeting point:", meeting_point)

    # Combine the paths, making sure to include the meeting point
    final_path = forward_path[:-1] + [meeting_point] + backward_path
    print("Final combined path:", final_path)

    return final_path


def run_pathfinding(start, end):
    if start and end:
        print("\nStarting bidirectional search from", start, "to", end)
        # Run bidirectional search to find the shortest path
        path, visited_nodes = bidirectional_search(start, end)

        if path:
            print("\nPath found using bidirectional search")
            print("Final path returned:", path)
            # print("Visited nodes and neighbors examined:")
            # for current, neighbor, wall in visited_nodes:
            #    print(f"Current: {current}, Neighbor: {neighbor}, Wall: {wall}")
            return path, visited_nodes
        else:
            print("No path found.")
            return None
    else:
        print("Start or end point not found in the maze.")
        return None