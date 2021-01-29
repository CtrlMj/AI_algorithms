# A* algorithm to solver 8-puzzle

import heapq
class Node:
    def __init__(self, state):
        self.state  = state
        self.left   = None
        self.right  = None
        self.up     = None
        self.down   = None
        self.parent = None

    def addRight(self, node):
        self.right = node
        self.right.parent = self

    def addLeft(self, node):
        self.left = node
        self.left.parent = self

    def addUp(self, node):
        self.up = node
        self.up.parent = self

    def addDown(self, node):
        self.down = node
        self.down.parent = self


def moveLeft(node):
    state = node.state
    i = state.index("0")
    moved = state[:i-1] + "0" + state[i-1] + state[i+1:]
    return Node(moved)


def moveRight(node):
    state = node.state
    i = state.index("0")
    moved = state[:i] + state[i+1] + "0" + state[i+2:]
    return Node(moved)


def moveUp(node):
    state = node.state
    i = state.index
    moved = state[:i-3] + "0" + state[i-2:i] + state[i-3] + state[i+1:]
    return Node(moved)


def moveDown(node):
    state = node.state
    i = state.index
    moved = state[:i] + state[i+3] + state[i+1:i+3] + "0" + state[i+4:]
    return Node(moved)


def generate_path(node):            #this function will generate the path to achieve the goal
    list_of_path = [node]           #while there exists a parent, continue backtracking
    while not node.parent:
        node = node.parent
        list_of_path.append(node)

    return list_of_path

def computecost(node):
    h = 0
    g = 0
    # compute h
    for i, value in enumerate(node.state):
        if value != goal[i]:
            h += 1
    # compute g:
    while node.parent:
        g += 1
        node = node.parent

    return g+h



def Astar(initial, goal):
    heap = heapq.heappush([], (computecost(initial), initial))
    while heap:
        root = heapq.heappop(heap)
        if root.state == goal:
            return generate_path(root)

        elif root.state not in visited:
            visited.append(root.state)
            i = root.state.index("0")
            if i % 3 != 0:      # if empty is not in index 0, 3 or 6, we cant move it to left
                new = moveLeft(root.state)
                root.addLeft(new)
                heapq.heappush(heap, (computecost(root.left), root.left))

            if i % 3 != 2:  # if empty is not in index 2, 5 or 7, we can move it to right
                new = moveRight(root.state)
                root.addRight(new)
                heapq.heappush(heap, (computecost(root.right), root.right))

            if i > 2:  # if empty is below the first row, we can move it up
                new = moveUp(root.state)
                root.addUp(new)
                heapq.heappush(heap, (computecost(root.up), root.up))

            if i < 6:  # if empty is above the last row, we can move it down
                new = moveDown(root.state)
                root.addDown(new)
                heapq.heappush(heap, (computecost(root.down), root.down))

    else:
        return "no path found"


initial = "134802765"
goal = "123804765"
visited = []
Astar(Node(initial))
