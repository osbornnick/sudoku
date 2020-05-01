import itertools


class Sudoku():
    """
    Sudoku game representation
    """

    def __init__(self, solution=None, puzzle=None):
        self.height = 9
        self.width = 9
        if solution:
            self.solution = solution
        if puzzle:
            self.puzzle = puzzle
        else:
            self.puzzle = [[0 for col in range(9)] for row in range(9)]
        # generate possible filled solution
        # generate puzzle with unique solution

    def print_solution(self):
        for row in self.solution:
            print(" ".join([str(cell) for cell in row]))

    def print_puzzle(self):
        for row in self.puzzle:
            print(" ".join([str(cell) if cell != 0 else ' ' for cell in row]))

    def complete(self):
        if self.puzzle == self.solution:
            return True
        return False

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
    def neighborhood(cell):
        pass


class Sentence():
    """
    Logical statement about a Sudoku game
    A sentence consists of a set of board cells,
    and a set of possible values of those cells.
    """
    def __init__(self, cells, values):
        self.cells = set(cells)
        self.values = set(values)

    def __eq__(self, other):
        return self.cells == other.cells and self.values == other.values

    def __hash__(self):
        return hash((tuple(self.cells), tuple(self.values)))

    def __str__(self):
        return f"{self.cells} <> {self.values}"

    def conclusive(self):
        """
        Test if a sentence can assign the value of a cell
        """
        if len(self.cells) == 1 and len(self.values == 1):
            return True

    def remove_assigned(self, cell, value):
        """
        Updates internal knowledge representation given the fact that
        a cell is assigned
        """
        if cell in self.cells and value in self.values:
            self.cells.remove(cell)
            self.values.remove(value)


class SudokuAI():
    """
    Sudoku AI, plays by inference
    """
    def __init__(self, game):
        self.game = game
        self.puzzle = game.puzzle
        self.knowledge = set()
        self.assigned = {}
        self.init_knowledge()

    def init_knowledge(self):
        for i in range(9):
            row_cells = set()
            col_cells = set()
            for j in range(9):
                row_cells.add((i, j))
                col_cells.add((j, i))
            row_s = Sentence(row_cells, {i for i in range(1, 10)})
            col_s = Sentence(col_cells, {i for i in range(1, 10)})
            self.knowledge.add(row_s)
            self.knowledge.add(col_s)
        # TODO:
        # add box knowledge
        for i in [0, 3, 6]:
            for j in [0, 3, 6]:
                cells = set()
                for k in range(3):
                    for v in range(3):
                        cells.add((i+k, j+v))
                s = Sentence(cells, {i for i in range(1, 10)})
                self.knowledge.add(s)

        for i, row in enumerate(self.puzzle):
            for j, val in enumerate(row):
                cell = (i, j)
                if self.game.assigned(cell):
                    self.assigned[cell] = val
                    s = Sentence(cell, [val])
                    self.knowledge.add(s)

    def infer(self, cell, values):
        """
        Perform one round of:
        infer sentences based on puzzles
        """
        for cell in self.assigned:
            for s in self.knowledge:
                s.remove_assigned(cell, self.assigned[cell])
        # TODO:
        # subtract subsets
        for s1, s2 in itertools.
