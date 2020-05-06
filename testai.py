from sudokuengine import *

with open('puzzles.txt', 'r') as f:
    data = f.read().split()
    puzzles = data[::2]
    solutions = data[1::2]


for sol, puz in zip(solutions, puzzles):
    game = Sudoku(solution=sol, puzzle=puz)
    game.print_puzzle()
    ai = SudokuAI(game)
    ai.solve()
    # ai.axioms()
    # for i in range(25):
    #     print(f"step {i}")
    #     print(game.progress())
    #     ai.infer()
    #     game.print_puzzle()
    # for s in ai.knowledge:
    #     if (8, 6) in s.boxes:
    #         print(s)
    print(game.grid_to_string(game.puzzle))
