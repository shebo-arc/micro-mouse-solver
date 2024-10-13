import tkinter as tk
import random

class MazeApp:
    def __init__(self, root, width=10, height=10, cell_size=40):
        self.root = root
        self.width = width  # Number of columns in the maze
        self.height = height  # Number of rows in the maze
        self.cell_size = cell_size  # Size of each cell in pixels
        self.canvas = tk.Canvas(root, width=width * cell_size, height=height * cell_size)
        self.canvas.pack()
        self.grid = []
        self.create_maze_grid()
        self.draw_maze()
        self.draw_random_path()

    def create_maze_grid(self):
        """Create a simple maze grid (can be customized for complex mazes)."""
        # Initializing the maze with 0 for open spaces and 1 for walls.
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        # Adding random walls to make it a simple maze
        for i in range(self.height):
            for j in range(self.width):
                if random.choice([0, 1]) == 1:
                    self.grid[i][j] = 1  # Mark as a wall

    def draw_maze(self):
        """Draw the maze on the canvas."""
        for row in range(self.height):
            for col in range(self.width):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = "black" if self.grid[row][col] == 1 else "white"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def draw_random_path(self):
        """Draw a random path in the maze by coloring one brick after another."""
        path = self.generate_random_path()
        self.animate_path(path)

    def generate_random_path(self):
        """Generate a random path through the maze."""
        path = []
        # Start at the top-left corner (0, 0)
        current_pos = (0, 0)
        path.append(current_pos)

        while current_pos != (self.height - 1, self.width - 1):  # Until reaching bottom-right corner
            row, col = current_pos
            # Choose a random direction to move (right, down)
            possible_moves = []
            if row + 1 < self.height and self.grid[row + 1][col] == 0:
                possible_moves.append((row + 1, col))
            if col + 1 < self.width and self.grid[row][col + 1] == 0:
                possible_moves.append((row, col + 1))

            if not possible_moves:
                break  # No more possible moves
            current_pos = random.choice(possible_moves)
            path.append(current_pos)

        return path

    def animate_path(self, path):
        """Animate the drawing of the path."""
        for i, (row, col) in enumerate(path):
            self.root.after(i * 100, self.color_cell, row, col, "blue")

    def color_cell(self, row, col, color):
        """Color a specific cell."""
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")


# Initialize the Tkinter application
root = tk.Tk()
app = MazeApp(root)
root.mainloop()
