import pprint
class Node:
    def __init__(self, variable, domain):
        self.neighbors = []
        self.variable = variable
        self.value = 0
        self.domain = list(range(domain))
    def addNeighbor(self, node):
        self.neighbors.append(node)
    def domainRemove(self, value):
        self.domain.remove(value)


constraints = [(2, 0), (2, 1), (3, 0), (3, 1)]
incompatibles = {(2, 0): [(2, 1), (2, 0), (0, 2)],
                 (2, 1): [(2, 1), (1, 0), (1, 1)],
                 (3, 0): [(2, 0), (2, 1), (1, 1)],
                 (3, 1): [(0, 1), (0, 0), (2, 0)]}
d = 3
variables = [0, 1, 2, 3]
nodes = []

def constructNodes():
    for variable in variables:
        nodes.append(Node(variable, d))

def constructGraph():
    graph = dict.fromkeys(nodes, [[] for i in range(len(nodes))])
    for i in nodes:
        for j in nodes[i+1:]:
            if ((nodes[i], nodes[j]) in constraints) or ((nodes[j], nodes[i]) in constraints):
                nodes[i].addNeighbor(nodes[j])
                graph[nodes[i]].append(nodes[j])
                nodes[j].addNeighbor(nodes[i])
                graph[nodes[j]].append(nodes[i])

    return graph

graph = constructGraph()

def variableChoice(nodesset):
    mostConstrained = None
    l = 0
    for variable in nodesset:
        neighborsnum = len(graph[variable])
        if neighborsnum > l:
            l = neighborsnum
            mostConstrained = variable
    return mostConstrained

def valueChoice(var):
    leastConstraining = 0
    for value in var.domain:
        pass
    for adjacent in graph[var]:
        if (var.variable, adjacent.variable) in incompatibles:



def forwardCheck(setofnodes):
    currentNode = variableChoice(setofnodes)
    currentNode.value = valueChoice(currentNode)


print(pprint.pprint(constructGraph()))
