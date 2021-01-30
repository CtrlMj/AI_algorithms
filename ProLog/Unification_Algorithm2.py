import sys


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


# root = Node(12)
# root.addLeft(11)
# root.addRight(10)
# root.leftChild.addLeft(9)
# root.leftChild.addRight(8)
# root.rightChild.addLeft(7)
# root.rightChild.addRight(6)
#
# root.printTree()

def separatefunc(func):
    inner = func[func.lfind('(') + 1: func.rfind(')')]
    if len(inner) < 1:
        raise ValueError("not enough arguments in function " + func)
    args = []
    i = 0
    while i < len(inner):
        if inner[i].isupper():
            if i < len(inner) - 1 and inner[i+1] != ',':
                raise ValueError("Missing comma after argument " + inner[i] + " in function " + func)
            elif i == len(inner) - 1:
                args.append(inner[i])
                return args
            elif inner[i+1] == ',' and i+1 < len(inner) - 1:
                args.append(inner[i])
                i = 2
            else:
                raise Exception("invalid ending for the function " + inner)

        if inner[i].islower():
            if i < len(inner) - 2 and inner[i+1] == '(':
                parencounter = 1
                for j in range(i+2, len(func) - 2):
                    if inner[j] == ')':
                        parencounter -= 1
                    elif inner[j] == '(':
                        parencounter += 1
                    if parencounter == 0:
                        if j != len(inner) - 1 and inner[j+1] != ',':
                            raise ValueError("Missing comma after parenthesis in function " + inner[i:j+1])
                        elif j == len(inner) - 1:
                            args.append(inner[i:j+1])
                            break
                        elif inner[j+1] == ',' and j+1 < len(inner) - 1:
                            args.append(inner[i:j + 1])
                            i = j+2
                            break
                        else:
                            raise Exception("Arguments dont end with parenthesis in " + inner[i:j+1])
            elif i < len(inner) - 2 and inner[i+1] == ',':
                args.append(inner[i])
                i = i + 2
            elif i == len(inner) - 1:
                args.append(inner[i])
                return args
            else:
                raise Exception("invalid argument in " + func)
        else:
            raise Exception("Invalid argument in " + func)

    return args


def separate(expression):
    expression = expression[expression.lfind('(') + 1: expression.rfind(')')]
    if len(expression) < 3:
        raise ValueError("Not enough arguments to compare in comparison " + expression)
    args = []
    startofsecond = 2
    if expression[0].islower():  # the first argument starts with lower case it could be function or constant
        if expression[1] == '(':  # if it is a function:
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
    elif expression[0].isupper():  # if the first argument starts with upper case it should be variable
        if expression[1] != ',':
            raise ValueError("you forgot to separate your Variable " + expression[1] + "with comma")
        else:
            args.append(expression[0])

    elif not (expression[0].isalpha):
        raise ValueError("invalid arguments " + expression[0] + " in the comparison " + expression)

    # if no error has occurred so far, it starts for the second argument
    if expression[startofsecond].islower():
        if expression[startofsecond + 1] == '(':
            countpar = 1
            for i in range(startofsecond, len(expression)):
                if expression[i] == '(':
                    countpar += 1
                elif expression[i] == ')':
                    countpar -= 1

                if countpar == 0:
                    if i - startofsecond < 3:
                        raise ValueError("not enough arguments in the function " + expression[startofsecond])
                    if i != len(expression) - 1:
                        raise ValueError(
                            "there is redundant stuff after the closing parenthesis in second arg of comparison + " + expression)
                    else:
                        args.append(expression[startofsecond:])

        elif startofsecond == len(expression) - 1:
            args.append(expression[startofsecond])
        else:
            raise ValueError("Second argument in the comparison " + expression + " is not valid")

    elif expression[startofsecond].isupper():
        if startofsecond != len(expression) - 1:
            raise ValueError("Second argument in the comparison " + expression + " is not valid")
        else:
            args.append(expression[startofsecond])



    elif not (expression[startofsecond].isalpha):
        raise ValueError("invalid arguments " + expression[0] + " in the comparison " + expression)

    return args



def updateTree(l, r):
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
            updateTree(r, curval)
        elif curval.isupper():
            treeDic[l] = r
            treeDic[curval] = r
    else:
        return 0



def makeTree(node):
    expression = node.value
    left, right = separate(expression)

    #if left is variable:
    if len(left) == 1 and left.isupper():
        updateTree(left, right)
        return
    #if the right one is a variable:
    if len(right) == 1 and right.isupper():
        updateTree(right, left)
        return
    #two unvariables with different names cannot be equal
    elif left[0].islower() and right[0].islower() and left != right:
        raise AttributeError("Can't make " + left + " equal to " + right)

    #the case when we have two functions with the same name
    elif (len(left) > 1 and left[0].islower()) and (len(right) > 1 and right[0].islower()) and (right[0] == left[0]):
        lfuncargs = separatefunc(left)      #returns the left function arguments in a list
        rfuncargs = separatefunc(right)     #returns the right function arguments in a list
        if len(lfuncargs) != len(rfuncargs):
            raise Exception("functions " + left + " and " + right + " does not have the same number of arguments")
        elif len(lfuncargs) == len(rfuncargs) == 1:
            node.addLeft('(' + lfuncargs[0] + ',' + rfuncargs[0] + ')')
            makeTree(node.leftchild)
        elif len(lfuncargs) == len(rfuncargs):
            node.addLeft('(' + lfuncargs[0] + ',' + rfuncargs[0] + ')')
            makeTree(node.leftChild)
            x = node.leftChild
            for i in range(1, len(lfuncargs)):
                x.addNextSibling('(' + lfuncargs[i] + ',' + rfuncargs[i] + ')')
                makeTree(x.nextSibling)
                x = x.nextSibling
        else:
            raise Exception("Something strange went wrong")






inpt = sys.argv[2]

treeDic = {}
if inpt[0] != '(' or inpt[-1] != ')':
    raise SyntaxError("Missing parantheses in the start and/or end of the expression")

inside = inpt[inpt.find('(') + 1: inpt.rfind(')')]
if inside is None:
    raise ValueError("Not enough arguments in the " + inpt)
else:
    makeTree(inpt)
