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

######################################################
# Functions to make moves from a given node
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
# End of Functions to make moves from a given node
#######################################################

#######################################################
# Breadth first search
def bf(initialstate):
    global nodesNum
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
                nodesNum += 1

            if i % 3 != 2:           #if empty is not in index 2, 5 or 7, we can move it to right
                new = moveRight(root)
                root.addRight(new)
                q.put(root.right)
                nodesNum += 1

            if i > 2:                #if empty is below the first row, we can move it up
                new = moveUp(root)
                root.addUp(new)
                q.put(root.up)
                nodesNum += 1

            if i < 6:                #if empty is above the last row, we can move it down
                new = moveDown(root)
                root.addDown(new)
                q.put(root.down)
                nodesNum += 1

    else:
        raise ProcessLookupError("Sorry, no path available")


# Depth first search
def df(root, depthbound):
    global nodesNum
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
            nodesNum += 1
            result = df(root.left, depthbound - 1)
            if result:
                return result
        if i % 3 != 2:  # if empty is not in index 2, 5 or 7, we can move it to right
            new = moveRight(root)
            root.addRight(new)
            nodesNum += 1
            result = df(root.right, depthbound - 1)
            if result:
                return result
        if i > 2:       # if empty is below the first row, we can move it up
            new = moveUp(root)
            root.addUp(new)
            nodesNum += 1
            result = df(root.up, depthbound - 1)
            if result:
                return result
        if i < 6:       # if empty is above the last row, we can move it down
            new = moveDown(root)
            root.addDown(new)
            nodesNum += 1
            result = df(root.down, depthbound - 1)
            if result:
                return result


# Iterative deepening depth first search
def iddf(initialstate):
    global visited
    success = None
    depthcounter = 1
    while not success:
        visited = []
        success = df(initialstate, depthcounter)
        depthcounter += 1
    return success


# The A* algorithm
def Astar(initial, costfunc):
    global nodesNum
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
                nodesNum += 1
            if i % 3 != 2:  # if empty is not in index 2, 5 or 7, we can move it to right
                new = moveRight(root)
                root.addRight(new)
                heapq.heappush(heap, (costfunc(root.right), root.right))
                nodesNum += 1

            if i > 2:  # if empty is below the first row, we can move it up
                new = moveUp(root)
                root.addUp(new)
                heapq.heappush(heap, (costfunc(root.up), root.up))
                nodesNum += 1

            if i < 6:  # if empty is above the last row, we can move it down
                new = moveDown(root)
                root.addDown(new)
                heapq.heappush(heap, (costfunc(root.down), root.down))
                nodesNum += 1

    else:
        return "no path found"
#######################################################

#######################################################
# Start of the heuristics computation block
# 1st heuristic, Computing the tiles
def computetiles(node):
    h = 0
    g = 0
    # compute h
    for i, value in enumerate(node.state):
        if value == 0:
            continue
        if value != goal[i]:
            h += 1
    # compute g:
    while node.parent:
        g += 1
        node = node.parent

    return g+h
# 2nd heuristic, Manhattan distance
def computeManhattan(node):
    h = 0
    g = 0
    # compute h
    # manhattan distance in for x which is located in ith position
    # would be difference of rows + difference of columns = abs(i%3-x%3) + abs(i/3-x/3)
    for i, value in enumerate(node.state):
        if value == 0:
            continue
        j = goal.index(value)
        h += abs(i % 3 - j % 3) + abs(i / 3 - j / 3)

    # compute g:
    while node.parent:
        g += 1
        node = node.parent

    return h + g
# 3rd heurisitic, Chebysheve distance
def computeChebyshev(node):
    h = 0
    g = 0
    # compute h
    # would be max of difference in rows & difference of columns = max(abs(i%3-x%3),abs(i/3-x/3))
    for i, value in enumerate(node.state):
        if value == 0:
            continue
        j = goal.index(value)
        h += max(abs(i % 3 - j % 3), abs(i / 3 - j / 3))

    # compute g:
    while node.parent:
        g += 1
        node = node.parent

    return 2*h + g                     # 2*h is computed because the question asks for double of the chebyshev distance
