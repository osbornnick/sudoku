class Sudoku():
    """
    Sudoku game representation
    """

    def __init__(self, solution, puzzle):
        self.height = 9
        self.width = 9
        if len(solution) == 9:
            self.solution = solution
        else:
            self.solution = self.string_to_grid(solution)
        if len(puzzle) == 9:
            self.puzzle = puzzle
        else:
            self.puzzle = self.string_to_grid(puzzle)
        # generate possible filled solution
        # generate puzzle with unique solution

    def print_solution(self):
        for row in self.solution:
            print(" ".join([str(cell) for cell in row]))

    def print_puzzle(self):
        print("Puzzle -")
        for row in self.puzzle:
            print(" ".join([str(cell) if cell != 0 else ' ' for cell in row]))

    def complete(self):
        if self.puzzle == self.solution:
            return True
        return False

    def progress(self):
        flat = [val for row in self.puzzle for val in row]
        return 81 - flat.count('0')

    def turn(self):
        row = int(input("Choose a row (0-8)> "))
        col = int(input("Choose a column (0-8)> "))
        val = int(input("Choose a value (1-9)> "))
        self.puzzle[row][col] = val

    def play(self):
        print("Let's play Soduku!")
        print("The puzzle:")
        self.print_puzzle()
        while not self.complete():
            self.turn()
            self.print_puzzle()

    def assigned(self, cell):
        i, j = cell
        if self.puzzle[i][j] != 0:
            return True
        return False

    @classmethod
    def string_to_grid(self, board_string):
        temp = [0 if i == '.' else int(i) for i in board_string]
        return [temp[9*i:9*i+9] for i in range(9)]

    @classmethod
    def grid_to_string(self, grid):
        flat = [str(val) for row in grid for val in row]
        return "".join(flat)
