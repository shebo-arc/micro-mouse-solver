import tkinter as tk


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

        # Draw the maze
        self.draw_maze()

    def load_maze(self, file_path):
        """Load the maze from a text file."""
        with open(file_path, 'r') as file:
            maze = [list(line.strip()) for line in file.readlines()]  # Read as list of characters
        return maze

    def draw_maze(self):
        """Draw the maze on the Tkinter canvas."""
        for r in range(self.rows):
            for c in range(self.cols):
                # Set colors based on the character in the maze
                if self.grid[r][c] == '1':
                    color = 'orange'  # Wall
                elif self.grid[r][c] == '0':
                    color = '#FFFFF0'  # Path
                elif self.grid[r][c] == 'S':
                    color = 'cyan'  # Start point
                elif self.grid[r][c] == 'E':
                    color = 'cyan'  # End point

                # Draw the cell
                self.canvas.create_rectangle(c * self.cell_size, r * self.cell_size,
                                             (c + 1) * self.cell_size, (r + 1) * self.cell_size,
                                             fill=color)


if __name__ == "__main__":
    root = tk.Tk()

    # Path to the text file containing the maze structure
    file_path = 'grid.txt'

    app = MazeApp(root, file_path)
    root.mainloop()
