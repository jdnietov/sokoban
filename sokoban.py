import curses
import os
import time

from copy import deepcopy
from net import Node


class Sokoban:
    WALL = '#'
    PLAYER = '@'
    PLAYERONGOAL = '+'
    BOX = '$'
    BOXONGOAL = '!'
    GOAL = 'o'
    FLOOR = '-'

    _KEYBIND = {
        'KEY_RIGHT': ('move', 'right'),
        'KEY_LEFT': ('move', 'left'),
        'KEY_UP': ('move', 'up'),
        'KEY_DOWN': ('move', 'down'),
        'u': ('reset', '')
    }
    
    def __init__(self, board):
        self.original = board
        self.board = deepcopy(board)

        self.goals = []
        self.boxes = []
        for j in range(len(self.board)):
            row = self.board[j]
            for i in range(len(row)):
                c = row[i]
                if c == Sokoban.GOAL:
                    self.goals.append((j, i))
                elif c == Sokoban.BOX:
                    self.boxes.append((j, i))
                elif c == Sokoban.BOXONGOAL:
                    self.goals.append((j, i))
                    self.boxes.append((j, i))
                elif c == Sokoban.PLAYER:
                    self.pos = (j, i)
                elif c == Sokoban.PLAYERONGOAL:
                    self.goals.append((j, i))
                    self.pos = (j, i)


        self.goals.sort()
        self.boxes.sort()

    def __str__(self):
        s = ''
        for row in self.board:
            for c in row:
                s += c + ' '
            s += '\n'
        s += str(self.pos)
        return s

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(Sokoban.boardstr(self.board))

    def press(self, key):
        if key == os.linesep:
            return False
        bind = Sokoban._KEYBIND[str(key)]
        print(bind)
        if bind[0] == 'move':
            self.move(bind[1])
        elif bind[0] == 'reset':
            print('resetting!')
            self.board = self.original
        
        return True
    
    def move(self, move):
        self.pos = Sokoban.move_board(self, move, False)

    def expand(self):
        boards = [
            Sokoban.move_board(self, 'up'),
            Sokoban.move_board(self, 'down'),
            Sokoban.move_board(self, 'left'),
            Sokoban.move_board(self, 'right'),
        ]

        return {
            'up': Sokoban(boards[0]) if boards[0] is not None else None,
            'down': Sokoban(boards[1]) if boards[1] is not None else None,
            'left': Sokoban(boards[2]) if boards[2] is not None else None,
            'right': Sokoban(boards[3]) if boards[3] is not None else None,
        }


    def heu(self):
        goals = self.goals
        boxes = self.boxes
        # print("goals", self.goals)
        # print("boxes", self.boxes)
        if len(goals) != len(boxes):
            raise Exception('goals and boxes arrays must be of same length')

        h = 0
        for i in range(len(self.goals)):
            goal = goals[i]
            box = boxes[i]

            h += abs(goal[0] - box[0]) + abs(goal[1] - box[1])  

        # print("h", h)      
        return h

    @staticmethod
    def move_board(sokoban, move, immutable=True):
        pos = sokoban.pos
        board = deepcopy(sokoban.board) if immutable else sokoban.board
        y, x = sokoban.pos

        # Horizontal moves
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
                    else:
                        return None if immutable else pos

                    if not immutable:
                        sokoban.boxes[sokoban.boxes.index((y, nx))] = (y, nx+1)
                        sokoban.boxes.sort()

                elif move == 'left' and nx-1 >= 0:
                    if board[y][nx-1] == Sokoban.GOAL:
                        board[y][nx-1] = Sokoban.BOXONGOAL
                    elif board[y][nx-1] == Sokoban.FLOOR:
                        board[y][nx-1] = Sokoban.BOX
                    else:
                        return None if immutable else pos

                    if not immutable:
                        sokoban.boxes[sokoban.boxes.index((y, nx))] = (y, nx-1)
                        sokoban.boxes.sort()

                board[y][nx] = Sokoban.PLAYER
                board[y][x] = Sokoban.GOAL if board[y][x] == Sokoban.PLAYERONGOAL else Sokoban.FLOOR
            
            elif board[y][nx] == Sokoban.BOXONGOAL:
                if move == 'right' and nx+1 <= len(board[y]):
                    if board[y][nx+1] == Sokoban.GOAL:
                        board[y][nx+1] = Sokoban.BOXONGOAL
                    elif board[y][nx+1] == Sokoban.FLOOR:
                        board[y][nx+1] = Sokoban.BOX
                    else:
                        return None if immutable else pos

                    if not immutable:
                        sokoban.boxes[sokoban.boxes.index((y, nx))] = (y, nx+1)
                        sokoban.boxes.sort()

                elif move == 'left' and nx-1 >= 0:
                    if board[y][nx-1] == Sokoban.GOAL:
                        board[y][nx-1] = Sokoban.BOXONGOAL
                    elif board[y][nx-1] == Sokoban.FLOOR:
                        board[y][nx-1] = Sokoban.BOX
                    else:
                        return None if immutable else pos

                    if not immutable:
                        sokoban.boxes[sokoban.boxes.index((y, nx))] = (y, nx-1)
                        sokoban.boxes.sort()

                board[y][nx] = Sokoban.PLAYERONGOAL
                board[y][x] = Sokoban.FLOOR

            elif board[y][nx] == Sokoban.GOAL:
                board[y][nx] = Sokoban.PLAYERONGOAL
                board[y][x] = Sokoban.FLOOR
            
            else:
                return None if immutable else pos
            
            pos = (y, nx)

        # Vertical moves
        elif (move == 'up' and y-1 >= 0) or (move == 'down' and y+1 < len(board)):
            ny = y-1 if move == 'up' else y+1

            if board[ny][x] == Sokoban.FLOOR:
                board[ny][x] = Sokoban.PLAYER
                board[y][x] = Sokoban.GOAL if board[y][x] == Sokoban.PLAYERONGOAL else Sokoban.FLOOR
            
            elif board[ny][x] == Sokoban.GOAL:
                board[ny][x] = Sokoban.PLAYERONGOAL
                board[y][x] = Sokoban.GOAL if board[y][x] == Sokoban.PLAYERONGOAL else Sokoban.FLOOR

            elif board[ny][x] == Sokoban.BOX:
                if move == 'down' and ny+1 < len(board):
                    if board[ny+1][x] == Sokoban.GOAL:
                        board[ny+1][x] = Sokoban.BOXONGOAL
                    elif board[ny+1][x] == Sokoban.FLOOR:
                        board[ny+1][x] = Sokoban.BOX
                    else:
                        return None if immutable else pos

                    if not immutable:
                        sokoban.boxes[sokoban.boxes.index((ny, x))] = (ny+1, x)
                        sokoban.boxes.sort()

                elif move == 'up' and ny-1 >= 0:
                    if board[ny-1][x] == Sokoban.GOAL:
                        board[ny-1][x] = Sokoban.BOXONGOAL
                    elif board[ny-1][x] == Sokoban.FLOOR:
                        board[ny-1][x] = Sokoban.BOX
                    else:
                        return None if immutable else pos

                    if not immutable:
                        sokoban.boxes[sokoban.boxes.index((ny, x))] = (ny-1, x)
                        sokoban.boxes.sort()

                board[ny][x] = Sokoban.PLAYER
                board[y][x] = Sokoban.GOAL if board[y][x] == Sokoban.PLAYERONGOAL else Sokoban.FLOOR

            elif board[ny][x] == Sokoban.BOXONGOAL:
                if move == 'down' and ny+1 < len(board):
                    if board[ny+1][x] == Sokoban.GOAL:
                        board[ny+1][x] = Sokoban.BOXONGOAL
                    elif board[ny+1][x] == Sokoban.FLOOR:
                        board[ny+1][x] = Sokoban.BOX
                    else:   
                        return board if immutable else pos
                elif move == 'up' and ny-1 >= 0:
                    if board[ny-1][x] == Sokoban.GOAL:
                        board[ny-1][x] = Sokoban.BOXONGOAL
                    elif board[ny-1][x] == Sokoban.FLOOR:
                        board[ny-1][x] = Sokoban.BOX
                    else:
                        return board if immutable else pos

                board[ny][x] = Sokoban.PLAYERONGOAL
                board[y][x] = Sokoban.FLOOR

            else:
                return None if immutable else pos

            pos = (ny, x)
        
        return board if immutable else pos

    @staticmethod
    def parse(rle):
        i, x = 0, 0
        pos = (0, 0)
        matrix = [[]]
        goals = []
        boxes = []

        while i < len(rle):
            c = rle[i]
            if c.isdigit():
                while rle[i+1].isdigit():
                    i += 1
                    c += rle[i]
                
                n = int(c)
                i += 1
                t = rle[i]

                for _ in range(0, n):
                    matrix[x].append(t)
                
            else:
                if c == '|':
                    matrix.append([])
                    x += 1

                else:
                    matrix[x].append(c)

            i += 1
        
        return matrix

    @staticmethod
    def boardstr(board):
        s = ''
        for row in board:
            for c in row:
                s += c + ' '
            s += '\n'
        return s

