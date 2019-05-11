import curses
import os

from copy import deepcopy

class Sokoban:
    WALL = '#'
    PLAYER = '@'
    PLAYERONGOAL = '+'
    BOX = '$'
    BOXONGOAL = '!'
    GOAL = '.'
    FLOOR = '-'

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

        if (move == 'right' and x+1 < len(board[y])) or (move == 'left' and x-1 >= 0):
            nx = x+1 if move == 'right' else x-1

            if board[y][nx] == Sokoban.FLOOR:
                board[y][nx] = Sokoban.PLAYER
                board[y][x] = Sokoban.GOAL if board[y][x] == Sokoban.PLAYERONGOAL else Sokoban.FLOOR

            elif board[y][nx] == Sokoban.BOX:
                if move == 'right' and nx+1 <= len(board[y]):
                    if board[y][nx+1] == Sokoban.GOAL:
                        board[y][nx+1] = Sokoban.BOXONGOAL
                    elif board[y][nx+1] == Sokoban.FLOOR:
                        board[y][nx+1] = Sokoban.BOX
                elif move == 'left' and nx-1 >= 0:
                    if board[y][nx-1] == Sokoban.GOAL:
                        board[y][nx-1] = Sokoban.BOXONGOAL
                    elif board[y][nx-1] == Sokoban.FLOOR:
                        board[y][nx-1] = Sokoban.BOX

                board[y][nx] = Sokoban.PLAYER
                board[y][x] = Sokoban.FLOOR

            elif board[y][nx] == Sokoban.GOAL:
                board[y][nx] = Sokoban.PLAYERONGOAL
                board[y][x] = Sokoban.FLOOR
            
            else:
                return board if immutable else pos
            
            pos = (y, nx)

        # TODO: down is not working
        elif (move == 'up' and y-1 >= 0) or (move == 'down' and y+1 < len(board)):
            ny = y-1 if move == 'up' else y+1

            if board[ny][x] == Sokoban.FLOOR:
                board[ny][x] = Sokoban.PLAYER
                board[y][x] = Sokoban.FLOOR
            
            elif board[ny][x] == Sokoban.GOAL:
                board[ny][x] = Sokoban.PLAYERONGOAL
                board[y][x] = Sokoban.GOAL if board[y][x] == Sokoban.PLAYERONGOAL else Sokoban.FLOOR

            elif board[ny][x] == Sokoban.BOX: 
                if move == 'down' and ny+1 < len(board):
                    if board[ny+1][x] == Sokoban.GOAL:
                        board[ny+1][x] = Sokoban.BOXONGOAL
                    elif board[ny+1][x] == Sokoban.FLOOR:
                        board[ny+1][x] = Sokoban.BOX
                elif move == 'up' and ny-1 >= 0:
                    if board[ny-1][x] == Sokoban.GOAL:
                        board[ny-1][x] = Sokoban.BOXONGOAL
                    elif board[ny-1][x] == Sokoban.FLOOR:
                        board[ny-1][x] = Sokoban.BOX

                board[ny][x] = Sokoban.PLAYER
                board[y][x] = Sokoban.FLOOR

            else:
                return board if immutable else pos

            pos = (ny, x)
        
        return board if immutable else pos

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

# DEBUGGING MAIN
# def main():
#     sokoban = Sokoban(levels[0])

#     print(sokoban)
#     sokoban.move('right')
#     print(sokoban)
#     sokoban.move('right')
#     print(sokoban)
#     sokoban.move('right')
#     print(sokoban)

# main()