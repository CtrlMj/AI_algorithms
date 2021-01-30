# class Node:
#     def __init__(self, index, value):
#         self.index = None
#         self.value = None
#         self.parent = None
#     def addChild(self, node):
#         node.parent = self

# Globals


constraints = [(2, 0), (2, 1), (3, 0), (3, 1)]
incompatibles = {(2, 0): [(2, 1), (2, 0), (0, 2)],
                 (2, 1): [(2, 1), (1, 0), (1, 1)],
                 (3, 0): [(2, 0), (2, 1), (1, 1)],
                 (3, 1): [(0, 1), (0, 0), (2, 0)]}
domain = 4
variables = [0, 1, 2, 3]

# This would be the stack to save all assignments from start till now in pairs of (variable, value)
assignments = []

def isSafe(var, val):
    for assignment in assignments:
        if (var, assignment[0]) in constraints:
           if (val, assignment[1]) in incompatibles[(var, assignment[0])]:
               return False
        if (assignment[0], var) in constraints:
            if (assignment[1], val) in incompatibles[(assignment[0], var)]:
                return False
    return True



def findSolution(index, value):
    if index < 0:
        return False
    elif index >= len(variables):
        return True

    variable = variables[index]
    while value < domain:
        if isSafe(variable, value):
            assignments.append((variable, value))
            return findSolution(index + 1, 0)
        else:
            value += 1

    else:
        try:
            assingment = assignments.pop()
            return findSolution(index - 1, assingment[1] + 1)
        except IndexError:
            return False










if findSolution(0, 0):
    print(assignments)
