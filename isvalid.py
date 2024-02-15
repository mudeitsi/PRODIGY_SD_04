# Function to check if all elements of the board[][] array store value in the range[1, 9]
def isinRange(board):
    N = 9
    # Traverse board[][] array
    for i in range(0, N):
        for j in range(0, N):
            # Check if board[i][j]
            # lies in the range
            if (board[i][j] <= 0) or (board[i][j] > 9):
                return False
    return True


# Function to check if the solution of sudoku puzzle is valid or not
def isValidSudoku(board):
    N = 9
    # Check if all elements of board[][] stores value in the range[1, 9]
    if isinRange(board) == False:
        return False

    # Stores unique value from 1 to N
    unique = [False] * (N + 1)

    # Traverse each row of the given array
    for i in range(0, N):
        # Initialize unique[] array to false
        for m in range(0, N + 1):
            unique[m] = False

        # Traverse each column of current row
        for j in range(0, N):
            # Stores the value of board[i][j]
            Z = board[i][j]

            # Check if current row stores duplicate value
            if unique[Z] == True:
                return False

            unique[Z] = True

    # Traverse each column of the given array
    for i in range(0, N):
        # Initialize unique[] array to false
        for m in range(0, N + 1):
            unique[m] = False

        # Traverse each row of current column
        for j in range(0, N):
            # Stores the value of board[j][i]
            Z = board[j][i]

            # Check if current column stores duplicate value
            if unique[Z] == True:
                return False

            unique[Z] = True

    # Traverse each block of size 3 * 3 in board[][] array
    for i in range(0, N - 2, 3):
        # j stores first column of each 3 * 3 block
        for j in range(0, N - 2, 3):
            # Initialize unique[] array to false
            for m in range(0, N + 1):
                unique[m] = False

            # Traverse current block
            for k in range(0, 3):
                for l in range(0, 3):
                    # Stores row number of current block
                    X = i + k

                    # Stores column number of current block
                    Y = j + l

                    # Stores the value of board[X][Y]
                    Z = board[X][Y]

                    # Check if current block stores duplicate value
                    if unique[Z] == True:
                        return False

                    unique[Z] = True

    # If all conditions satisfied
    return True

def is_valid_sudoku( grid):
    # Check each row
    for row in grid:
        if not is_valid_unit(row):
            return False

    # Check each column
    for col in zip(*grid):
        if not is_valid_unit(col):
            return False

    # Check each 3x3 subgrid
    for i in (0, 3, 6):
        for j in (0, 3, 6):
            unit = [grid[x][y] for x in range(i, i + 3) for y in range(j, j + 3)]
            if not is_valid_unit(unit):
                return False
    return True

def is_valid_unit( unit):
    unit = [i for i in unit if i != 0]
    return len(unit) == len(set(unit))

def is_num_valid(puzzle, i, j, num):
    # Check the row
    for k in range(9):
        if puzzle[i][k] == num:
            return False

    # Check the column
    for k in range(9):
        if puzzle[k][j] == num:
            return False

    # Check the 3x3 subgrid
    row_start = i // 3 * 3
    col_start = j // 3 * 3
    for k in range(3):
        for l in range(3):
            if puzzle[row_start + k][col_start + l] == num:
                return False
    return True

if __name__ == "__main__":
    board = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    if isValidSudoku(board):
        print("Valid")
    else:
        print("Not Valid")

    if is_valid_sudoku(board):
        print("Valid")
    else:
        print("Not Valid")