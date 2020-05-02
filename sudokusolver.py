from sudoku import Sudoku
import random
from collections import defaultdict
import time


class SudokuSolver():
    """
    Defines a Sudoku Solver, to solve a Sudoku game
    via a brute force backtracking method
    """
    def __init__(self, sudoku):
        self.sudoku = sudoku
        self.assignment = self.sudoku.puzzle

    def find_unknowns(self, grid):
        unknowns = []
        for i, row in enumerate(grid):
            for j, val in enumerate(row):
                if val == 0:
                    unknowns.append((i, j))
        return unknowns

    def get_possibles(self, cell):
        all = set(range(1, 10))
        box = set(self.get_box(cell))
        row = set(self.get_row(cell))
        col = set(self.get_col(cell))
        taken = box.union(row.union(col))
        return all - taken

    def get_box(self, cell):
        i, j = cell
        row = i // 3 * 3
        col = j // 3 * 3
        box = []
        for i in range(row, row+3):
            box.extend(self.assignment[i][col:col+3])
        return set(box)

    def get_col(self, cell):
        _, j = cell
        return {row[j] for row in self.assignment}

    def get_row(self, cell):
        i, _ = cell
        return set(self.assignment[i])

    def backtrack(self):
        if self.sudoku.complete():
            return True
        unknowns = self.find_unknowns(self.assignment)
        cell = unknowns.pop()
        possibles = self.get_possibles(cell)
        for pos in possibles:
            self.assignment[cell[0]][cell[1]] = pos
            if self.backtrack():
                print("solved")
                self.sudoku.print_puzzle()
                return
            else:
                self.assignment[cell[0]][cell[1]] = 0
        return None


if __name__ == '__main__':
    with open('puzzles.txt', 'r') as f:
        data = f.read().split()
        puzzles = data[::2]
        solutions = data[1::2]

    for sol, puz in zip(solutions, puzzles):
        game = Sudoku(solution=sol, puzzle=puz)
        solver = SudokuSolver(game)
        start = time.time()
        solver.backtrack()
        end = time.time()
        print(f"{end-start} seconds to solve")
