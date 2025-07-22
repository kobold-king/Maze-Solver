from tkinter import Tk, BOTH, Canvas
import random
import time
import json

class Window:
    def __init__(self, width, height):
        """
        Initializes a new Window object.
        """
        self.__root = Tk()
        self.__root.title("Maze Solve")  # Set the title of the window
        self.__canvas = Canvas(self.__root, width=width, height=height, bg="white")
        self.__canvas.pack(fill=BOTH, expand=1)  # Pack the canvas widget to make it visible
        self.__running = False  # Initialize the running state to False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        """
        Forces a redraw of the Tkinter root window and its widgets.

        This function first processes all pending "idle" events, such as
        geometry management and redrawing, using update_idletasks().
        Then, it processes all other pending events, including callbacks
        and event handling, using update().

        """
        self.__root.update_idletasks()  # Process pending idle tasks
        self.__root.update()           # Process all other pending events and callbacks

    def wait_for_close(self):
        self.__running = True
        while self.__running == True:
            self.redraw()

    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color) # Draws line

    def close(self):
        self.__running = False


class Point:
    """
    Represents a point in 2D space with x and y coordinates.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    """
    Represents a line segment defined by two Point objects.
    """
    def __init__(self, point1, point2):
        """
        Initializes a Line object with two Point objects as its endpoints.
        """
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color):
        canvas.create_line(self.point1.x, self.point1.y,
                           self.point2.x, self.point2.y,
                           fill=fill_color, width=3)

