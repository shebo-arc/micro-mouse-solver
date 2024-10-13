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
        self.draw_maze()

        # Find start and end points
        self.start, self.end = self.find_start_and_end()

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

    def draw_path(self,file_path):
        """Draw the solution path on the Tkinter canvas."""
        for (r, c) in file_path:
            if self.grid[r][c] != 'S' and self.grid[r][c] != 'E':  # Keep S and E red
                self.canvas.create_rectangle(c * self.cell_size, r * self.cell_size,
                                             (c + 1) * self.cell_size, (r + 1) * self.cell_size,
                                             fill='blue')  # Path will be blue
    def animate_path(self, path):
        """Animate the drawing of the path."""
        for i, (row, col) in enumerate(path):
            self.master.after(i * 100, self.color_cell, row, col, "blue")

    def color_cell(self, row, col, color):
        """Color a specific cell."""
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

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


if __name__ == "__main__":
    root = tk.Tk()

    # Path to the text file containing the maze structure
    file_path = 'grid.txt'

    app = MazeApp(root, file_path)
    path = astar.run_astar(app.grid, app.start, app.end)
    app.animate_path(path)
    root.mainloop()
