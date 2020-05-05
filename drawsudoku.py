from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
sudoku = ".79.8.5.2..8.9.....4.57..38.....8..3463..5....2.4...5..3........543.....6..7....."
sudoku1 = "379684512518293764246571938795168423463925187821437659137846295954312876682759341"
sudoku = sudoku1


def draw_sudoku(board_string, board_string2=None):
    empty = [".", "0"]
    board1 = [char if char not in empty else ' ' for char in board_string]
    if board_string2:
        board2 = [char if char not in empty else ' ' for char in board_string2]
    else:
        board2 = board1
    im = Image.new('RGB', (900, 900), color='white')
    d = ImageDraw.Draw(im)
    fnt = ImageFont.truetype('OpenSans-Regular.ttf', 60)
    d.rectangle([(0, 0), (900, 900)], outline='black', fill=None, width=9)
    for i in range(1, 9):
        w = 3
        if i % 3 == 0:
            w = 9
        d.line([(0, i*100), (900, i*100)], fill='black', width=w)
        d.line([(i*100, 0), (i*100, 900)], fill='black', width=w)

    positions = []
    for i in range(0, 9):
        for j in range(0, 9):
            W, H = j*100 + 30, i*100 + 10
            positions.append((W, H))
    for char1, char2, pos in zip(board1, board2, positions):
        fill = 'black'
        if char2 != char1:
            fill = 'red'
        d.text(pos, char2, font=fnt, fill=fill)
    im.save(f'sudoku{datetime.now().strftime("%f")}.png')
    im.show()


draw_sudoku(sudoku, sudoku1)
