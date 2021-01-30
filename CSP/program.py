import time, math, random, copy


###################################################################################################################
########################Arc Consistency############################################################################
###################################################################################################################
# if an arc is not consistent revise the domains
def revise(i, j):
    revis = False
    # loop over the values of i
    for value in domains[i]:
        # if the value in question is incompatible with everything in j's domain, remove it
        if all([(value, _) in incompatibles[(i, j)] for _ in domains[j]]):
            domains[i].remove(value)
            revis = True

    return revis

def arcConsistency():
    global domains
    # line below keeps a copy of domains, in case we need to restore the changes that will be made
    dom = copy.deepcopy(domains)
    queue = []
    # Initialize the queue which holds the inconsistent arc's that need to be checked
    for constraint in constraints:
        if not any([constraint[0] in assignment for assignment in assignments]) and \
        not any([constraint[1] in assignment for assignment in assignments]):
            queue.append(constraint)
    # End of queue initialization

    # Loop over all inconsistent arcs and revise domains if necessary
    while queue:
        i, j = queue.pop(0)
        if revise(i, j):
            for (a, b) in constraints:
                if (a, b) not in queue and i == a and b != j and\
                not any([b in assignment for assignment in assignments]):
                    queue.append((b, a))
                elif (a, b) not in queue and i == b and a != j and \
                not any([a in assignment for assignment in assignments]):
                    queue.append((a, b))

        if not domains[i]:
            # if the status is not arc consistent, restore the changes made to domains
            domains = dom
            return False

    return True

####################################################################################################################
#####################Back Track#####################################################################################
####################################################################################################################

# Check whether setting the var(variable) equal to val(value) does not violate anything with previous assignments
def isSafe(var, val):
    # loop over all previous assignments
    for assignment in assignments:
        if (var, assignment[0]) in constraints:
           if (val, assignment[1]) in incompatibles[(var, assignment[0])]:
               return False
        if (assignment[0], var) in constraints:
            if (assignment[1], val) in incompatibles[(assignment[0], var)]:
                return False
    return True


# recursive algorithm for backtrack
# it will try to assign the variable with indice "index" and in doing so checks all values in
# domain starting from parameter value
def backTrack(index, value):
    if index < 0:
        return False
    elif index >= len(variables):
        return True

    # fetch the variable you are trying to assign
    variable = variables[index]
    # loop over the variables in domain
    while value < domain:
        # if the current value is safe
        if isSafe(variable, value):
            # store this couple as assignment in the assignments list
            assignments.append((variable, value))
            # move to the next variable
            return backTrack(index + 1, 0)
        else:
            # if the current value is not safe, check the next value in domain
            value += 1
    # if could not find a value for current variable, replace the previous assignment (backtrack)
    else:
        try:
            # remove the previous assignment and try to find a new value for the variable
            assignment = assignments.pop()
            return backTrack(index - 1, assignment[1] + 1)
        except IndexError:
            # if there is no previous assignment, it is not solvable so return false
            return False

####################################################################################################################
###########################Forward Check############################################################################
####################################################################################################################

# remove inconsistent neighbors after assigning val to var (i.e. look forward)
def modify_neighbors_domain(var, val):
    # loop over all variables
    for variable in variables:
        # if the variable is not already assigned
        if not(any([variable in assignment for assignment in assignments])):
            # this block removes the incompatible values from the domain of the variable
            if ((var, variable) in incompatibles):
                tuples = incompatibles[(var, variable)]
                for t in tuples:
                    if val == t[0] and (t[1] in domains[variable]):
                        domains[variable].remove(t[1])
            # does the same thing as previous if block only it's possible that the pair (variable, var) occurs
            # in inconsistents rather than (var, variable)
            elif (variable, var) in incompatibles:
                tuples = incompatibles[(variable, var)]
                for t in tuples:
                    if val == t[1] and (t[0] in domains[variable]):
                        domains[variable].remove(t[0])

# this function restores the changes in the domain after removing the pair (var, val) from the assignments
def restorDomains(var, val):
    # loop over all variables
    for variable in variables:
        # if the variables is not assigned a value yet
        if not (any([variable in assignment for assignment in assignments])):
            # and if the variable has a conflict with var
            if (var, variable) in incompatibles:
                tuples = incompatibles[(var, variable)]
                # reinsert all the values that were removed from domain of variable due to assignment (var, val)
                for t in tuples:
                    if val == t[0] and (t[1] not in domains[variable]) and (isSafe(variable, t[1])):
                        cnter = 0
                        while t[1] > domains[variable][cnter]:
                            cnter += 1
                        domains[variable].insert(cnter, t[1])

            # does the same thing as previous if block only it's possible that the pair (variable, var) occurs
            # in inconsistents rather than (var, variable)
            elif (variable, var) in incompatibles:
                tuples = incompatibles[(variable, var)]
                for t in tuples:
                    if val == t[1] and (t[0] not in domains[variable]) and (isSafe(variable, t[0])):
                        cnter = 0
                        while t[0] > domains[variable][cnter]:
                            cnter += 1
                        domains[variable].insert(cnter, t[0])

