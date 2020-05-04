from sudoku import Sudoku
from itertools import permutations


class Sentence():
    """
    A Sentence to build the knowledge base
    for a Sudoku solving knowledge based agent
    """
    def __init__(self, boxes, values):
        self.boxes = set(boxes)
        self.values = list(values)

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
        vals = self.values.copy()
        for i in other.values:
            if i in self.values:
                vals.remove(i)
        boxes = self.boxes - other.boxes
        return Sentence(boxes, vals)

    def peer(self, other):
        if not isinstance(other, Sentence):
            raise ValueError(f"{other.__repr__()} is not a Sentence")
        if self.boxes.intersection(other.boxes):
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


class SudokuAI():
    def __init__(self, game):
        self.game = game
        self.knowledge = []

    def axioms(self):
        # logical sentences from row + column clauses
        for i in range(9):
            row_cells = set()
            col_cells = set()
            for j in range(9):
                row_cells.add((i, j))
                col_cells.add((j, i))
            row_s = Sentence(row_cells, [i for i in range(1, 10)])
            col_s = Sentence(col_cells, [i for i in range(1, 10)])
            self.knowledge.append(row_s)
            self.knowledge.append(col_s)

        # logical sentences from box clause
        for i in [0, 3, 6]:
            for j in [0, 3, 6]:
                cells = set()
                for k in range(3):
                    for v in range(3):
                        cells.add((i+k, j+v))
                s = Sentence(cells, [i for i in range(1, 10)])
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
        for s1, s2 in permutations(self.knowledge, 2):
            if s1.peer(s2):
                s3 = s1 - s2
                self.knowledge.append(s3)

        self.clean_knowledge()

        for sentence in self.knowledge:
            if sentence.conclusive():
                i, j = list(sentence.boxes)[0]
                self.game.puzzle[i][j] = sentence.values[0]

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
            print(len(self.knowledge))
