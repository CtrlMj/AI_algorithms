# Prolog Unification Algorithm
#in this code:
#1- function maketree() builds up the whole tree, each node contains two expressions in the form: (ex1,ex2)
#2- dicntionary treeDic records the equality
#3- separete() separates each argument of each node into exp1 and exp2
#4- separatefunc() extracts the arguments of a function
#5- printDic is a helper which prints the recorded equalities such that duplicates dont happen (things like X=Y,Y=X)

#how to compile: simply write the following in a command window at the program's directory:
#python Unification_Algorithm YourInput
import sys

#the pillar of code. each node in the tree will consist 2 expressions in the form of (exp1,exp2) which will be examined
#whether they can be unified or not
class Node():
    def __init__(self, value):
        self.value = value
        self.leftChild = None
        self.nextSibling = None
        self.parent = None
        self.leftsibling = None

    def addLeft(self, left):
        if self.leftChild == None:
            self.leftChild = Node(left)
            self.leftChild.parent = self
        else:
            print("Cant have two left children!")

    def addNextSibling(self, next):
        if self.nextSibling == None:
            self.nextSibling = Node(next)
            self.nextSibling.parent = self.parent
            self.nextSibling.leftsibling = self
        else:
            print("Cant have more than one next children")



#this function extracts arguments of an arbitrary function to a list of arguments
def separatefunc(func):
    inner = func[func.find('(') + 1: func.rfind(')')]       #get rid of the starting and ending parentheses of a function
    #if what remains has length less than 1, something is wrong
    if len(inner) < 1:
        raise ValueError("not enough arguments in function " + func)
    args = []
    i = 0
    #start to traverse the function
    while i < len(inner):
        #if next argument is a variable:
        if inner[i].isupper():
            if i < len(inner) - 1 and inner[i+1] != ',':
                raise ValueError("Missing comma after argument " + inner[i] + " in function " + func)
            elif i == len(inner) - 1:
                args.append(inner[i])
                return args
            elif inner[i+1] == ',' and i+1 < len(inner) - 1:
                args.append(inner[i])
                i = i + 2
                continue
            else:
                raise Exception("invalid ending for the function " + inner)

        #if next argument is a function or constant
        if inner[i].islower():
            if i < len(inner) - 2 and inner[i+1] == '(':                                                                #if the argument is a function (parenthesis indicates function)
                parencounter = 1
                for j in range(i+2, len(func) - 2):                                                                     #traverse the function untill you reach the ending parenthesis(add +1 for oppening
                    if inner[j] == ')':                                                                                 #parenthesis, reduce 1 for a closing parenthesis.(works like a stack))
                        parencounter -= 1
                    elif inner[j] == '(':
                        parencounter += 1
                    if parencounter == 0:                                                                               #soon as ending parenthesis reached do the following
                        if j < len(inner) - 1 and inner[j+1] != ',':                                                    #if next character is not comma and we havnt reached end of expression
                            raise ValueError("Missing comma after parenthesis in function " + inner[i:j+1])             #there is an error in the input since it would be like this: f(X,z)a
                        elif j == len(inner) - 1:                                                                       #if we reached end of expression
                            args.append(inner[i:j+1])
                            return args
                        elif inner[j+1] == ',' and j+1 < len(inner) - 1:                                                #if the end of the argument has reached
                            args.append(inner[i:j + 1])                                                                 #add the argument to the list and break to do the same for next arugment
                            i = j+2                                                                                     #Set i to the start of the next argument
                            break
                        else:                                                                                           #if none of the above happened, inout is flawed
                            raise Exception("invalid arguments in " + inner)
                    if j == len(inner) - 1:                                                                             #after each iteration in for loop, check if we ve reached end of expression
                        raise Exception("Unbalanced parentheses in " + inner)
                continue
            elif i < len(inner) - 2 and inner[i+1] != ',' and inner[i+1] != '(':                                        #if exp1 is neither a constant nor a variable
                raise ValueError("invalind arguments in " + inner)
            elif i < len(inner) - 2 and inner[i+1] == ',':                                                              #if a exp1 is a constant(if nothing but comma apears after lowercase, the lowercase is cnst
                args.append(inner[i])
                i = i + 2
                continue
            elif i == len(inner) - 1:                                                                                   #if we reached end of expression
                args.append(inner[i])
                return args
            else:                                                                                                       #if none of the above happened, input is flawed
                raise Exception("invalid argument in " + func)

        else:                                                                                                           #if argument is neither variable, nor constant or function then input is flawed
            raise Exception("Invalid argument in " + func + "at position " + str(i+2) + ':' + inner[i])

    return args



