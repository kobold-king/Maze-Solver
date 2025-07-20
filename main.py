from tkinter import Tk, BOTH, Canvas
from window import Window, Line, Point, Cell

def main():

    win = Window(800, 600)
    # l = Line(Point(0, 600), Point(800, 0))
    # win.draw_line(l, "black")
    C1 = Cell(win)
    C1.has_left_wall = False
    C1.draw(0, 0, 100, 100)

    C2 = Cell(win)
    C2.has_right_wall = False
    C2.draw(100, 100, 200, 200)

    C3 = Cell(win)
    C3.has_bottom_wall = False
    C3.draw(200, 200, 300, 300)

    C4 = Cell(win)
    C4.has_top_wall = False
    C4.draw(300, 300, 400, 400)

    win.wait_for_close()


if __name__ == "__main__":
    main()
