from tkinter import *
import time

root = Tk()
root.title("Sudoku")

class Sudoku:

    board = [[0 for i in range(9)]for j in range(9)]

    def __init__(self):
        with open('board', 'r') as file:
            self.board = [[int(num) for num in line.split(',')] for line in file]

    def reset_board(self):
        with open('board', 'r') as file:
            self.board = [[int(num) for num in line.split(',')] for line in file]

    def print_board(self):
        for row in self.board:
            for num in row:
                print(num, end=" ")
            print("")

    def row_check(self, num, row):
        for i in range(9):
            if num == self.board[row][i]:
                return False
        else:
            return True

    def col_check(self, num, col):
        for i in range(9):
            if num == self.board[i][col]:
                return False
        else:
            return True

    def square_check(self, num, row, col):
        for i in range(3):
            for j in range(3):
                if num == self.board[row - (row % 3) + i][col - (col % 3) + j]:
                    return False
        return True

    def is_safe(self, num, row, col):
        if self.row_check(num, row) and self.col_check(num, col) and self.square_check(num, row, col):
            return True
        return False

    def next_available(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i, j
        return False

    def solve_sudoku(self):

        coor = self.next_available()
        if not coor:
            return True

        row, col = coor

        for num in range(1, 10):
            if self.is_safe(num, row, col):
                self.board[row][col] = num

                if self.solve_sudoku():
                    return True

                self.board[row][col] = 0

        return False


class Cube:

    def __init__(self, row, col):
        self.frame = Frame(width=60, height=60, highlightbackground="black", highlightcolor="black",
                           highlightthickness=1, bd=0)
        self.suggestionLabel = Label(self.frame, text="", font=("Comics", 20), fg="black")
        self.answerLabel = Label(self.frame, text="", font=("Comics", 36), fg="black")

        self.known = False
        self.suggestion = False
        self.answer = False
        self.val = 0
        self.row = row
        self.col = col

    def place_cube(self, i, j):
        self.frame.grid(row=i, column=j + 1)

        self.suggestionLabel.place(relx=0.2, rely=0.3, anchor=CENTER)
        self.suggestionLabel.pos = self.suggestionLabel.place_info()
        self.suggestionLabel.place_forget()

        self.answerLabel.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.answerLabel.pos = self.answerLabel.place_info()
        self.answerLabel.place_forget()

    def write_suggestion(self, val):
        self.suggestion = True
        self.suggestionLabel.config(text=val)
        self.suggestionLabel.place(self.suggestionLabel.pos)
        self.val = val

    def clear_suggestion(self):
        self.suggestion = False
        self.suggestionLabel.config(text="")
        self.suggestionLabel.place_forget()

    def write_answer(self, val):
        self.answer = True
        self.answerLabel.config(text=val)
        self.answerLabel.place(self.answerLabel.pos)
        self.val = val

    def clear_answer(self):
        self.answer = False
        self.answerLabel.config(text="")
        self.answerLabel.place_forget()
        self.val = 0


class Grid:

    cubes = [[0 for i in range(9)]for j in range(9)]
    verticalLine = [[0 for i in range(4)] for j in range(9)]
    horizontalLine = [[0 for i in range(4)] for j in range(9)]

    def __init__(self, sudoku):
        # create all cubes
        for i in range(9):
            for j in range(9):
                self.cubes[i][j] = Cube(i, j)
                self.cubes[i][j].place_cube(i, j)
                if sudoku.board[i][j] != 0:
                    self.cubes[i][j].write_answer(sudoku.board[i][j])
                    self.cubes[i][j].known = True
                else:
                    self.bind_cube(i, j)
        self.grid_lines()
        self.footer = Frame(root, width=540, height=60, highlightbackground="black", highlightcolor="black",
                            highlightthickness=1, bd=0)
        self.footer.grid(row=9, columnspan=10)
        self.notification = Label(self.footer, text="", font=("Comics", 20), fg="black")
        self.notification.place(rely=0.5, relx = 0, anchor="w")
        self.playTime = Label(self.footer, text="", font=("Comics", 20), fg="black")
        self.playTime.place(rely=0.5, relx=1, anchor="e")
        self.startTime = time.time()
        self.countDown = 0

    def clock_update(self):
        now = time.time()
        elapsed = round(now - self.startTime)
        second = elapsed % 60
        minute = elapsed // 60
        self.playTime.config(text=str(minute) + ":" + str(second))
        if self.countDown != 0:
            self.countDown -= 1
        else:
            self.notification.config(text="")
            root.update()
        root.after(1000, self.clock_update)

    def grid_lines(self):
        # creates vertical lines
        for i in range(9):
            for j in range(2):
                self.verticalLine[i][j] = Frame(width=2, height=60, highlightbackground="black", highlightcolor="black",
                                           highlightthickness=1, bd=0)
                self.verticalLine[i][j].grid(row=i, column=(j + 1) * 3, sticky="e")
                self.verticalLine[i][j + 2] = Frame(width=2, height=60, highlightbackground="black", highlightcolor="black",
                                               highlightthickness=1, bd=0)
                self.verticalLine[i][j + 2].grid(row=i, column=(j + 1) * 3 + 1, sticky="w")

        # creates horizontal lines
        for i in range(9):
            for j in range(2):
                self.horizontalLine[i][j] = Frame(width=60, height=2, highlightbackground="black", highlightcolor="black",
                                             highlightthickness=1, bd=0)
                self.horizontalLine[i][j].grid(row=(j + 1) * 3 - 1, column=i + 1, sticky="s")
                self.horizontalLine[i][j + 2] = Frame(width=60, height=2, highlightbackground="black",
                                                 highlightcolor="black", highlightthickness=1, bd=0)
                self.horizontalLine[i][j+2].grid(row=(j+1)*3, column=i+1, sticky="n")

    def bind_cube(self, row, col):
        self.cubes[row][col].suggestionLabel.config(fg="gray55")
        self.cubes[row][col].answerLabel.config(fg="gray55")
        self.cubes[row][col].frame.bind("<Button-1>", lambda event: UserActions.frame_click(event, self.cubes[row][col]))
        self.cubes[row][col].frame.bind("<Leave>", lambda event: UserActions.leave_mouse(event, self.cubes[row][col]))
        self.cubes[row][col].frame.bind("<Enter>", lambda event: UserActions.enter_mouse(event, self.cubes[row][col]))
        self.cubes[row][col].suggestionLabel.bind("<Button-1>", lambda event: UserActions.frame_click(event, self.cubes[row][col]))
        self.cubes[row][col].suggestionLabel.bind("<Leave>", lambda event: UserActions.leave_mouse(event, self.cubes[row][col]))
        self.cubes[row][col].suggestionLabel.bind("<Enter>", lambda event: UserActions.enter_mouse(event, self.cubes[row][col]))
        self.cubes[row][col].answerLabel.bind("<Button-1>", lambda event: UserActions.frame_click(event, self.cubes[row][col]))
        self.cubes[row][col].answerLabel.bind("<Leave>", lambda event: UserActions.leave_mouse(event, self.cubes[row][col]))
        self.cubes[row][col].answerLabel.bind("<Enter>", lambda event: UserActions.enter_mouse(event, self.cubes[row][col]))

    def reload_grid(self, sudoku):
        for i in range(9):
            for j in range(9):
                self.cubes[i][j] =  Cube(i, j)
                self.cubes[i][j].place_cube(i, j)
                if sudoku.board[i][j] != 0:
                    self.cubes[i][j].write_answer(sudoku.board[i][j])
        self.grid_lines()

    def solve_grid(self, sudoku):
        coor = sudoku.next_available()
        if not coor:
            return True

        row, col = coor

        for num in range(1, 10):
            if sudoku.is_safe(num, row, col):
                sudoku.board[row][col] = num
                self.cubes[row][col].write_answer(num)
                self.cubes[row][col].answerLabel.config(fg="green2")
                root.update()
                time.sleep(0.001)

                if self.solve_grid(sudoku):
                    return True

                sudoku.board[row][col] = 0
                self.cubes[row][col].answerLabel.config(fg="red")
                root.update()
                time.sleep(0.001)

        return False


class UserActions:

    def frame_click(event, cube):
        global lastCube
        if lastCube != 0:
            lastCube.frame.config(highlightbackground="black", highlightcolor="black", highlightthickness=1, bd=0)

        cube.frame.config(highlightbackground="dark orange", highlightcolor="dark orange", highlightthickness=3,
                          bd=0)
        lastCube = cube

    def enter_mouse(event, cube):
        if cube != lastCube:
            cube.frame.config(highlightbackground="burlywood3", highlightcolor="burlywood3", highlightthickness=3,
                              bd=0)

    def leave_mouse(event, cube):
        if cube != lastCube:
            cube.frame.config(highlightbackground="black", highlightcolor="black", highlightthickness=1, bd=0)

    def enter_press(event, sudoku, grid):
        if lastCube != 0:
            if sudoku.is_safe(lastCube.val, lastCube.row, lastCube.col) and lastCube.suggestion:
                lastCube.write_answer(lastCube.val)
                lastCube.clear_suggestion()
                sudoku.board[lastCube.row][lastCube.col] = lastCube.val
                grid.notification.config(text="Number can be correct ;)")
                grid.countDown = 3
            else:
                grid.notification.config(text="You cannot enter that number here.")
                grid.countDown = 3

    def back_space_press(event, sudoku):
        if lastCube != 0:
            if lastCube.val != 0:
                lastCube.clear_answer()
                lastCube.clear_suggestion()
                sudoku.board[lastCube.row][lastCube.col] = 0

    def keyboard_press(event, sudoku, grid):
        if event.char.isdigit() and int(event.char) != 0 and not lastCube.answer:
            lastCube.write_suggestion(int(event.char))

        elif event.char == " ":
            sudoku.reset_board()
            grid.reload_grid(sudoku)
            grid.solve_grid(sudoku)


lastCube = 0

sudoku = Sudoku()
grid = Grid(sudoku)
grid.clock_update()

root.bind("<Key>", lambda event: UserActions.keyboard_press(event, sudoku, grid))
root.bind("<Return>", lambda event: UserActions.enter_press(event, sudoku, grid))
root.bind("<BackSpace>", lambda event: UserActions.back_space_press(event, sudoku))


root.mainloop()
