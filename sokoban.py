# elements = {
#     '#': 'wall',
#     '@': 'player',
#     '+': 'player on goal',
#     '$': 'box',
#     '*': 'box on goal',
#     '.': 'goal',
#     '-': 'floor'
# }

levels = [
  '11#|#@-$5-.#|11#',
]

def parseLevelString(rle):
    i = 0
    board = ''

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
                board += t + ' '
            
        else:
            if c == '|':
                board += '\n'
            else:
                board += c + ' '

        i += 1
    
    return board
        
print(parseLevelString(levels[0]))