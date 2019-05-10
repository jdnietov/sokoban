import curses
import os

from copy import deepcopy

class Sokoban:
    _WALL = '#'
    _PLAYER = '@'
    _PLAYERONGOAL = '+'
    _BOX = '$'
    _BOXONGOAL = '*'
    _GOAL = '.'
    _FLOOR = '-'

    _KEYBIND = {
        'KEY_RIGHT': ('move', 'right'),
        'KEY_LEFT': ('move', 'left'),
        'KEY_UP': ('move', 'up'),
        'KEY_DOWN': ('move', 'down')
    }
    _WALKABLE = set(['-', '.'])

    def __init__(self, rle):
        self.rle = rle
        self.board, self.pos = Sokoban.parseLevelString(rle)

    def __str__(self):
        s = ''
        for row in self.board:
            for c in row:
                s += c + ' '
            s += '\n'
        s += str(self.pos)
        return s

    def press(self, key):
        if key == os.linesep:
            return False

        bind = Sokoban._KEYBIND[str(key)]
        if bind[0] == 'move':
            self.move(bind[1])
        
        return True
    
    def move(self, move):
        self.pos = Sokoban.move_board(self.board, self.pos, move, False)

    @staticmethod
    def move_board(board, pos, move, immutable=True):
        if immutable:
            board = deepcopy(board)
        y, x = pos

        nx = {
            'left': x-1 if x-1 >= 0 else None,
            'right': x+1 if x+1 <= len(board[x]) else None
        }.get(move, x)

        ny = {
            'up': y-1 if y-1 >= 0 else None,
            'down': y+1 if y+1 <= len(board) else None
        }.get(move, y)
        
        if ny == y and nx == x:
            raise Exception('Move type is not recognized')
        if ny is None or nx is None:
            return None
        
        if move == 'up' or move == 'down':
            if board[ny][x] == '-':
                n = board[ny][x]
                board[y][x] = n
                board[ny][x] = Sokoban._PLAYER
                pos = (ny, x)
        else:
            if board[y][nx] == '-':
                n = board[y][nx]
                board[y][x] = n
                board[y][nx] = Sokoban._PLAYER
                pos = (y, nx)
        
        if immutable:
            return board
        else:
            return pos

    @staticmethod
    def parseLevelString(rle):
        i, j = 0, 0
        x = 0
        pos = (0, 0)
        matrix = [[]]

        while i < len(rle):
            c = rle[i]

            if c.isdigit():
                while rle[i+1].isdigit():
                    i += 1
                    c += rle[i]
                
                n = int(c)
                i += 1
                t = rle[i]

                for j in range(0, n):
                    matrix[x].append(t)
                    j += 1
                
            else:
                if c == '|':
                    matrix.append([])
                    x += 1
                    j = 0

                else:
                    if c == '@':
                        pos = (x, j)
                    matrix[x].append(c)
                    j += 1

            i += 1
        
        return (matrix, pos)

levels = [
  '11#|#@-$5-.#|11#',
  '7#|#--.--#|#-$.--#|#--#$-#|#-$#--#|#--.$-#|#@-.--#|7#',
  '8#|#--@#-.#|#-3#--#|#-#.#$-#|#3-#--#|3#$#--#|--#-$--#|--#--.-#|--#--3#|--4#'
]

def main(win):
    sokoban = Sokoban(levels[1])
    win.nodelay(True)
    key=""
    win.clear()
    win.addstr(str(sokoban))
    while 1:          
        try:                 
            key = win.getkey()
           
            if not sokoban.press(str(key)):
                break

            win.clear()
            win.addstr(str(sokoban))
        except Exception as e:  
           # No input   
           pass 

curses.wrapper(main)