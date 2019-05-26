import queue
import heapq

class Node:
    _ID = 0
    def __init__(self, puzzle: 'Puzzle', parent=None):
        self.id = Node._ID
        self.puzzle = puzzle
        self.children = []
        self.parent = parent
        self.depth = parent.depth + 1 if parent else 0
        Node._ID = Node._ID + 1

    def __lt__(self, other):
        return (self.depth + self.puzzle.heu()) < (other.depth + other.puzzle.heu())
    
    def add_child(self, puzzle: 'Puzzle'):
        self.children.append(Node(puzzle, self))
        
    def expand(self):
        expand = self.puzzle.expand()
        for puzzle in expand.values():
            if puzzle is not None:
                self.add_child(puzzle)

    # A* search
    def astar(self, goal=None):
        q, visited = [self], set()
        heapq.heapify(q)
        counter = 0
        minimal = 100000
        
        while q:
            node = heapq.heappop(q)

            if node.puzzle not in visited:
                counter += 1
                if (goal is not None and node.puzzle == goal) or (goal is None and node.puzzle.heu() == 0):
                    return (node, counter)
                if node.puzzle.heu() < minimal:
                    f = open("demofile2.txt", "a")
                    f.write(f"{str([n.puzzle.heu() for n in q[:5]])} {str(node.puzzle.heu())} {str(len(q))}\n")
                    f.close()
                    minimal = node.puzzle.heu()
                
                visited.add(node.puzzle)
                node.expand()
                for child in node.children:
                    if child.puzzle not in visited:
                        heapq.heappush(q, child)
        
        return None
    
    def __str__(self):
        return str(self.puzzle)
    
    def from_top(self):
        node = self
        stack = []
        while node.parent is not None:
            stack.append(node)
            node = node.parent

        return stack