# keep doing forward check recursively starting from the variable with indice "index" and a possible value for that
# variable with indice "valueindex"
def forwarCheck(index, valueindex=0):
    if index < 0:
        return False
    elif index >= len(variables):
        return True

    variable = variables[index]
    if domains[variable] and valueindex < len(domains[variable]):
        value = domains[variable][valueindex]
        assignments.append((variable, value))
        modify_neighbors_domain(variable, value)
        return forwarCheck(index+1)
    else:
        try:
            variable, value = assignments.pop()
            restorDomains(variable, value)
            return forwarCheck(index-1, domains[variable].index(value) + 1)
        except IndexError:
            return False

#####################################################################################################################
###########################Full Look Ahead(FLA)######################################################################
######################################################################################################################

# full look ahead algorithm; input arguments are similiar as forward check
def fla(index, valueindex=0):
    if index < 0:
        return False
    elif index >= len(variables):
        return True

    variable = variables[index]
    # this if statement is the only difference with forward check,i.e. it checks the arcConsistency too
    if domains[variable] and valueindex < len(domains[variable]) and arcConsistency():
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
##################################################################################
##################################################################################
##################################################################################

n, p, alpha, r = input("Please input the parameters (n, p, alpha, r) in order, separated with space: ").split()
n, p, alpha, r = int(n), float(p), float(alpha), float(r)
starttime, endtime = 0.0, 0.0

#############Random Generator###############
def randomGenerator():
    counter = 0
    while counter < numConstraints:
        constraint = tuple(random.sample(variables, 2))
        if not(constraint in constraints) and not(constraint[::-1] in constraints):
            constraints.append(constraint)
            counter += 1

    for constraint in constraints:
        incompatibles[constraint] = []
        i = 0
        while i < numPairs:
            pair = (random.randint(0, domain-1), random.randint(0, domain-1))
            if pair not in incompatibles[constraint]:
                incompatibles[constraint].append(pair)
                i += 1

#########End of Random Generator############

#########Function to print the CSP###########
def printCSP():
    for item in incompatibles:
        print(f"(X{item[0]}, X{item[1]}):", incompatibles[item])

########End of Function to print CSP#########

########Function to print the solutions######
def printSolution():
    for item in assignments:
        print(f"X{item[0]}={item[1]}")

########End of function to print solutions###

domain = int(n**alpha)
constraints, incompatibles = [], {}
numConstraints = round(r*n*math.log(n))
variables = list(range(0, n))
numPairs = round(p*math.pow(domain, 2))

# The following list be the stack to save all assignments from start till now in pairs of (variable, value)
# So note that assignment[i][0] = variable and assignment[i][1] = value
assignments = []
# The following dictionary is for keeping track of the domains of the variables
domains = {variable: list(range(domain)) for variable in variables}

pt = 1 - math.exp(-alpha/r)
if p >= pt:
    print("Sorry, you have crossed the threshold")
else:
    randomGenerator()
    printCSP()

    alg = input("Please choose the algorithm: 1-Backtrack 2-ForwardCheck 3-FLA\n")
    if alg == "1":
        shouldArc = input("Do you wanna run arc consistency before anything now?(y/n): ")
        if shouldArc == 'y':
            starttime = time.process_time()
            if not arcConsistency():
                raise Exception("So apparently things aren't arc consistent")

        if backTrack(0, 0):
            endtime = time.process_time()
            print(f"runtime(*10^-12s): {(endtime - starttime)*1000000000}")
            printSolution()
        else:
            print("No solution found for this setting")

    elif alg == "2":
        starttime = time.process_time()
        if forwarCheck(0, 0):
            endtime = time.process_time()
            print(f"runtime(*10^-12s): {(endtime - starttime)*1000000000}")
            printSolution()
        else:
            print("No solution found for this setting")

    elif alg == "3":
        starttime = time.process_time()
        if fla(0, 0):
            endtime = time.process_time()
            print(f"runtime(*10^-12s): {(endtime - starttime)*1000000000}")
            printSolution()
        else:
            print("No solution found for this setting")
    else:
        print("You did not choose a legitimate option")
