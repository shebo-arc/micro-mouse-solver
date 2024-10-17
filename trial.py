import numpy as np
import matplotlib.pyplot as plt
import time


class Mouse:
    def __init__(self, maze):
        self.maze = maze
        self.position = [0, 0]  # Starting at the top-left corner
        self.path = [tuple(self.position)]  # To store the path taken
        self.visited = set()  # To keep track of visited positions

    def move(self, new_position):
        # Update the position if it's valid
        if (0 <= new_position[0] < self.maze.shape[0] and
                0 <= new_position[1] < self.maze.shape[1] and
                self.maze[new_position[0], new_position[1]] == 0 and
                tuple(new_position) not in self.visited):
            self.position = new_position
            self.path.append(tuple(self.position))
            self.visited.add(tuple(self.position))

    def navigate(self):
        # Simple logic to navigate using depth-first search (DFS)
        stack = [self.position]  # Start with the initial position
        while stack:
            current = stack.pop()
            self.move(current)  # Move to the current position

            # Check if the mouse reached the exit (bottom-right corner)
            if self.position == [self.maze.shape[0] - 1, self.maze.shape[1] - 1]:
                break

            # Get potential moves (up, down, left, right)
            directions = [
                [current[0] - 1, current[1]],  # up
                [current[0] + 1, current[1]],  # down
                [current[0], current[1] - 1],  # left
                [current[0], current[1] + 1]  # right
            ]

            for new_position in directions:
                if (0 <= new_position[0] < self.maze.shape[0] and
                        0 <= new_position[1] < self.maze.shape[1] and
                        self.maze[new_position[0], new_position[1]] == 0 and
                        tuple(new_position) not in self.visited):
                    stack.append(new_position)  # Add valid moves to the stack

            time.sleep(0.2)  # Slow down the movement for visualization


def visualize_maze(maze, path):
    plt.imshow(maze, cmap='binary')
    for pos in path:
        plt.scatter(pos[1], pos[0], color='red')  # Mark the path in red
    plt.title('Mouse Path through Maze')
    plt.gca().invert_yaxis()  # Invert Y axis for proper orientation
    plt.show()


# Define a simple maze (0 = path, 1 = wall)
maze = np.array([
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
])

# Create a Mouse instance and navigate the maze
mouse = Mouse(maze)
mouse.navigate()
visualize_maze(maze, mouse.path)
