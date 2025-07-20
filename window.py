from tkinter import Tk, BOTH, Canvas
import random

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
                           fill=fill_color, width=2)

class Cell:
    """
    Creates a box in our window with 4 potential walls
    """
    def __init__(self, window_instance):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1
        self.__win = window_instance


    def get_random_color(self):
        """Generates a random hexadecimal color code."""
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return f'#{r:02x}{g:02x}{b:02x}'


    def draw(self, new_x1, new_y1, new_x2, new_y2):
        self.__x1 = new_x1
        self.__x2 = new_x2
        self.__y1 = new_y1
        self.__y2 = new_y2

        if self.has_left_wall:
            left_wall = Line(Point(self.__x1, self.__y1), Point(self.__x1, self.__y2))
            self.__win.draw_line(left_wall, self.get_random_color())

        if self.has_right_wall:
            right_wall = Line(Point(self.__x2, self.__y1), Point(self.__x2, self.__y2))
            self.__win.draw_line(right_wall, self.get_random_color())

        if self.has_top_wall:
            top_wall = Line(Point(self.__x1, self.__y1), Point(self.__x2, self.__y1))
            self.__win.draw_line(top_wall, self.get_random_color())

        if self.has_bottom_wall:
            bottom_wall = Line(Point(self.__x1, self.__y2), Point(self.__x2, self.__y2))
            self.__win.draw_line(bottom_wall, self.get_random_color())

    def draw_move(self, to_cell, undo=False):
        pass
        # find center point of self (point 1)
        # find center of new cell (point 2)
        # if undo, color of line is red, otherwise gray