levels = [
  '11#|#@-$5-o#|11#',
  '7#|#--o--#|#-$o--#|#--#$-#|#-$#--#|#--o$-#|#@-o--#|7#',
  '8#|#--@#-o#|#-3#--#|#-#o#$-#|#3-#--#|3#$#--#|--#-$--#|--#--o-#|--#--3#|--4#',
]

def main(win):
    win.nodelay(True)
    key=""
    win.clear()
    
    sokoban = Sokoban(Sokoban.parse(levels[1]))
    root = Node(sokoban)
    win.addstr('Loading...')
    node = root.astar()
    # win.clear()

    if node is None:
        win.addstr('Puzzle had no solution.')
    else:
        win.addstr('Solution:\n')
        stack = node.branch()

        while stack:
            try:
                key = win.getkey()

                if key == os.linesep:
                    break

                win.clear()
                win.addstr(str(stack.pop()))
            except Exception as e:
                pass

    # win.addstr(str(sokoban))
    # while 1:          
    #     try:                 
    #         key = win.getkey()
           
    #         if not sokoban.press(str(key)):
    #             break

    #         win.clear()
    #         win.addstr(str(sokoban))
    #         win.addstr('\n')
    #         win.addstr(str(sokoban.boxes))
    #         win.addstr('\n')
    #         win.addstr(str(sokoban.goals))
    #         win.addstr('\n')
    #         win.addstr(str(sokoban.heu()))
    #     except Exception as e:  
    #     #    No input   
    #        pass 

curses.wrapper(main)



# DEBUGGING MAIN
# sokoban = Sokoban(Sokoban.parse(levels[1]))
# print(sokoban)
# sokoban.move('right')
# print(sokoban.heu())
# sokoban.move('right')
# print(sokoban.heu())
# sokoban.move('right')
# print(sokoban.heu())
# sokoban.move('right')
# print(sokoban.heu())
# sokoban.move('right')
# print(sokoban.heu())
# sokoban.press('u')
# print(sokoban)

# for key, value in sokoban.expand().items():
#     if value is not None:
#         print(key, '\n', Sokoban.boardstr(value))
#     else:
#         print("can't move", key)

# sokoban = Sokoban(Sokoban.parse(levels[2]))
# root = Node(sokoban)
# print(sokoban.goals)
# print(sokoban.boxes)

# node = root.astar()
# if node is None:
#     print('Puzzle had no solution.')
# else:
#     print('Solution:')
#     node.branch()