class Cell:
    """
    Creates a box in our window with 4 potential walls
    """
    def __init__(self, window_instance=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1
        self.visited = False
        self.__win = window_instance


    def get_random_color(self):
        """Generates a random hexadecimal color code."""
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return f'#{r:02x}{g:02x}{b:02x}'


    def draw(self, new_x1, new_y1, new_x2, new_y2):
        if self.__win is None:
            return

        self.__x1 = new_x1
        self.__x2 = new_x2
        self.__y1 = new_y1
        self.__y2 = new_y2

        if self.has_left_wall:
            left_wall = Line(Point(self.__x1, self.__y1), Point(self.__x1, self.__y2))
            self.__win.draw_line(left_wall, "black")
        else:
            left_wall = Line(Point(self.__x1, self.__y1), Point(self.__x1, self.__y2))
            self.__win.draw_line(left_wall, "white")

        if self.has_right_wall:
            right_wall = Line(Point(self.__x2, self.__y1), Point(self.__x2, self.__y2))
            self.__win.draw_line(right_wall, "black")
        else:
            right_wall = Line(Point(self.__x2, self.__y1), Point(self.__x2, self.__y2))
            self.__win.draw_line(right_wall, "white")

        if self.has_top_wall:
            top_wall = Line(Point(self.__x1, self.__y1), Point(self.__x2, self.__y1))
            self.__win.draw_line(top_wall, "black")
        else:
            top_wall = Line(Point(self.__x1, self.__y1), Point(self.__x2, self.__y1))
            self.__win.draw_line(top_wall, "white")

        if self.has_bottom_wall:
            bottom_wall = Line(Point(self.__x1, self.__y2), Point(self.__x2, self.__y2))
            self.__win.draw_line(bottom_wall, "black")
        else:
            bottom_wall = Line(Point(self.__x1, self.__y2), Point(self.__x2, self.__y2))
            self.__win.draw_line(bottom_wall, "white")

    def draw_move(self, to_cell, undo=False):
        if self.__win is None:
            return
        # The draw point is is the middleof the cell
        half_length = abs(self.__x2 - self.__x1) // 2
        x_center = half_length + self.__x1
        y_center = half_length + self.__y1

        half_length2 = abs(to_cell.__x2 - to_cell.__x1) // 2
        x_center2 = half_length2 + to_cell.__x1
        y_center2 = half_length2 + to_cell.__y1

        if not undo:
            move_line = Line(Point(x_center, y_center), Point(x_center2, y_center2))
            self.__win.draw_line(move_line, self.get_random_color())
        else:
            move_line = Line(Point(x_center, y_center), Point(x_center2, y_center2))
            self.__win.draw_line(move_line, "gray")
        # find center point of self (point 1)
        # find center of new cell (point 2)
        # if undo, color of line is red, otherwise gray


class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__cells = [] # 2D list
        # Check for seed
        if seed:
            random.seed(seed)

        # Generate cells for maze at start
        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0, 0)
        time.sleep(10)
        self.__reset_cells_visited()



    def __create_cells(self):
        for i in range(0, self.__num_cols):
            column = []
            for j in range(0, self.__num_rows):
                cell = Cell(self.__win)
                column.append(cell)
            self.__cells.append(column)

        for i in range(0, self.__num_cols):
            for j in range(0, self.__num_rows):
                self.__draw_cell(i, j)

    def __draw_cell(self, i, j):
        if self.__win is None:
            return

        cell_x1 = self.__x1 + i * self.__cell_size_x
        cell_y1 = self.__y1 + j * self.__cell_size_y
        cell_x2 = cell_x1 + self.__cell_size_x
        cell_y2 = cell_y1 + self.__cell_size_y

        self.__cells[i][j].draw(cell_x1 , cell_y1 , cell_x2 , cell_y2)
        self.__animate()

    def __animate(self):
        if self.__win is None:
            return

        self.__win.redraw()
        time.sleep(0.05)

    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0, 0)
        self.__cells[self.__num_cols - 1][self.__num_rows - 1].has_bottom_wall = False
        self.__draw_cell((self.__num_cols - 1),(self.__num_rows - 1))

    # Break walls to make Maze
    def __break_walls_r(self, i, j):
        self.__cells[i][j].visited = True

        while True:
            to_visit = []
            # left
            if i > 0 and not self.__cells[i - 1][j].visited:
                to_visit.append((i - 1, j))
            # right
            if i < self.__num_cols - 1 and not self.__cells[i + 1][j].visited:
                to_visit.append((i + 1, j))
            # up
            if j > 0 and not self.__cells[i][j - 1].visited:
                to_visit.append((i, j - 1))
            # down
            if j < self.__num_rows - 1 and not self.__cells[i][j + 1].visited:
                to_visit.append((i, j + 1))

            # Check if 0 Directions found
            if len(to_visit) == 0:
                self.__draw_cell(i, j)
                return

            # randomly choose the next direction to go
            direction_index = random.randrange(len(to_visit))
            next_index = to_visit[direction_index]

            # knock out walls
            # right
            if next_index[0] == i + 1:
                self.__cells[i][j].has_right_wall = False
                self.__cells[i + 1][j].has_left_wall = False
            # left
            if next_index[0] == i - 1:
                self.__cells[i][j].has_left_wall = False
                self.__cells[i - 1][j].has_right_wall = False
            # down
            if next_index[1] == j + 1:
                self.__cells[i][j].has_bottom_wall = False
                self.__cells[i][j + 1].has_top_wall = False
            # up
            if next_index[1] == j - 1:
                self.__cells[i][j].has_top_wall = False
                self.__cells[i][j - 1].has_bottom_wall = False

            # recursively visit the next cell
            self.__break_walls_r(next_index[0], next_index[1])

    # Reset Cells
    def __reset_cells_visited(self):
        for col in self.__cells:
            for cell in col:
                cell.visited = False

    # Solve the Maze
    def _solve_r(self, i, j):
        self.__animate()
        self.__cells[i][j].visited = True

        # Check if at the end
        if not self.__cells[i][j].has_bottom_wall and j == self.__num_rows - 1:
            return True

        # Check directions
        # left
        if i > 0 and not self.__cells[i][j].has_left_wall and not self.__cells[i - 1][j].visited:
            self.__cells[i][j].draw_move(self.__cells[i - 1][j])
            next_cell = self._solve_r((i - 1),j)
            if next_cell == True:
                return True
            else:
                self.__cells[i][j].draw_move(self.__cells[i - 1][j], True)
        # right
        if i < self.__num_cols - 1 and not self.__cells[i][j].has_right_wall and not self.__cells[i + 1][j].visited:
            self.__cells[i][j].draw_move(self.__cells[i + 1][j])
            next_cell = self._solve_r((i + 1),j)
            if next_cell == True:
                return True
            else:
                self.__cells[i][j].draw_move(self.__cells[i + 1][j], True)
        # up
        if j > 0 and not self.__cells[i][j].has_top_wall and not self.__cells[i][j - 1].visited:
            self.__cells[i][j].draw_move(self.__cells[i][j - 1])
            next_cell = self._solve_r(i, (j - 1))
            if next_cell == True:
                return True
            else:
                self.__cells[i][j].draw_move(self.__cells[i][j - 1], True)
        # down
        if j < self.__num_rows - 1 and not self.__cells[i][j].has_bottom_wall and not self.__cells[i][j + 1].visited:
            self.__cells[i][j].draw_move(self.__cells[i][j + 1])
            next_cell = self._solve_r(i, (j + 1))
            if next_cell == True:
                return True
            else:
                self.__cells[i][j].draw_move(self.__cells[i][j + 1], True)

        return False

    def solve(self):
        return self._solve_r(0, 0)
