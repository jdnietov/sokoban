import queue
import heapq

class Node:
    _ID = 0
    def __init__(self, puzzle: 'Puzzle', parent=None):
        self.id = Node._ID
        self.puzzle = puzzle
        self.children = []
        self.parent = parent
        Node._ID = Node._ID + 1
    
    def __lt__(self, other):
        return self.puzzle.heu() < other.puzzle.heu()
    
    def add_child(self, puzzle: 'Puzzle'):
        self.children.append(Node(puzzle, self))
        
    def expand(self):
        expand = self.puzzle.expand()
        for puzzle in expand.values():
            if puzzle is not None:
                self.add_child(puzzle)
    
    # Breadth-first search
    def bfs(self, goal: 'Puzzle'):
        q = queue.Queue()
        visited = set() # set of Puzzles
        
        q.put(self)
        
        while not q.empty():
            node = q.get()
            print(node.puzzle)
            if node.puzzle in visited:
                continue
                        
            visited.add(node.puzzle)
            
            if node.puzzle == goal:
                return node
            
            node.expand()
            for p in node.children:
                if p.puzzle not in visited:
                    q.put(p)
        
        return None # what??
    
    # Depth-first search
    def dfs(self, goal: 'Puzzle'):
        stack = [self]
        visited = set()
        
        while stack:
            node = stack.pop()
            if node.puzzle in visited:
                continue
                
            if node.puzzle == goal:
                return node
            
            visited.add(node.puzzle)
            node.expand()
            for child in node.children:
                if child.puzzle not in visited:
                    stack.append(child)
        
        return None
        
    # A* search
    def astar(self, goal=None):            
        q = [self]
        visited = set()
        counter = 0
        
        while q:
            node = heapq.heappop(q)
            # print("node:",node)
            
            if node in visited:
                continue

            if goal:
                if node.puzzle == goal:
                    return node
            else:
                if node.puzzle.heu() == 0:
                    return node
            
            visited.add(node.puzzle)
            node.expand()
            for child in node.children:
                if child.puzzle not in visited:
                    heapq.heappush(q, child)
                
            counter += 1
        
        return None
    
    def __str__(self):
        return str(self.puzzle)
    
    def branch(self):
        node = self
        stack = []
        while node.parent is not None:
            stack.append(node)
            node = node.parent

        return stack
        # print(len(stack), 'moves were required.')
        # while len(stack) > 0:
        #     print(stack.pop())