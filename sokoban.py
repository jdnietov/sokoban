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
        self.board = Sokoban.parseLevelString(rle)

    def __str__(self):
        s = ''
        for row in self.board:
            for c in row:
                s += c
            s += '\n'
        return s

    def press(self, key):
        if key == 'KEY_RIGHT':
            self.move('right')
    
    def move(self, move):
        self.pos = Sokoban.move_board(self.board, self.pos, move, False)

    @staticmethod
    def parseLevelString(rle):
        i = 0
        x = 0
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
                
            else:
                if c == '|':
                    matrix.append([])
                    x += 1
                else:
                    matrix[x].append(c)

            i += 1
        
        return matrix

levels = [
  '11#|#@-$5-.#|11#',
  '7#|#--.--#|#-$.--#|#--#$-#|#-$#--#|#--.$-#|#@-.--#|7#'
]

def main(win):
    sokoban = Sokoban(levels[0])
    print(sokoban)
    win.nodelay(True)
    key=""
    win.clear()                
    win.addstr("Detected key:")
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