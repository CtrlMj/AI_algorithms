import pprint
import math
import random
n = int(input())
p = 0.33
a = 0.8
r = 0.7
d = int(n**a)
constraints = []
numConstraints = round(r*n*math.log(n))
n = list(range(0, n))
numPairs = round(p*math.pow(d, 2))
counter = 0
while counter < numConstraints:
    constraint = tuple(random.sample(n, 2))
    if not(constraint in constraints) and not(constraint[::-1] in constraints):
        constraints.append(constraint)
        counter += 1

incompatibles = {}
for constraint in constraints:
    incompatibles[constraint] = []
    i = 0
    while i < numPairs:
        pair = (random.randint(0, d-1), random.randint(0, d-1))
        if pair not in incompatibles[constraint]:
            incompatibles[constraint].append(pair)
            i += 1


pprint.pprint(incompatibles)


