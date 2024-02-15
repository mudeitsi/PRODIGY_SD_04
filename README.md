# Sudoku Mastermind: Your Ultimate Puzzle Solver

Welcome to Sudoku Mastermind, your ultimate companion for effortlessly conquering Sudoku puzzles! This sleek graphical interface empowers you to input puzzles, solve them with finesse, generate new challenges, or clear the board with ease. Tailor the difficulty level to your liking, choosing between "Easy", "Medium", or "Hard".

![Sudoku Mastermind](sudoku_mastermind.gif)

## Prerequisites

- Python 3.6 or newer
- tkinter
- PIL

## Getting Started

To launch the program, follow these simple steps:

1. Clone the repository:
```
git clone https://github.com/mudeitsi/PRODIGY_SD_04.git
cd SudokuMastermind
```

2. Run the main.py file:
```
python3 ./main.py
```

## Inputting a Puzzle

Select any cell on the grid and input a number from 1 to 9. The program intuitively highlights the corresponding row, column, and 3x3 subgrid. If an invalid entry is detected, an error message will promptly appear. Until a valid puzzle is inputted, the solve, generate, or clear buttons will remain inactive.

## Solving a Puzzle

Once a valid puzzle is entered, a single click on the "Solve" button sets the solving process in motion. Sudoku Mastermind employs ingenious algorithms, including backtracking, to fill the empty cells strategically. In case of an unsolvable puzzle, an error message will gracefully notify you.

## Generating a New Puzzle

Click the "Generate" button to conjure up a fresh Sudoku challenge. Sudoku Mastermind randomly crafts puzzles according to the selected difficulty level (default: "Easy"). Get ready to tackle a brand new brain teaser!

## Clearing the Current Puzzle

For a clean slate, hit the "Clear" button. This action wipes the board clean, allowing you to embark on a new puzzle-solving adventure or input your own creation.

## Capturing a Screenshot

Capture the current puzzle by pressing CTRL+S or accessing the file menu. Sudoku Mastermind swiftly snaps a screenshot, storing the image within the assets folder as sudoku-[current time].png.

## Future Enhancements

Exciting enhancements on the horizon include additional GUI features, such as puzzle loading from files or saving solved puzzles. Performance optimizations will be made to enhance solving speed and handle puzzles with multiple solutions more efficiently.

Enjoy mastering Sudoku puzzles like a pro with Sudoku Mastermind!

Feel free to share your thoughts or suggestions. Happy puzzling! 🧩🌟