def separate(expression):
    expression = expression[expression.find('(') + 1: expression.rfind(')')]                                            #get rid of initial and final parentheses: (exp1,exp2)-->exp1,exp2
    if len(expression) < 3:                                                                                             #if the length of the interior expression is less than 3, not enough arguments
        raise ValueError("Not enough arguments to compare in comparison " + expression)
    args = []
    startofsecond = 2
    if expression[0].islower():                                                                                         #the first argument starts with lower case it could be function or constant
        if expression[1] == '(':                                                                                        #if it is a function:
            countpar = 1
            for i in range(2, len(expression)):
                if expression[i] == '(':
                    countpar += 1
                elif expression[i] == ')':
                    countpar -= 1

                if countpar == 0:  # it means we ve reached balanced parantheses:
                    if i - 0 < 3:
                        raise ValueError("not enough arguments in function " + expression[0])
                    if expression[i + 1] != ',':
                        raise ValueError(
                            "you forgot to separate your two input arguments in " + expression + "with comma")
                    else:
                        args.append(expression[0:i + 1])
                        startofsecond = i + 2
                    break

        elif expression[1] == ',':  # if it is a constant
            args.append(expression[0])
        else:
            raise Exception("Invalid first argument in the comparison: " + expression)

    elif expression[0].isupper():  # if the first argument starts with upper case it should be variable
        if expression[1] != ',':
            raise ValueError("you forgot to separate your Variable " + expression[1] + "with comma in:" + expression)
        else:
            args.append(expression[0])

    else:
        raise ValueError("invalid arguments " + expression[0] + " in the comparison " + expression)                     #from last comment till here, the same thing for each argument is input of separatefunc
                                                                                                                        #is happening. Nothing new
    # if no error has occurred so far, it starts for the second argument
    if expression[startofsecond].islower():                                                                             #from this point onwards, the same thing happens for second argument in the tree node
        if startofsecond == len(expression) - 1:
            args.append(expression[startofsecond])
        elif expression[startofsecond + 1] == '(':
            countpar = 1
            for i in range(startofsecond + 2, len(expression)):
                if expression[i] == '(':
                    countpar += 1
                elif expression[i] == ')':
                    countpar -= 1

                if countpar == 0:
                    if i - startofsecond < 3:
                        raise ValueError("not enough arguments in the function " + expression[startofsecond:])
                    if i != len(expression) - 1:
                        raise ValueError(
                            "Unbalanced paranthesis or redundant stuff after parenthesis in " + expression[
                                                                                                startofsecond:i + 1])
                    else:
                        args.append(expression[startofsecond:])
                        if i != len(expression) - 1:
                            raise Exception(
                                "Unbalanced paranthesis or redundant stuff after parenthesis in " + expression[
                                                                                                    startofsecond:i + 1])
                        break

                if i == len(expression) - 1:
                    raise Exception("Unbalanced paranthesis in " + expression[startofsecond:])


        else:
            raise ValueError("Second argument in the comparison " + expression + " is not valid")

    elif expression[startofsecond].isupper():
        if startofsecond != len(expression) - 1:
            raise ValueError("Second argument in the comparison " + expression + " is not valid")
        else:
            args.append(expression[startofsecond])



    else:
        raise ValueError("invalid arguments " + expression[0] + " in the comparison: " + expression)

    return args

                                                                                                                        #this function saves the equivalent stuff in a dictionary called treeDic sets the left
def updateTree(l, r):                                                                                                   #argument l equal to right arguemnt r.
    if l != r:                                                                                                          #check whether the two are already equal
        curval = treeDic.get(l, None)
        if r[0].islower():
            if l in r[1:]:
                raise Exception("Cannot make a function " + r + " equal to variable " + l)

        if curval == None:
            treeDic[l] = r
            return 0
        elif curval != r:
            if curval[0].islower() and r[0].islower():
                raise Exception("Cannot make " + l + " equal to both " + curval + " and " + r)
            elif curval[0].islower() and r.isupper():
                updateTree(r, curval)                                                                                   #if r is a variable, set its value equal to value of l as well
            elif curval.isupper():                                                                                      #if the value of l its self is a variable, set its value equal to r too
                treeDic[l] = r
                updateTree(curval, r)
        else:
            return 0
    else:
        return 0

