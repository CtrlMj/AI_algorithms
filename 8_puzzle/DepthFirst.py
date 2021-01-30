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


def df(initial):
    stack = []              #We can simply use a list as stack and pop or append at the back of the list
    stack.append(initial)
    while stack:
        root = stack.pop()
        if root.state == goal:
            return generate_path(root)
        # only proceed with this node if it is not already visited
        if root.state not in visited:
            visited.append(root.state)

            i = root.state.index("0")
            if i % 3 != 0:  # if empty is not in index 0, 3 or 6, we can move it to left
                new = moveLeft(root.state)
                root.addLeft(new)
                stack.append(root.left)

            if i % 3 != 2:  # if empty is not in index 2, 5 or 7, we can move it to right
                new = moveRight(root.state)
                root.addRight(new)
                stack.append(root.left)

            if i > 2:       # if empty is below the first row, we can move it up
                new = moveUp(root.state)
                root.addUp(new)
                stack.append(root.up)

            if i < 6:       # if empty is above the last row, we can move it down
                new = moveDown(root.state)
                root.addDown(new)
                stack.append(root.down)

    else:
        print("Sorry, no path available")


stack = []                       #note that a list object can easily be used as stack with it's "append()" and "pop()" methods
goal = "123804765"
initial = "134802765"
visited = []                     #keep track of visited nodes
df(Node(initial))
