from sudokuengine import *

with open('puzzles.txt', 'r') as f:
    data = f.read().split()
    puzzles = data[::2]
    solutions = data[1::2]


for sol, puz in zip(solutions[1:2], puzzles[1:2]):
    game = Sudoku(solution=sol, puzzle=puz)
    game.print_puzzle()
    ai = SudokuAI(game)
    ai.axioms()
    for _ in range(10):
        ai.infer()
        print(f"progress: {game.progress()}")
        print(len(ai.knowledge))
        game.print_puzzle()
    for s in ai.knowledge:
        print(s)
