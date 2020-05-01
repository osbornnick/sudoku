from sudoku import Sudoku, SudokuAI

with open('puzzles.txt', 'r') as f:
    data = f.read().split()
    puzzles = data[::2]
    solutions = data[1::2]

for sol, puz in zip(solutions, puzzles):
    game = Sudoku(solution=sol, puzzle=puz)
    ai = SudokuAI(game)
    ai.solve()
