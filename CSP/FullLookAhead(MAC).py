from queue import Queue

constraints = [(2, 0), (2, 1), (3, 0), (3, 1)]
incompatibles = {(2, 0): [(2, 1), (2, 0), (0, 2)],
                 (2, 1): [(2, 1), (1, 0), (1, 1)],
                 (3, 0): [(2, 0), (2, 1), (1, 1)],
                 (3, 1): [(0, 1), (0, 0), (2, 0)]}
domain = 4
variables = [0, 1, 2, 3]
domains = {variable: list(range(domain)) for variable in variables}

assignments = []

def modify_neighbors_domain(var, val):
    for variable in variables:
        if (var, variable) in incompatibles:
            tuples = incompatibles[(var, variable)]
            for t in tuples:
                if val == t[0] and (t[1] in domains[variable]):
                    domains[variable].remove(t[1])

        elif (variable, var) in incompatibles:
            tuples = incompatibles[(variable, var)]
            for t in tuples:
                if val == t[1] and (t[0] in domains[variable]):
                    domains[variable].remove(t[0])

def restorDomains(var, val):
    for variable in variables:
        if (var, variable) in incompatibles:
            tuples = incompatibles[(var, variable)]
            for t in tuples:
                if val == t[0] and (t[1] not in domains[variable]):
                    domains[variable].insert(t[1], t[1])

        elif (variable, var) in incompatibles:
            tuples = incompatibles[(variable, var)]
            for t in tuples:
                if val == t[1] and (t[0] not in domains[variable]):
                    domains[variable].insert(t[0], t[0])


def fla(index, valueindex=0):
    if index < 0:
        return False
    elif index >= len(variables):
        return True

    variable = variables[index]
    if domains[variable] and valueindex < len(domains[variable]) and arc_consistent():
        value = domains[variable][valueindex]
        assignments.append((variable, value))
        modify_neighbors_domain(variable, value)
        return fla(index+1)
    else:
        try:
            variable, value = assignments.pop()
            restorDomains(variable, value)
            return fla(index-1, domains[variable].index(value) + 1)
        except IndexError:
            return False


