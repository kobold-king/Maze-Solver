from tkinter import Tk, BOTH, Canvas
from window import Window, Line, Point, Cell, Maze

def main():

    # win = Window(800, 600)
    # l = Line(Point(0, 600), Point(800, 0))
    # win.draw_line(l, "black")
    # C1 = Cell(win)
    # C1.has_left_wall = False
    # C1.draw(0, 0, 100, 100)

    # C2 = Cell(win)
    # C2.has_right_wall = False
    # C2.draw(100, 100, 200, 200)

    # C1.draw_move(C2)

    # C3 = Cell(win)
    # C3.has_bottom_wall = False
    # C3.draw(200, 200, 300, 300)

    # C2.draw_move(C3, undo=True)

    # C4 = Cell(win)
    # C4.has_top_wall = False
    # C4.draw(300, 300, 400, 400)

    # C3.draw_move(C4)
    num_rows = 30
    num_cols = 30
    margin = 20
    screen_x = 1000
    screen_y = 1000
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows
    win = Window(screen_x, screen_y)

    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win, 10)

    win.wait_for_close()


if __name__ == "__main__":
    main()