def printDic(key):                                                                                                      #this function prints the tree, in way that no duplicates occur
    values = []                                                                                                         #this list will contain what should be printed for the desired key
    if treeDic[key][0].islower():                                                                                       #if the key you wanna print is equal to a constant or function simply add it to values
        values.append(treeDic[key])
        return values
    else:                                                                                                               #if the value of key is set equal to a variable, using a while loop, add whatever that
        value = treeDic[key]                                                                                            #value is equal to to the print list "values" in a chain
        while (value.isupper()) and (key != treeDic.get(value, None)):
            values.append(value)
            if treeDic.get(value, None) is None:
                break
            else:
                oldval = value
                value = treeDic[value]
                treeDic[oldval] = '!'
        if len(values) == 0:
            values.append(value)
            return values
        if value != values[-1]:
            values.append(value)
        if value.isupper() and (value in treeDic.keys()):
            treeDic[value] = '!'
        return values


def makeTree(node):
    expr = node.value
    left, right = separate(expr)


    if len(left) == 1 and left.isupper():                                                                               #if left is variable:
        updateTree(left, right)
        return

    if len(right) == 1 and right.isupper():                                                                             #if the right one is a variable:
        updateTree(right, left)
        return

    elif left[0].islower() and right[0].islower() and left[0] != right[0]:                                              #two unvariables with different names cannot be equal
        raise AttributeError("Can't make " + left + " equal to " + right)


    elif (len(left) > 1 and left[0].islower()) and (len(right) > 1 and right[0].islower()) and (right[0] == left[0]):   #the case when we have two functions with the same name
        lfuncargs = separatefunc(left)                                                                                  #returns the left function arguments in a list
        rfuncargs = separatefunc(right)                                                                                 #returns the right function arguments in a list
        if len(lfuncargs) != len(rfuncargs):                                                                            #two function with different number of arguments cannot be equal
            raise Exception("functions " + left + " and " + right + " does not have the same number of arguments")
        elif len(lfuncargs) == len(rfuncargs) == 1:                                                                     #if there is only one argument per function, you only need one left child
            node.addLeft('(' + lfuncargs[0] + ',' + rfuncargs[0] + ')')
            makeTree(node.leftchild)
        elif len(lfuncargs) == len(rfuncargs):                                                                          #else if there are more than one argument, add some next childs as many number as necassary
            node.addLeft('(' + lfuncargs[0] + ',' + rfuncargs[0] + ')')
            makeTree(node.leftChild)
            x = node.leftChild
            for i in range(1, len(lfuncargs)):                                                                          #this for loop adds the next right children after the leftmost child being built before
                x.addNextSibling('(' + lfuncargs[i] + ',' + rfuncargs[i] + ')')
                makeTree(x.nextSibling)
                x = x.nextSibling
        else:
            raise Exception("Something strange went wrong")
    else:
        raise Exception("Something strange went wrong, cant make them equal")






inpt = sys.argv[2]

treeDic = {}                                                                                                            #dictionary to record the equalities
if inpt[0] != '(' or inpt[-1] != ')':
    raise SyntaxError("Missing parantheses in the start and/or end of the expression")

inside = inpt[inpt.find('(') + 1: inpt.rfind(')')]
if len(inside) < 3:
    raise ValueError("Not enough arguments in the " + inpt)
else:
    makeTree(Node(inpt))
    print("yes\n")
    for key in treeDic.keys():                                                                                          #basically this whole for loop does not take much time since the length of sequences
        if treeDic[key] != '!':                                                                                         #are short. it only tries to finlalize output for variables that are equal but only
            print(key, "=", end=' ')                                                                                    #through some intermediary variables
            for equivalent in printDic(key):
                if equivalent[0].islower() and len(equivalent) > 1:
                    for char in equivalent:
                        if char.isupper() and (char in treeDic.keys()):
                            equivalent = equivalent.replace(char, printDic(char)[-1])
                print(equivalent, "=", end=' ')
        print('\b\b\b\n')
