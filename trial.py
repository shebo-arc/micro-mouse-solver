import tkinter as tk
import heapq
import astar

# Directions for moving in the maze: Right, Down, Left, Up
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class MazeApp:
    def __init__(self, master, file_path, cell_size=30):
        self.master = master
        self.cell_size = cell_size

        # Load the maze from a text file
        self.grid = self.load_maze(file_path)
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

        # Set up the canvas with the correct size
        self.canvas = tk.Canvas(master, width=self.cols * cell_size, height=self.rows * cell_size)
        self.canvas.pack()

        # Draw the initial maze
        self.draw_maze(self.start, self.end)

        # Find start and end points
        self.start, self.end = self.find_start_and_end()

        self.draw_path()

    '''
        # If both start and end are found, solve the maze using A*
        if self.start and self.end:
            path = self.astar(self.start, self.end)
            if path:
                self.draw_path(path)
                self.save_solution_to_file('solved_maze.txt', path)
            else:
                print("No path found.")
        else:
            print("Start or end point not found in the maze.")
    '''

    def load_maze(self, file_path):
        """Load the maze from a text file."""
        with open(file_path, 'r') as file:
            maze = [list(line.strip()) for line in file.readlines()]  # Read as list of characters
        return maze

    def draw_maze(self):
        """Draw the maze on the Tkinter canvas."""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == '1':
                    color = 'black'  # Wall
                elif self.grid[r][c] == '0':
                    color = 'white'  # Path
                elif self.grid[r][c] == 'S':
                    color = 'red'  # Start point
                elif self.grid[r][c] == 'E':
                    color = 'red'  # End point

                self.canvas.create_rectangle(c * self.cell_size, r * self.cell_size,
                                             (c + 1) * self.cell_size, (r + 1) * self.cell_size,
                                             fill=color)

    def draw_path(self):
        """Draw the solution path on the Tkinter canvas."""
        path = astar.astar(maze, start, end)
        for (r, c) in path:
            if self.grid[r][c] != 'S' and self.grid[r][c] != 'E':  # Keep S and E red
                self.canvas.create_rectangle(c * self.cell_size, r * self.cell_size,
                                             (c + 1) * self.cell_size, (r + 1) * self.cell_size,
                                             fill='blue')  # Path will be blue

'''
    def find_start_and_end(self):
        """Find the start (S) and end (E) points in the maze."""
        start = None
        end = None
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c] == 'S':
                    start = (r, c)
                elif self.grid[r][c] == 'E':
                    end = (r, c)
        return start, end

    def heuristic(self, a, b):
        """Calculate the Manhattan distance between two points."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def astar(self, start, goal):
        """A* algorithm to find the shortest path from start to goal in the maze."""
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
                return self.reconstruct_path(came_from, current)

            # Explore neighbors
            for direction in DIRECTIONS:
                neighbor = (current[0] + direction[0], current[1] + direction[1])

                if (0 <= neighbor[0] < self.rows and 0 <= neighbor[1] < self.cols and
                        self.grid[neighbor[0]][neighbor[1]] != '1'):  # Check if not a wall
                    tentative_g_score = g_score[current] + 1

                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score = tentative_g_score + self.heuristic(neighbor, goal)
                        heapq.heappush(open_set, (f_score, neighbor))

        return None  # Return None if no path is found

    def reconstruct_path(self, came_from, current):
        """Reconstruct the path from the goal to the start."""
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    def save_solution_to_file(self, output_file, path):
        """Save the maze with the solution path marked by '*' to a text file."""
        # Mark the path in the grid
        for (r, c) in path:
            if self.grid[r][c] != 'S' and self.grid[r][c] != 'E':
                self.grid[r][c] = '*'  # Mark the path with '*'

        # Write the modified maze to the output file
        with open(output_file, 'w') as f:
            for row in self.grid:
                f.write("".join(row) + "\n")
'''

if __name__ == "__main__":
    root = tk.Tk()

    # Path to the text file containing the maze structure
    file_path = 'grid.txt'

    app = MazeApp(root, file_path)
    root.mainloop()
