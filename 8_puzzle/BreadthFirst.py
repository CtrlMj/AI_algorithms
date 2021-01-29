import time
import heapq
from queue import Queue


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

    def __lt__(self, other):
        return False
    def __gt__(self, other):
        return False
    def __eq__(self, other):
        return True


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
    i = state.index("0")
    moved = state[:i-3] + "0" + state[i-2:i] + state[i-3] + state[i+1:]
    return Node(moved)


def moveDown(node):
    state = node.state
    i = state.index("0")
    moved = state[:i] + state[i+3] + state[i+1:i+3] + "0" + state[i+4:]
    return Node(moved)


def generate_path(node):            #this function will generate the path to achieve the goal
    list_of_path = [node.state]     #while there exists a parent, continue backtracking
    while node.parent:
        node = node.parent
        list_of_path.append(node.state)

    return list_of_path



def bf(initialstate):
    q = Queue()
    q.put(initialstate)
    while q.not_empty:
        root = q.get()
        if root.state == goal:
            return generate_path(root)
        #only proceed with this node if it is not already visited
        elif root.state not in visited:
            visited.append(root.state)

            i = root.state.index("0")
            if i % 3 != 0:           #if empty is not in index 0, 3 or 6, we cant move it to left
                new = moveLeft(root)
                root.addLeft(new)
                q.put(root.left)

            if i % 3 != 2:           #if empty is not in index 2, 5 or 7, we can move it to right
                new = moveRight(root)
                root.addRight(new)
                q.put(root.right)

            if i > 2:                #if empty is below the first row, we can move it up
                new = moveUp(root)
                root.addUp(new)
                q.put(root.up)

            if i < 6:                #if empty is above the last row, we can move it down
                new = moveDown(root)
                root.addDown(new)
                q.put(root.down)

    else:
        raise ProcessLookupError("Sorry, no path available")


def df(root, depthbound):
    if root.state == goal:
        return generate_path(root)
    if depthbound <= 0:
        return None

    if root.state not in visited:  # only proceed with this node if it is not already visited
        visited.append(root.state)

        i = root.state.index("0")
        if i % 3 != 0:  # if empty is not in index 0, 3 or 6, we can move it to left
            new = moveLeft(root)
            root.addLeft(new)
            result = df(root.left, depthbound - 1)
            if result:
                return result
        if i % 3 != 2:  # if empty is not in index 2, 5 or 7, we can move it to right
            new = moveRight(root)
            root.addRight(new)
            result = df(root.right, depthbound - 1)
            if result:
                return result
        if i > 2:       # if empty is below the first row, we can move it up
            new = moveUp(root)
            root.addUp(new)
            result = df(root.up, depthbound - 1)
            if result:
                return result
        if i < 6:       # if empty is above the last row, we can move it down
            new = moveDown(root)
            root.addDown(new)
            result = df(root.down, depthbound - 1)
            if result:
                return result


def iddf(initialstate):
    success = None
    depthcounter = 1
    while not success:
        global visited
        visited = []
        success = df(initialstate, depthcounter)
        depthcounter += 1
    return success

def checkPossible(start, end):
    # if the number of inversions in goal state is even
    # and that of initial state is odd, the goal is not reachable
    # the same is true for the converse case
    start = list(start)
    startcounter = 0            #counts the number of inversions in the starting state
    end = list[end]
    endcounter = 0              #counts the number of inversions in the ending state
    for i in range(9):
        for j in range(i+1, 9):
            if start[j] < start[i]: startcounter += 1
            if   end[j] <   end[i]: endcounter   += 1

    if (startcounter % 2) != (endcounter % 2):
        return False
    else:
        return True

def computetiles(node):
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
def computeChebyshev(node, goal):
    h = 0
    g = 0
    # compute h
    # manhattan distance in for x which is located in ith position
    # would be difference of rows + difference of columns = abs(i%3-x%3) + abs(i/3-x/3)
    for i, value in enumerate(node.state):
        j = goal.index(value)
        h += max(abs(i % 3 - j % 3), abs(i / 3 - j / 3))

    # compute g:
    while node.parent:
        g += 1
        node = node.parent

    return 2*h + g                     # 2*h is computed because the question asks for double of the chebyshev distance
def computeManhattan(node, goal):
    h = 0
    g = 0
    # compute h
    # manhattan distance in for x which is located in ith position
    # would be difference of rows + difference of columns = abs(i%3-x%3) + abs(i/3-x/3)
    for i, value in enumerate(node.state):
        j = goal.index(value)
        h += abs(i % 3 - j % 3) + abs(i / 3 - j / 3)

    # compute g:
    while node.parent:
        g += 1
        node = node.parent

    return h + g
def computeCombo(node, goal):
    pass
def Astar(initial, costfunc):
    heap = []
    heapq.heappush(heap, (costfunc(initial), initial))
    while heap:
        tuple = heapq.heappop(heap)
        root = tuple[1]
        if root.state == goal:
            return generate_path(root)

        elif root.state not in visited:
            visited.append(root.state)

            i = root.state.index("0")
            if i % 3 != 0:      # if empty is not in index 0, 3 or 6, we cant move it to left
                new = moveLeft(root)
                root.addLeft(new)
                heapq.heappush(heap, (costfunc(root.left), root.left))

            if i % 3 != 2:  # if empty is not in index 2, 5 or 7, we can move it to right
                new = moveRight(root)
                root.addRight(new)
                heapq.heappush(heap, (costfunc(root.right), root.right))

            if i > 2:  # if empty is below the first row, we can move it up
                new = moveUp(root)
                root.addUp(new)
                heapq.heappush(heap, (costfunc(root.up), root.up))

            if i < 6:  # if empty is above the last row, we can move it down
                new = moveDown(root)
                root.addDown(new)
                heapq.heappush(heap, (costfunc(root.down), root.down))

    else:
        return "no path found"



# Global variables are as follows:
initial  = "134802765"               # Initial state
goal     = "123804765"               # The goal state
# initial  = input("please input your initial state: ")
# goal     = input("please input your goal state: ")
method   = "Astar"#input("please enter the method you wish to use\n1-Bread First = BF\n2-Depth First = DF"
                 #"\n3-Iterative Depth First = IDDF\n4-Best First = Astar\n")
visited  = []                        # The list that saves visited nodes in the tree
start    = 0                         # Records the starting time of the algorithm
end      = 0                         # Records the ending time of the algorithm
nodesNum = 0                         # Records the total number of nodes generated in the tree
path     = []                        # The list which will save the path from initial state to the goal state
# End of global variables





# if the Breadth first search is sought
if method == "BF":
    start = time.time()
    path = bf(Node(initial))
    end = time.time()
    print(path)

elif method == "DF":
    dbound  = input("Please enter your desired bound: ")
    start   = time.time()
    path    = df(Node(initial), dbound)
    end     = time.time()
    if not path:
        raise ProcessLookupError("Could not find the goal state within given depth")
    else:
        print(path)

elif method == "IDDF":
    start   = time.time()
    path    = iddf(Node(initial))
    end     = time.time()
    print(path)

elif method == "Astar":
    costfuncDictionary = {'1' : computetiles, "2" : computeManhattan, "3" : computeCombo, "4": computeChebyshev}
    hfunc   = '1'#input("Please enter the # for your desired cost function from the options below:\n1  2  3  4")
    start   = time.time()
    path    = Astar(Node(initial), costfuncDictionary[hfunc])
    end     = time.time()
    print(path)
else:
    raise ValueError("You did not specify a valid search function")


# print("Path:", printPath(path))
# print("The total number of generated nodes =", nodesNum)
print("The total running time = %.70f" % (end - start))
