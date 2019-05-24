import curses
import os
import sys

from random import randint
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

    def stuck(self):
        for box in self.boxes:
            y, x = box
            ul = self.board[y-1][x] == Sokoban.WALL and self.board[y][x-1] == Sokoban.WALL
            ur = self.board[y-1][x] == Sokoban.WALL and self.board[y][x+1] == Sokoban.WALL
            dl = self.board[y+1][x] == Sokoban.WALL and self.board[y][x-1] == Sokoban.WALL
            dr = self.board[y+1][x] == Sokoban.WALL and self.board[y][x+1] == Sokoban.WALL
            if ul or ur or dl or dr:
                return True
        return False

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

        if len(goals) != len(boxes):
            raise Exception('goals and boxes arrays must be of same length')

        h = 0
        for i in range(len(self.goals)):
            goal = goals[i]
            box = boxes[i]

            h += abs(goal[0] - box[0]) + abs(goal[1] - box[1])
        
        # return h if not self.stuck() else sys.maxsize
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

                elif move == 'left' and nx-1 >= 0:
                    if board[y][nx-1] == Sokoban.GOAL:
                        board[y][nx-1] = Sokoban.BOXONGOAL
                    elif board[y][nx-1] == Sokoban.FLOOR:
                        board[y][nx-1] = Sokoban.BOX
                    else:
                        return None if immutable else pos

                sokoban.boxes[sokoban.boxes.index((y, nx))] = (y, nx-1 if move == 'left' else nx+1)
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

                elif move == 'left' and nx-1 >= 0:
                    if board[y][nx-1] == Sokoban.GOAL:
                        board[y][nx-1] = Sokoban.BOXONGOAL
                    elif board[y][nx-1] == Sokoban.FLOOR:
                        board[y][nx-1] = Sokoban.BOX
                    else:
                        return None if immutable else pos

                sokoban.boxes[sokoban.boxes.index((y, nx))] = (y, nx-1 if move == 'left' else nx+1)
                sokoban.boxes.sort()

                board[y][nx] = Sokoban.PLAYERONGOAL
                board[y][x] = Sokoban.GOAL if board[y][x] == Sokoban.PLAYERONGOAL else Sokoban.FLOOR

            elif board[y][nx] == Sokoban.GOAL:
                board[y][nx] = Sokoban.PLAYERONGOAL
                board[y][x] = Sokoban.GOAL if board[y][x] == Sokoban.PLAYERONGOAL else Sokoban.FLOOR
            
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

                elif move == 'up' and ny-1 >= 0:
                    if board[ny-1][x] == Sokoban.GOAL:
                        board[ny-1][x] = Sokoban.BOXONGOAL
                    elif board[ny-1][x] == Sokoban.FLOOR:
                        board[ny-1][x] = Sokoban.BOX
                    else:
                        return None if immutable else pos

                sokoban.boxes[sokoban.boxes.index((ny, x))] = (ny-1 if move == 'up' else ny+1, x)
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

                sokoban.boxes[sokoban.boxes.index((ny, x))] = (ny-1 if move == 'up' else ny+1, x)
                sokoban.boxes.sort()

                board[ny][x] = Sokoban.PLAYERONGOAL
                board[y][x] = Sokoban.GOAL if board[y][x] == Sokoban.PLAYERONGOAL else Sokoban.FLOOR
                #board[y][x] = Sokoban.FLOOR

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
  '11#|#ooo$@-$5-o#|11#',
  '11#|#@-$5-o#|11#',
  '--3#|3#o#|#o$$##|##@$o#|-5#',
  '3-4#|3-#--#|3-#--#|3-#-$##|5#--3#|#-!5-+#|#3-6#|5#',
  '7#|#--o--#|#-$o--#|#--#$-#|#-$#--#|#--o$-#|#@-o--#|7#',
  '8#|#--@#-o#|#-3#--#|#-#o#$-#|#3-#--#|3#$#--#|--#-$--#|--#--o-#|--#--3#|--4#',
  '5#|#3-7#|#-#-##--oo#|#-$--$-o!o#|3#--#-!oo#|--#-7#|--#-#4-#|--#-#-$$-#|--#-$-$@-#|--#3-4#|--5#',
  '8#|#@-#3-#|##$#3-#|#--#3-#|#--##$##|#-o--o-#|#--#3-#|8#',
  '-6#|##4-#|#--##$#|#5-3#|##-#-oo+#|-#$7#|-#-#5-#|##-#-#$#-#|#--#5-#|#5-4#|#3-3#|5#',
  '7#|#3o$-##|#3o3-#|##-$-$-#|-3#-3#|-#@$-$-#|-#-$3-#|-#4-##|-6#',
  '12#|#@-#--$-3o#|##$#$-$-3o#|#3-$6-#|#9-$#|8#3-#|7-5#',
  '6#|#o#-@#|#o#$-##|#o#-$-#|#-$3-#|#3-3#|5#',
  '9#|#3o$3-#|#3o$3-#|5#-$##|4-#--#|4-#$-#|4-#-$#|4-#$-#|4-#@-#|4-4#',
  '12-5#|12-#3-#|-12#-#-#|-#o10-!--#|-12#-3#|5-#3-#--#-#|5-#-$@#--#-#|5-#3-#--#-#|8#$4#-3#|#--!9-!--#|#-#-4#--3#-#-#|#3-#--#o-#-#3-#|5#--4#-5#',
  '4-5#|5#3o#|#-$5-#|#3-#$--#|5#--##|#-@-#$$#|#3-#--#|#3-#$-##|##--$3-#|#3o#3-#|9#',
  '10#|#o#4-@-#|#o#$$#-$-#|#o#--#$-##|#o$--#-$#|#o#--#--#|#o#5-#|#4-#--#|#--6#|4#',
  '7#|#o#3-#|#o#-$-#|#@--$-#|#o-$$-#|#o#-$-#|#o#3-#|7#',
  '6#|#4-#|#-$--#|#-$@-#|#-#!##-4#|#-#o##-#--#|#--!-#-#$-#|#-#o-#-#--#|#-#o-#-#-3#|#-#o-3#3-#|#8-$-#|3#--7#|--4#',
  '3-4#|3-#--7#|3-#3-$4-#|3-#--3#-$-#|-3#--#-#$--#|-#@3-#-#-$-#|-##$$-#-#--$#|##-$--#-#--o#|#o-#--#-5#|#5o#|#-o4#|4#',
  '12#|#@9-#|#--$-$-$-$-#|#--##$3#$-#|#3-6o-#|12#',
  '-7#|##-o--@#|#-o-#o-#|#-$##--#|#-$--$-#|#--##--#|8#',
  '10#|#3-o4-#|#-##$3#-#|#-#3-o#-#|#-#-##-#-#|#-#-@#$$-#|#-4#-#-#|#--o3-#-#|#-#$#--#-#|#--!3-#o#|10#',
  '5#--5#|#3-#--#3-#|#-@-#--#-$-#|#3-#--#3-#|##$##--#3-#|#3-#--#3-#|#3-5#$##|#3-o!oo3-#|#3-4#3-#|#3-4#3-#|12#',
  '11#|#@3-#4-#|#-$-o$o-$-#|#4-#4-#|#-o-3#-o-#|##$##!##$##|#-o-3#-o-#|#4-#4-#|#-$-o$o-$-#|#4-#4-#|11#',
  '-4#|-#--4#|-#5-#|##-##--#|#--##-##|#5-o#|5#-##|#@3-$#|4#--#|3-4#',
  '--4#|3#--#|#3-$##|#3-$o#|4#+-#|3-4#',
  '--4#--4#|3#--#--#--#|#3-$4#$-3#|#3-$o!6-#|4#o@##-#o--#|3-5#3-3#|7-5#',
  '-8#|-#--##--##|##7-#|#-!-3#--#|#-!-#-#--#|#-!-#-#$-#|#-!-#-#--#|#-!-#-4#|#@!-#|#-o-#|5#',
  '5#|#oo@#|#oo-#|#oo-5#|#3o#3-#--5#|##-##$#-4#3-#|-#-$5-#-$-#-#|-#4-#-$6-#|-6#-$#$$4#|6-#-$-$-#|6-#5-#|6-7#',
  '5#-9#|#3-#-#3-#3-#|#-#-3#$#3-$-#|#4-$5-#--#|3#$3#$5#-#|--#--o--#3-#-#|--#$5o-$3-#|--#--o$-#3-3#|--3#o7#|4-#o#|4-#$#|4-#@#|4-3#',
  '10#|#@--$-o--##|#3-##-#--#|##--o#-##-#|-#$$##-o#-#|-#-o-##$#-#|-#3-o-$--#|-##$##-$--#|-#-o##3-##|-#-o3-3#|-7#',
  '9-7#|4-6#5-3#|-4#4-$7-#|-#6-#-$--3#$##|-#6-#o#--#4-#|3#$5#o4#$3-#|#@5-5o$4-##|4#$-3#o5#--#|3-#--#-#o#3-##$#|3-4#-#-3#-#--#|8-#3-3#-##|8-#$#5-#|8-#3-5#|8-5#',
  '8#|#6-#|#--$3-#|#-$$-$-#|#-@##$-#|3#--$-#|#3o-$-#|#4o3#|6#',
  '9#|#-5o-#|#-$3#$-#|#3-$3-#|#-$-@-$-#|4#$4#|#--$-$--#|#7-#|#-$3#$-#|#-5o-#|9#',
  '6-5#|6-#3-4#|7#-#o3-#|#--#--#-##3-#|#-$3-#--$--##|#--##-4#$-#|#@-#3-o-o--#|#-$#-4#-3#|#-$5-$3o#|13#'
]

