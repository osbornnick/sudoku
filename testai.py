from sudokuengine import *

with open('puzzles.txt', 'r') as f:
    data = f.read().split()
    puzzles = data[::2]
    solutions = data[1::2]


for sol, puz in zip(solutions[2:3], puzzles[2:3]):
    game = Sudoku(solution=sol, puzzle=puz)
    game.print_puzzle()
    ai = SudokuAI(game)
    # ai.solve()
    ai.axioms()
    for i in range(410):
        print(f"step {i}")
        print(game.progress())
        ai.infer()
        game.print_puzzle()
    for s in ai.knowledge:
        cells = {(8, 6), (8, 7)}
        if cells.intersection(s.boxes):
            print(s)
    print(game.grid_to_string(game.puzzle))
