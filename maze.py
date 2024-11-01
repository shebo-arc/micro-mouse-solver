import tkinter as tk
import astar
import dijkstra
import flood

# Directions for moving in the maze: Right, Down, Left, Up
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class MazeApp:
    def __init__(self, master, file_path, title, algorithm_func, cell_size=30):
        self.master = master
        self.master.title(title)  # Set window title
        self.algorithm_func = algorithm_func  # Algorithm function (A* or Dijkstra)
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

        # Run the algorithm and animate the solution
        path, visited_nodes = self.algorithm_func(self.start, self.end)
        if path:
            for current, neighbor, det in visited_nodes:
                if current in path:
                    self.color_cell(current[0], current[1], 'blue')
                else:
                    self.color_cell(current[0], current[1], 'cyan')
                if det == '1' and neighbor not in path:
                    self.color_cell(neighbor[0], neighbor[1], 'black')
                elif det == '0' and neighbor not in path:
                    self.color_cell(neighbor[0], neighbor[1], 'white')
                elif det == 'S' and neighbor not in path:
                    self.color_cell(neighbor[0], neighbor[1], 'red')
                elif det == 'E' and neighbor not in path:
                    self.color_cell(neighbor[0], neighbor[1], 'red')
        else:
            for current, neighbor, det in visited_nodes:
                self.color_cell(current[0], current[1], 'cyan')
                if det == '1':
                    self.color_cell(neighbor[0], neighbor[1], 'black')
                elif det == '0':
                    self.color_cell(neighbor[0], neighbor[1], 'white')
                elif det == 'S':
                    self.color_cell(neighbor[0], neighbor[1], 'red')
                elif det == 'E':
                    self.color_cell(neighbor[0], neighbor[1], 'red')


            #self.animate_path(path)'''

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
                if self.grid[r][c]=='S' or self.grid[r][c]=='E':
                    color = 'red'
                else:
                    color = 'yellow'

                self.canvas.create_rectangle(c * self.cell_size, r * self.cell_size,
                                             (c + 1) * self.cell_size, (r + 1) * self.cell_size,
                                             fill=color)

    def animate_path(self, path, color):
        """Animate the drawing of the path."""
        for i, (row, col) in enumerate(path):
            self.master.after(i * 100, self.color_cell, row, col, color)

    def color_cell(self, row, col, color):
        """Color a specific cell."""
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        if color == 'blue':
            outline = 'gray'
        else:
            outline = 'black'
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=outline)

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
    # Path to the text file containing the maze structure
    maze_path = 'grid.txt'

    # First window for A* algorithm
    '''root_astar = tk.Tk()
    astar_app = MazeApp(root_astar, maze_path, "A* Algorithm", astar.run_astar)

    # Second window for Dijkstra algorithm
    root_dijkstra = tk.Tk()
    dijkstra_app = MazeApp(root_dijkstra, maze_path, "Dijkstra Algorithm", dijkstra.run_dijkstra)'''

    # Third window for Flood fill algorithm
    root_flood = tk.Tk()
    flood_app = MazeApp(root_flood, maze_path, "Flood Fill Algorithm", flood.flood_fill)

    # Start both Tkinter windows
    #root_astar.mainloop()
    #root_dijkstra.mainloop()
    root_flood.mainloop()