from sudokuengine import *

with open('puzzles.txt', 'r') as f:
    data = f.read().split()
    puzzles = data[::2]
    solutions = data[1::2]

for sol, puz in zip(solutions[:1], puzzles[:1]):
    game = Sudoku(solution=sol, puzzle=puz)
    game.print_puzzle()
    ai = SudokuAI(game)
    ai.solve()
    # ai.axioms()
    # ai.infer()
    # ai.infer()
    # for s in ai.knowledge:
    #     print(s)