def main(win):
    win.nodelay(True)
    key=""
    win.clear()

    mode = 0 if len(sys.argv) == 1 else sys.argv[1]
    levelidx = 0 if len(sys.argv) == 1 else (randint(0, len(levels)) if sys.argv[2] == 'random' else int(sys.argv[2]))
    print(f"Solving level {levelidx}")
    sokoban = Sokoban(Sokoban.parse(levels[levelidx]))

    if mode == 'solve':
        try:
            root = Node(sokoban)
            win.addstr('Hold on...')
            win.addstr(levels[levelidx])
            node, count = root.astar()
            i = 1

            if node is None:
                win.addstr('Puzzle had no solution.')
            else:
                win.clear()
                win.addstr(f'I just solved level {levelidx}!\n')
                stack = node.from_top()
                moves = len(stack)
                win.addstr(f"\n{str(moves)} moves were required.")
                win.addstr(f"\n{str(count)} nodes were visited.")
                
                while stack:
                    try:
                        key = win.getkey()

                        if key == os.linesep:
                            break

                        win.clear()
                        move = stack.pop()
                        win.addstr(f'Solving level {levelidx}!\n')
                        win.addstr(f'Move {i}:\n')
                        win.addstr(str(move))
                        win.addstr(f"\n{str(moves)} moves were required.")
                        i+=1
                    except Exception as e:
                        pass
        except Exception as e:
            win.addstr(str(e))
            win.addstr(f"Level {levelidx}")

    elif mode == 'play':
        moves = 0
        while 1:          
            try:                 
                key = win.getkey()
                moves += 1
            
                if not sokoban.press(str(key)):
                    break

                win.clear()
                win.addstr(f"LEVEL {levelidx}\n")
                win.addstr(str(sokoban))
                win.addstr('\n')
                win.addstr("boxes: " + str(sokoban.boxes))
                win.addstr('\n')
                win.addstr("goals: " + str(sokoban.goals))
                win.addstr('\n')
                win.addstr(str(sokoban.heu()))
                win.addstr(f"you've moved {moves} times")
                if(sokoban.stuck()):
                    win.addstr("\nYou're stuck!")
            except Exception as e:  
            #    No input   
                pass 

curses.wrapper(main)