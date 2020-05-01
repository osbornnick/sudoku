from sudoku import Sudoku, SudokuAI

board = [
         [6, 7, 2, 1, 4, 5, 3, 9, 8],
         [1, 4, 5, 9, 8, 3, 6, 7, 2],
         [3, 8, 9, 7, 6, 2, 4, 5, 1],
         [2, 6, 3, 5, 7, 4, 8, 1, 9],
         [9, 5, 8, 6, 2, 1, 7, 4, 3],
         [7, 1, 4, 3, 9, 8, 5, 2, 6],
         [5, 9, 7, 2, 3, 6, 1, 8, 4],
         [4, 2, 6, 8, 1, 7, 9, 3, 5],
         [8, 3, 1, 4, 5, 9, 2, 6, 7]
]

puzzle = [
         [6, 7, 2, 0, 4, 0, 3, 9, 8],
         [0, 0, 5, 9, 8, 3, 0, 0, 2],
         [3, 0, 9, 7, 6, 0, 0, 5, 1],
         [2, 0, 0, 5, 0, 4, 8, 0, 9],
         [0, 5, 8, 6, 2, 1, 7, 4, 0],
         [7, 0, 4, 3, 0, 8, 0, 0, 6],
         [5, 9, 0, 0, 3, 6, 1, 0, 4],
         [4, 0, 0, 8, 1, 7, 9, 0, 0],
         [8, 3, 1, 0, 5, 0, 2, 6, 7]
]

# export = ""
# for row in puzzle:
#     export += " ".join(str(i) for i in row) + " "
# print(export)
game = Sudoku(solution=board, puzzle=puzzle)
ai = SudokuAI(game)
game.print_puzzle()
ai.infer()
print("-")
ai.print_puzzle()
