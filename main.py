import tkinter as tk
from tkinter import messagebox
from random import randint
from isvalid import is_num_valid, is_valid_sudoku
from generator import _gen
import time
from PIL import ImageGrab

# Test
class SudokuMastermind:
    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku Mastermind")
        self.master.resizable(False, False)
        self.grid = [[None for _ in range(9)] for _ in range(9)]
        self.difficulty = "Easy"
        self.generated_list = []
        self.default_color = "#bbdefb"
        self.grid_clicked_color = "#bbdefd"
        self.grid_affected_color = "#ffffff"
        self.grid_unaffected_color = "#e2ebf3"
        self.generated_color = "#e2ebf3"
        self.fg_white = "white"
        self.fg_black = "black"
        self.grid_clicked = None
        self.buttons_can_be_clicked = True
        self._create_grid()
        self._create_menu()
        self._buttons()
        self._bindings()

    def _create_grid(self):
        # Create the grid
        self.grid = []
        for i in range(9):
            row = []
            for j in range(9):
                entry = tk.Entry(
                    width=3,
                    font=("Helvetica", 30),
                    justify="center",
                    bd=1,
                    relief=tk.RIDGE,
                )
                entry.grid(row=i, column=j, padx=1, pady=1)
                row.append(entry)
                entry.config(bg=self.default_color)
                entry.config(fg=self.fg_black)
                entry.bind("<Button-1>", self._grid_clicked)
            self.grid.append(row)

    def _grid_clicked(self, event):
        # Highlight the clicked cell, row, and column and the 3x3 subgrid
        # Get the row and column of the clicked cell
        row = event.widget.grid_info()["row"]
        col = event.widget.grid_info()["column"]
        self.grid_clicked = event.widget
        self._unhighlight(row, col)

        # Highlight the row and column
        for i in range(9):
            self.grid[row][i].config(bg=self.grid_affected_color)
            self.grid[i][col].config(bg=self.grid_affected_color)

        # Highlight the 3x3 subgrid
        for i in range(3):
            for j in range(3):
                self.grid[(row // 3) * 3 + i][(col // 3) * 3 + j].config(
                    bg=self.grid_affected_color
                )

        # unhighlight after focus is lost
        event.widget.bind(
            "<FocusOut>",
            lambda event: self._unhighlight(row, col)
            if event.widget.get() == ""
            else event.widget.config(bg=self.grid_unaffected_color),
        )

        # Highlight the clicked cell after its focused
        event.widget.config(bg=self.grid_clicked_color)

        # unhighlight everything after losing focus
        event.widget.bind(
            "<FocusOut>",
            lambda event: self._unhighlight(row, col)
            if event.widget.get() == ""
            else event.widget.config(bg=self.grid_unaffected_color),
        )

    def _unhighlight(self, row, col):
        # unhighlight the entire grid
        for i in range(9):
            for j in range(9):
                self.grid[i][j].config(bg=self.grid_unaffected_color)
        # unhighlight the clicked cell
        self.grid_clicked.config(bg=self.grid_unaffected_color)

        # unhiglight the row and column
        for i in range(9):
            self.grid[row][i].config(bg=self.grid_unaffected_color)
            self.grid[i][col].config(bg=self.grid_unaffected_color)

        # unhighlight the 3x3 subgrid
        for i in range(3):
            for j in range(3):
                self.grid[(row // 3) * 3 + i][(col // 3) * 3 + j].config(
                    bg=self.grid_unaffected_color
                )

    def _clickable_buttons(self):
        self.buttons_can_be_clicked = True
        # Make the buttons clickable
        self.solve_button.config(state=tk.NORMAL)
        self.generate_button.config(state=tk.NORMAL)
        self.clear_button.config(state=tk.NORMAL)

    def _unclickable_buttons(self):
        self.buttons_can_be_clicked = False
        # Make the buttons unclickable
        self.solve_button.config(state=tk.DISABLED)
        self.generate_button.config(state=tk.DISABLED)
        self.clear_button.config(state=tk.DISABLED)

    def _menu_unclickable(self):
        self.file_menu.entryconfig("Exit(E)", state=tk.DISABLED)
        self.puzzle_menu.entryconfig("Solve(S)", state=tk.DISABLED)
        self.puzzle_menu.entryconfig("Generate(G)", state=tk.DISABLED)
        self.puzzle_menu.entryconfig("Clear(C)", state=tk.DISABLED)

    def _menu_clickable(self):
        self.file_menu.entryconfig("Exit(E)", state=tk.NORMAL)
        self.puzzle_menu.entryconfig("Solve(S)", state=tk.NORMAL)
        self.puzzle_menu.entryconfig("Generate(G)", state=tk.NORMAL)
        self.puzzle_menu.entryconfig("Clear(C)", state=tk.NORMAL)

    def _toggle_buttons(self):
        if self.buttons_can_be_clicked:
            self._unclickable_buttons()
            self._menu_unclickable()
        else:
            self._clickable_buttons()
            self._menu_clickable()

    def _create_menu(self):
        # Create a menu
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)

        # File menu
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        # Difficulty dropdown menu
        self.difficulty_menu = tk.Menu(self.file_menu, tearoff=0)
        self.file_menu.add_cascade(label="Difficulty", menu=self.difficulty_menu)
        self.difficulty_menu.add_command(
            label="Easy (1)", command=lambda: self._toggle_difficulty("Easy")
        )
        self.difficulty_menu.add_command(
            label="Medium (2)", command=lambda: self._toggle_difficulty("Medium")
        )
        self.difficulty_menu.add_command(
            label="Hard (3)", command=lambda: self._toggle_difficulty("Hard")
        )
        self.file_menu.add_command(label="Save(S)", command=self.save)
        self.file_menu.add_command(label="Exit(E)", command=self.master.destroy)

        # Puzzle menu
        self.puzzle_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Puzzle", menu=self.puzzle_menu)
        self.puzzle_menu.add_command(label="Solve(S)", command=self.solve)
        self.puzzle_menu.add_command(
            label="Generate(G)", command=lambda: self.generate("Easy")
        )
        self.puzzle_menu.add_command(label="Clear(C)", command=self.clear)

        # Create a help menu
        self.help_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self._about)

    def _about(self):
        messagebox.showinfo(
            "About",
            "Sudoku Mastermind\n"
            "Version 1.0\n"
            "   - GUI version\n"
            "   - Uses backtracking algorithm\n"
            "   - Can generate puzzles\n"
            "   - Can solve puzzles\n"
            "   - Can change difficulty levels\n"
            "   - Can save the puzzle\n"
            "Created by: \n"
            "    - lorem ipsum\n"
            "    - lorem ipsum\n"
            "    - lorem ipsum\n"
            "    - lorem ipsum\n",
        )

    def _buttons(self):
        # Create "Solve" button
        self.solve_button = tk.Button(
            self.master,
            text="Solve",
            command=self.solve,
            bg="green",
            fg="white",
            width=13,
        )
        self.solve_button.grid(row=9, column=0, columnspan=2)

        # create generate button
        self.generate_button = tk.Button(
            self.master,
            text="Generate",
            command=lambda: self.generate(self.difficulty),
            bg="purple",
            fg="white",
            width=13,
        )
        self.generate_button.grid(row=9, column=2, columnspan=2)

        # create dofficulty button with background color light green
        self.difficulty_button = tk.Menubutton(
            self.master,
            text="Difficulty",
            relief=tk.RAISED,
            bg="yellow",
            fg="black",
            width=15,
        )
        self.difficulty_button.grid(row=9, column=5, columnspan=2)
        self.difficulty_menu = tk.Menu(self.difficulty_button, tearoff=0)
        # Add a command for easy difficulty that generates a puzzle and sets the difficulty to easy
        self.difficulty_menu.add_command(
            label="Easy", command=lambda: self._toggle_difficulty("Easy")
        )
        self.difficulty_menu.add_command(
            label="Medium", command=lambda: self._toggle_difficulty("Medium")
        )
        self.difficulty_menu.add_command(
            label="Hard", command=lambda: self._toggle_difficulty("Hard")
        )
        self.difficulty_button["menu"] = self.difficulty_menu

        # create clear button with background color RED
        self.clear_button = tk.Button(
            self.master,
            text="Clear",
            command=self.clear,
            bg="#F44336",
            fg="white",
            width=12,
        )
        self.clear_button.grid(row=9, column=7, columnspan=2)

    def _bindings(self):
        # Type ESC to unfocus the currently focused cell
        self.master.bind(
            "<Escape>",
            lambda event: self.master.focus() if self.buttons_can_be_clicked else None,
        )

        # type to change difficulty level
        self.master.bind(
            "1",
            lambda event: self._toggle_difficulty("Easy")
            if self.buttons_can_be_clicked
            else None,
        )
        self.master.bind(
            "2",
            lambda event: self._toggle_difficulty("Medium")
            if self.buttons_can_be_clicked
            else None,
        )
        self.master.bind(
            "3",
            lambda event: self._toggle_difficulty("Hard")
            if self.buttons_can_be_clicked
            else None,
        )

        # Type S to solve the puzzle
        self.master.bind(
            "s", lambda event: self.solve() if self.buttons_can_be_clicked else None
        )
        self.master.bind(
            "S", lambda event: self.solve() if self.buttons_can_be_clicked else None
        )

        # Type CTRL + S to save the puzzle
        self.master.bind(
            "<Control-s>",
            lambda event: self.save() if self.buttons_can_be_clicked else None,
        )
        self.master.bind(
            "<Control-S>",
            lambda event: self.save() if self.buttons_can_be_clicked else None,
        )

        # Type G to generate a puzzle
        self.master.bind(
            "g",
            lambda event: self.generate(self.difficulty)
            if self.buttons_can_be_clicked
            else None,
        )
        self.master.bind(
            "G",
            lambda event: self.generate(self.difficulty)
            if self.buttons_can_be_clicked
            else None,
        )

        # Type C to clear the puzzle
        self.master.bind(
            "c", lambda event: self.clear() if self.buttons_can_be_clicked else None
        )
        self.master.bind(
            "C", lambda event: self.clear() if self.buttons_can_be_clicked else None
        )

        # Type E to exit the program
        self.master.bind("e", lambda event: self.master.destroy())
        self.master.bind("E", lambda event: self.master.destroy())

    def _toggle_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.difficulty_button.config(text="Difficulty: " + difficulty)

    def solve(self):
        # make the other buttons unclickable
        self._toggle_buttons()

        puzzle = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                try:
                    puzzle[i][j] = int(self.grid[i][j].get())
                except ValueError:
                    pass
        # print(puzzle)
        if is_valid_sudoku(puzzle):
            if self.backtrack(puzzle):
                for i in range(9):
                    for j in range(9):
                        self.grid[i][j].delete(0, tk.END)
                        self.grid[i][j].insert(0, puzzle[i][j])
                        # sleep for 0.05 seconds
                        time.sleep(randint(1, 10) / 100)
                        self.master.update()
            else:
                messagebox.showerror("Error", "No solution exists")
        else:
            messagebox.showerror("Error", "Invalid Sudoku")

        # make the other buttons clickable
        self._toggle_buttons()

    def backtrack(self, puzzle):
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] == 0:
                    for num in range(1, 10):
                        if is_num_valid(puzzle, i, j, num):
                            puzzle[i][j] = num
                            if self.backtrack(puzzle):
                                return True
                            puzzle[i][j] = 0
                    return False
        return True

    def generate(self, difficulty):
        board = _gen()
        for i in range(9):
            for j in range(9):
                self.grid[i][j].delete(0, tk.END)
                self.grid[i][j].insert(0, board[i][j])
                self.grid[i][j].config(bg="white")
        if difficulty == "Easy":
            for i in range(9):
                for j in range(9):
                    if randint(0, 1) != 1:
                        self.grid[i][j].delete(0, tk.END)
                        self.grid[i][j].config(bg=self.generated_color)
                        self.generated_list.append((i, j))
        elif difficulty == "Medium":
            for i in range(9):
                for j in range(9):
                    if randint(0, 3) != 1:
                        self.grid[i][j].delete(0, tk.END)
                        self.grid[i][j].config(bg=self.generated_color)
                        self.generated_list.append((i, j))
        elif difficulty == "Hard":
            for i in range(9):
                for j in range(9):
                    if randint(0, 5) != 1:
                        self.grid[i][j].delete(0, tk.END)
                        self.grid[i][j].config(bg=self.generated_color)
                        self.generated_list.append((i, j))

    def save(self):
        # save the current puzzle as a png file in the current directory
        # get the coordinates of the puzzle grid
        x = self.grid[0][0].winfo_rootx()
        y = self.grid[0][0].winfo_rooty()
        x1 = self.grid[8][8].winfo_rootx() + 50
        y1 = self.grid[8][8].winfo_rooty() + 50
        # wait for 0.5 seconds
        time.sleep(0.5)
        # save the image as ./assets/sudoku-[current time].png
        ImageGrab.grab().crop((x, y, x1, y1)).save(
            "./assets/sudoku-" + str(time.time()) + ".png"
        )

    def clear(self):
        for i in range(9):
            for j in range(9):
                self.grid[i][j].delete(0, tk.END)
                self.grid[i][j].config(bg=self.default_color)


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuMastermind(root)
    root.mainloop()
