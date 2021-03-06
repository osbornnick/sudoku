from itertools import combinations
from sudoku import Sudoku
from collections import Counter


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
        a = tuple(sorted(self.boxes))
        b = tuple(sorted(self.values))
        return hash((a, b))

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

    def remove_assigned(self, other):
        self.boxes -= other.boxes
        self.values -= other.values

    def peer(self, other):
        """
        return True if self and other are peers otehrwise false
        they are peers if we can infer a new sentence from their overlap
        len of box overlap and value overlap must match
        """
        if not isinstance(other, Sentence):
            raise ValueError(f"{other.__repr__()} is not a Sentence")
        if len(self.boxes & other.boxes) == len(self.values & other.values):
            return True
        return False

    def neighbor(self, other):
        if not isinstance(other, Sentence):
            raise ValueError(f"{other.__repr__()} is not a Sentence")
        return bool(self.boxes.intersection(other.boxes))

    def empty(self):
        return not (self.boxes and self.values)

    def conclusive(self):
        return (len(self.boxes) == 1) and (len(self.values) == 1)

    def single(self):
        return (len(self.boxes) == 1)

    def multiple(self):
        return (len(self.boxes) > 1)


class SudokuAI():
    def __init__(self, game):
        self.game = game
        self.knowledge = []

    def axioms(self):
        # logical sentences from row + column clauses
        allvals = {i for i in range(1, 10)}
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
                    self.knowledge.append(Sentence({cell}, {val}))
                else:
                    self.knowledge.append(Sentence({cell}, allvals))

    def infer(self):
        """
        Make a round of inferences based on current knowledge
        """
        updated = False
        # remove assignments
        for s1 in self.knowledge:
            if s1.conclusive():
                i, j = list(s1.boxes)[0]
                if not self.game.puzzle[i][j]:
                    self.game.puzzle[i][j] = list(s1.values)[0]
                for s2 in self.knowledge:
                    if s1.peer(s2) and s1 != s2:
                        s2.remove_assigned(s1)
                        updated = True

        # infer new sentences
        for s1, s2 in combinations(self.knowledge, 2):
            if s1.peer(s2):
                s3 = s1 - s2
                if s3 not in self.knowledge and not s3.empty():
                    self.knowledge.append(s3)
                updated = True

        # update neighbors and find hidden singles
        new_sentences = set()
        for s1 in self.knowledge:
            if s1.single() and not s1.conclusive():
                for s2 in self.knowledge:
                    if s1.neighbor(s2):
                        s1.values = s1.values.intersection(s2.values)
                    updated = True

        for s1 in self.knowledge:
            if s1.multiple():
                components = set()
                for s2 in self.knowledge:
                    if s2.single() and s2.boxes.issubset(s1.boxes):
                        components.add(s2)
                if components:
                    cells = {box for s in components for box in s.boxes}
                if cells == s1.boxes:
                    new_sents = self.hidden_single(components)
                    if new_sents:
                        new_sentences.update(new_sents)

        self.knowledge.extend(list(new_sentences))

        self.clean_knowledge()

        if not updated:
            print("no updates made to knowledge")

    def hidden_single(self, sentences):
        out = set()
        c = Counter()
        for s in sentences:
            c.update(s.values)
        for val in c:
            if c[val] == 1:
                for s1 in sentences:
                    if val in s1.values:
                        s2 = Sentence(s1.boxes, {val})
                        if s2 not in self.knowledge:
                            out.add(s2)
        return out

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
