import curses
import os

# elements = {
#     '#': 'wall',
#     '@': 'player',
#     '+': 'player on goal',
#     '$': 'box',
#     '*': 'box on goal',
#     '.': 'goal',
#     '-': 'floor'
# }

class Sokoban:
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
        if key == 'KEY_RIGHT':
            return True
    
    def move(self, move):
        self.pos = Sokoban.move_board(self.board, self.pos, move, False)

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
  '7#|#--.--#|#-$.--#|#--#$-#|#-$#--#|#--.$-#|#@-.--#|7#'
]

def main(win):
    sokoban = Sokoban(levels[1])
    win.nodelay(True)
    key=""
    win.clear()                
    win.addstr("Detected key:\n")
    win.addstr(str(sokoban))
    while 1:          
        try:                 
            key = win.getkey()
           
            if sokoban.press(str(key)):
                break

            win.clear()                
            win.addstr("Detected key:")
            win.addstr(str(key))

            if key == os.linesep:
                break           
        except Exception as e:  
           # No input   
           pass 

curses.wrapper(main)