# 4th heuristic, combination of tot and seq
def computeCombo(node):
    h = 0
    g = 0
    seq = 0
    manhattan = 0
    state = node.state
    #make a clockwise copy of both the node and the goal state
    clockwiseNode = state[0]+state[1]+state[2]+state[5]+state[8]+state[7]+state[6]+state[3]
    clockwiseGoal = goal[0]+goal[1]+goal[2]+goal[5]+goal[8]+goal[7]+goal[6]+goal[3]
    #traverse clockwise and add scores for seq,
    for i, element in enumerate(clockwiseNode):
        #cost of a tile in the centre will be counted for separately
        if element == goal[4]:
            continue
        j = clockwiseGoal.index(element)
        #the %8 part is for the last clockwise element to go round and be compared with the first one
        if clockwiseNode[(i+1)%8] != clockwiseGoal[(j+1)%8]:
            seq += 2

    if state[4] != goal[4]:
        seq += 1
    #end of computing seq

    #start of Manhattan=tottdist
    for i, value in enumerate(state):
        if value == 0:
            continue
        j = goal.index(value)
        manhattan += abs(i % 3 - j % 3) + abs(i / 3 - j / 3)
    #end of computing manhattan
    h = manhattan + 3*seq

    #start of computing g
    while node.parent:
        g += 1
        node = node.parent
    #end of g
    return h+g
# End of the heuristics computation block
#######################################################

#######################################################
# Check whether we can reach the goal state from the initial state or not
def checkPossible(start, end):
    # if the number of inversions in goal state is even
    # and that of initial state is odd, the goal is not reachable
    # the same is true for the converse case
    start = list(start)
    startcounter = 0            #counts the number of inversions in the starting state
    end = list(end)
    endcounter = 0              #counts the number of inversions in the ending state
    for i in range(9):
        for j in range(i+1, 9):
            if start[j] < start[i]: startcounter += 1
            if   end[j] <   end[i]: endcounter   += 1

    return (startcounter % 2) == (endcounter % 2)


# This function will trace back the path required to reach a found goal state from the initial state
# if we consider root of the tree as the initial state, we only need to trace back a node that is found
# to be the goal state, back to the its first parent, namely the root
def generate_path(node):            #this function will generate the path to achieve the goal
    list_of_path = [node.state]     #while there exists a parent, continue backtracking
    while node.parent:
        node = node.parent
        list_of_path.append(node.state)

    return list_of_path


# This function will print stages in throughout the required path in nice 3by3 8puzzle format
def printPath(path):
    # traverse the tree from initial state to goal state and print in rows and columns
    for stage in path[::-1]:
        print("**************")
        print(' '.join(stage[0:3]))
        print(' '.join(stage[3:6]))
        print(' '.join(stage[6:]))
########################################################

#####################################################################################################################
#####################################End of Classes and Functions####################################################
#####################################################################################################################
# Global variables are as follows:
initial  = input("please input your initial state: ")
goal     = input("please input your goal state: ")
method   = input("please enter the method you wish to use\nBread First: BF\nDepth First: DF"
                 "\nIterative Depth First: IDDF\nBest First: Astar\n")
visited  = []                        # The list that saves visited nodes in the tree
start    = 0                         # Records the starting time of the algorithm
end      = 0                         # Records the ending time of the algorithm
nodesNum = 1                         # Records the total number of nodes generated in the tree
path     = []                        # The list which will save the path from initial state to the goal state
# End of global variables


# if not checkPossible(initial, goal):
#     raise LookupError("Goal state is not reachable from the start state")


# Check which of the algorithms is sought, ask for the respective inputs and do the job
if method == "BF":
    start = time.time()
    path = bf(Node(initial))
    end = time.time()

elif method == "DF":
    dbound  = int(input("Please enter your desired bound: "))
    start   = time.time()
    path    = df(Node(initial), dbound)
    end     = time.time()
    if not path:
        raise ProcessLookupError("Could not find the goal state within given depth")

elif method == "IDDF":
    start   = time.time()
    path    = iddf(Node(initial))
    end     = time.time()

elif method == "Astar":
    costfuncDictionary = {'1': computetiles, "2": computeManhattan, "3": computeCombo, "4": computeChebyshev}
    hfunc   = input("Please enter the # for your desired cost function from the options below:\n1-tiles out of place  2-manhattan  3-tott+seq  4-Chebyshev:\n")
    start   = time.time()
    path    = Astar(Node(initial), costfuncDictionary[hfunc])
    end     = time.time()

else:
    raise ValueError("You did not specify a valid search function")
# End of Check which of the algorithms is sought, ask for the respective inputs and do the job

# Output what you should
print("1-The total number of generated nodes =", nodesNum)
print("2-The total running time up to 70 decimal point precision = %.70f" % (end - start))
print("3-Path:")
printPath(path)
# End of output what you should
