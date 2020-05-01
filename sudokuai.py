import itertools





class Sentence():
    """
    Logical statement about a Sudoku game
    A sentence consists of a set of board cells,
    and a set of possible values of those cells.
    """
    def __init__(self, cells, values):
        self.cells = set(cells)
        self.values = list(values)

    def __repr__(self):
        return f"Sentence({self.cells}, {self.values})"

    def __eq__(self, other):
        if isinstance(other, Sentence):
            return self.cells == other.cells and self.values == other.values
        else:
            return False

    def __hash__(self):
        return hash(self.__repr__())

    def __str__(self):
        return f"{self.cells} <> {self.values}"

    def size(self):
        return (len(self.cells), len(self.values))

    def conclusive(self):
        """
        Test if a sentence can assign the value of a cell
        """
        if len(self.cells) == 1 and len(self.values) == 1:
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
        self.knowledge = []
        self.assigned = {}
        self.init_knowledge()

    def init_knowledge(self):
        # logical sentences from row + column clauses
        for i in range(9):
            row_cells = set()
            col_cells = set()
            for j in range(9):
                row_cells.add((i, j))
                col_cells.add((j, i))
            row_s = Sentence(row_cells, {i for i in range(1, 10)})
            col_s = Sentence(col_cells, {i for i in range(1, 10)})
            self.knowledge.append(row_s)
            self.knowledge.append(col_s)

        # logical sentences from box clause
        for i in [0, 3, 6]:
            for j in [0, 3, 6]:
                cells = set()
                for k in range(3):
                    for v in range(3):
                        cells.add((i+k, j+v))
                s = Sentence(cells, {i for i in range(1, 10)})
                self.knowledge.append(s)

        # add cells known at beginning to knowledge
        for i, row in enumerate(self.puzzle):
            for j, val in enumerate(row):
                cell = (i, j)
                if self.game.assigned(cell):
                    self.assigned[cell] = val

    def solve(self):
        """
        Perform all possible inference steps
        """
        while not self.game.complete():
            for sentence in self.knowledge:
                if sentence.conclusive():
                    cell = list(sentence.cells)[0]
                    value = sentence.values[0]
                    self.assigned[cell] = value

            for cell in self.assigned:
                for s in self.knowledge:
                    s.remove_assigned(cell, self.assigned[cell])

            for s1, s2 in list(itertools.combinations(self.knowledge, 2)):
                # subset
                if s1.cells and s1 != s2 and s1.cells.issubset(s2.cells):
                    vals = [val for val in s2.values if val not in s1.values]
                    s = Sentence(s2.cells - s1.cells, vals)
                    if s not in self.knowledge:
                        self.knowledge.append(s)
                # intersection
                # if s1.cells and s1 != s2 and s1.cells.intersection(s2.cells):
                #     cells = s1.cells.union(s2.cells)
                #     values = s1.values + s2.values
                #     val1 = [val for val in values if val not in s1.values]
                #     val2 = [val for val in values if val not in s2.values]
                #     sa = Sentence(cells - s1.cells, val1)
                #     sb = Sentence(cells - s2.cells, val2)
                #     if sa not in self.knowledge:
                #         self.knowledge.append(sa)
                #     if sb not in self.knowledge:
                #         self.knowledge.append(sb)

            for cell in self.assigned:
                i, j = cell
                self.puzzle[i][j] = self.assigned[cell]
            self.knowledge = list(set(self.knowledge))
            self.game.print_puzzle()
            print('-')
