DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def wall(current, direction):
    with open('grid.txt', 'r') as file:
        maze = [list(line.strip()) for line in file.readlines()]  # Read as list of characters

    rows, cols = len(maze), len(maze[0])
    neighbor = (current[0] + direction[0], current[1] + direction[1])
    if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and maze[neighbor[0]][neighbor[1]] == '1':
        return '1'
    elif 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and maze[neighbor[0]][neighbor[1]] == '0':
        return '0'
    elif 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and maze[neighbor[0]][neighbor[1]] == 'S':
        return 'S'
    elif 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and maze[neighbor[0]][neighbor[1]] == 'E':
        return 'E'
    return None
