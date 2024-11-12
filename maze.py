import tkinter as tk
import astar
import dijkstra
import flood
import ida
import time

# Directions for moving in the maze: Right, Down, Left, Up
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class MazeApp:
    def __init__(self, master, title, algorithm_func, cell_size=30):
        self.master = master
        self.master.title(title)  # Set window title
        self.algorithm_func = algorithm_func
        self.cell_size = cell_size

        # Load the maze from a text file
        self.rows = 20
        self.cols = 20

        # Set up the canvas with the correct size
        self.canvas = tk.Canvas(master, width=self.cols * cell_size, height=self.rows * cell_size)
        self.canvas.pack()

        # Add label for timer
        self.timer_label = tk.Label(master, text="Algorithm Runtime: 0 ms")
        self.timer_label.pack()

        # Find start and end points
        self.start, self.end = (0, 0), (9, 9)

        # Draw the initial maze
        self.draw_maze()

        # Run the algorithm and animate the solution
        start_time = time.perf_counter()
        path, visited_nodes = self.algorithm_func(self.start, self.end)
        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds

        # Update timer label
        self.timer_label.config(text=f"Algorithm Runtime: {execution_time:.2f} ms")
        print(f"{title} Runtime: {execution_time:.2f} ms")
        print(f"Path length: {len(path) if path else 0}")
        print(f"Nodes visited: {len(visited_nodes)}")

        if path:
            delay = 0
            for current, neighbor, det in visited_nodes:
                if current in path:
                    self.master.after(delay, self.color_cell, current[0], current[1], 'blue')
                else:
                    self.master.after(delay, self.color_cell, current[0], current[1], 'cyan')
                if det == '1' and neighbor not in path:
                    self.master.after(delay, self.color_cell, neighbor[0], neighbor[1], 'black')
                elif det == '0' and neighbor not in path:
                    self.master.after(delay, self.color_cell, neighbor[0], neighbor[1], 'white')
                elif det == 'S' and neighbor not in path:
                    self.master.after(delay, self.color_cell, neighbor[0], neighbor[1], 'red')
                elif det == 'E' and neighbor not in path:
                    self.master.after(delay, self.color_cell, neighbor[0], neighbor[1], 'red')
                delay += 50  # Increment delay for each step
        else:
            delay = 0
            for current, neighbor, det in visited_nodes:
                self.master.after(delay, self.color_cell, current[0], current[1], 'cyan')
                if det == '1':
                    self.master.after(delay, self.color_cell, neighbor[0], neighbor[1], 'black')
                elif det == '0':
                    self.master.after(delay, self.color_cell, neighbor[0], neighbor[1], 'white')
                elif det == 'S':
                    self.master.after(delay, self.color_cell, neighbor[0], neighbor[1], 'red')
                elif det == 'E':
                    self.master.after(delay, self.color_cell, neighbor[0], neighbor[1], 'red')
                delay += 50  # Increment delay for each step

    def draw_maze(self):
        """Draw the maze on the Tkinter canvas."""
        for r in range(self.rows):
            for c in range(self.cols):
                '''if grid[r][c] == '1':
                    color = 'black'  # Wall
                elif grid[r][c] == '0':
                    color = 'white'  # Path
                elif grid[r][c] == 'S':
                    color = 'red'  # Start point
                elif grid[r][c] == 'E':
                    color = 'red'  # End point '''
                if (r, c) == self.start or (r, c) == self.end:
                    color = 'red'
                else:
                    color = 'yellow'

                self.canvas.create_rectangle(c * self.cell_size, r * self.cell_size,
                                             (c + 1) * self.cell_size, (r + 1) * self.cell_size,
                                             fill=color)

    def animate_path(self, path, delay_start=0):
        """Animate the drawing of the path with multiple colors."""
        colors = ['cyan', 'blue', 'white', 'black', 'red']  # All colors used in the program
        color_index = 0
        delay = delay_start
        for i, (row, col) in enumerate(path):
            # Cycle through colors for each cell in the path
            color = colors[color_index]
            self.master.after(delay, self.color_cell, row, col, color)
            color_index = (color_index + 1) % len(colors)
            delay += 100  # Delay between each cell
        return delay  # Return the final delay for coordination with other animations

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


if __name__ == "__main__":
    # First window for A* algorithm
    root_astar = tk.Tk()
    astar_app = MazeApp(root_astar, "A* Algorithm", astar.run_astar)

    # Second window for Dijkstra algorithm
    root_dijkstra = tk.Tk()
    dijkstra_app = MazeApp(root_dijkstra, "Dijkstra Algorithm", dijkstra.run_dijkstra)

    # Third window for Flood fill algorithm
    root_flood = tk.Tk()
    flood_app = MazeApp(root_flood, "Flood Fill Algorithm", flood.run_flood)

    # Fourth window for Bidirectional search algorithm
    root_ida = tk.Tk()
    ida_app = MazeApp(root_ida, "Iterative Deepening A* Algorithm", ida.run_ida_star)

    # Start both Tkinter windows
    root_astar.mainloop()
    root_dijkstra.mainloop()
    root_flood.mainloop()
    root_ida.mainloop()
