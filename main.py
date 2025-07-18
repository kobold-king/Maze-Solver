from tkinter import Tk, BOTH, Canvas
from window import Window, Line, Point

def main():

    win = Window(800, 600)
    l = Line(Point(0, 600), Point(800, 0))
    win.draw_line(l, "black")
    win.wait_for_close()


if __name__ == "__main__":
    main()
