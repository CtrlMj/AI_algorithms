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


