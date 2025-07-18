from tkinter import Tk, BOTH, Canvas

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
