from itertools import permutations
from sudoku import Sudoku


class Sentence():
    """
    A Sentence to build the knowledge base
    for a Sudoku solving knowledge based agent
    """

    def __init__(self, boxes, values):
        self.boxes = set(boxes)
        self.values = set(values)

    def __repr__(self):
        return f"Sentence{self.boxes, self.values}"

    def __eq__(self, other):
        if not isinstance(other, Sentence):
            return False
        if self.boxes == other.boxes and self.values == other.values:
            return True
        return False

    def __hash__(self):
        return hash((tuple(self.boxes), tuple(self.values)))

    def __str__(self):
        return f"{self.boxes} -> {self.values}"

    def __sub__(self, other):
        """
        return a new Sentence instance
        encoding list differences of two Sentences values/boxes
        """
        if not isinstance(other, Sentence):
            raise ValueError(f"{other.__repr__()} is not a sentence")
        vals = self.values - other.values
        boxes = self.boxes - other.boxes
        return Sentence(boxes, vals)

    def peer(self, other):
        """
        return True if self and other are peers otehrwise false
        they are peers if we can infer a new sentence from their overlap
        """
        if not isinstance(other, Sentence):
            raise ValueError(f"{other.__repr__()} is not a Sentence")
        if len(self.boxes & other.boxes) == len(self.values & other.values):
            return True
        return False

    def empty(self):
        if self.boxes and self.values:
            return False
        return True

    def conclusive(self):
        if len(self.boxes) == 1 and len(self.values) == 1:
            return True
        return False

    def remove_assigned(self, other):
        self.boxes = self.boxes - other.boxes
        for i in other.values:
            if i in self.values:
                self.values.remove(i)


class SudokuAI():
    def __init__(self, game):
        self.game = game
        self.knowledge = []

    def axioms(self):
        # logical sentences from row + column clauses
        allvals = [i for i in range(1, 10)]
        for i in range(9):
            row_cells = set()
            col_cells = set()
            for j in range(9):
                row_cells.add((i, j))
                col_cells.add((j, i))
            row_s = Sentence(row_cells, allvals)
            col_s = Sentence(col_cells, allvals)
            self.knowledge.append(row_s)
            self.knowledge.append(col_s)

        # logical sentences from box clause
        for i in [0, 3, 6]:
            for j in [0, 3, 6]:
                cells = set()
                for k in range(3):
                    for v in range(3):
                        cells.add((i+k, j+v))
                s = Sentence(cells, allvals)
                self.knowledge.append(s)

        # add cells known at beginning to knowledge
        for i, row in enumerate(self.game.puzzle):
            for j, val in enumerate(row):
                cell = (i, j)
                if self.game.assigned(cell):
                    self.knowledge.append(Sentence({cell}, [val]))

    def infer(self):
        """
        Make a round of inferences based on current knowledge
        """
        # TODO: implement better logic
        # take only differences where cell + value overlap same amount

        # for s1, s2 in permutations(self.knowledge, 2):
        #     if s1.peer(s2):
        #         s3 = s1 - s2
        #         self.knowledge.append(s3)

        for s1 in self.knowledge:
            if s1.conclusive():
                i, j = list(s1.boxes)[0]
                self.game.puzzle[i][j] = s1.values[0]
                for s2 in self.knowledge:
                    if s1.peer(s2) and s1 != s2:
                        s2.remove_assigned(s1)

        self.clean_knowledge()

    def clean_knowledge(self):
        self.knowledge = list(set(self.knowledge))
        self.knowledge = [s for s in self.knowledge if not s.empty()]

    def solve(self):
        """
        Complete inference rounds until game solved
        """
        self.axioms()
        while not self.game.complete():
            self.infer()
        self.game.print_puzzle()
