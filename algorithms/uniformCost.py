from timeit import default_timer as timer

class Node:
    def __init__(self, state=None, parent=None, depth=0):
        self.state = state
        self.parent = parent
        self.depth = depth

# return T/F if state is a goal state
def isGoalNode(node):
    return (node.state == goalState1 or node.state == goalState2)

# return array of [index, cost] where I can move
def checkMoves(index):
    moves = []

    if index == 0:
        moves = [[1, 1], [3, 2], [4, 1], [5, 3], [7, 3]]
    elif index == 1:
        moves = [[0, 1], [2, 1], [5, 1]]
    elif index == 2:
        moves = [[1, 1], [3, 1], [6, 1]]
    elif index == 3:
        moves = [[0, 2], [2, 1], [4, 3], [6, 3], [7, 1]]
    elif index == 4:
        moves = [[0, 1], [1, 3], [3, 3], [5, 1], [7, 2]]
    elif index == 5:
        moves = [[1, 1], [4, 1], [6, 1]]
    elif index == 6:
        moves = [[2, 1], [5, 1], [7, 1]]
    elif index == 7:
        moves = [[0, 3], [2, 3], [3, 1], [4, 2], [6, 1]]

    return moves

# returns a list of new nodes
def expandChildNodes(node):
    childNodes = []
    state = node.state
    indexOfBlank = state.index(0)
    possibleMoves = checkMoves(indexOfBlank) # [[0, 1], [2, 1], [5, 1]]

    for move in possibleMoves:
        childState = state.copy()
        childState[indexOfBlank] = state[move[0]]
        childState[move[0]] = 0
        if(node.parent is not None):
            if(childState != node.parent.state):    
                newNode = Node(childState, node, node.depth + move[1])
                childNodes.append(newNode)
        else:
            newNode = Node(childState, node, node.depth + move[1])
            childNodes.append(newNode)
    
    return childNodes

def printSolution(node, start, end, index):
    f = open("output/"+ str(index) + "_" + "ucs_solution.txt", "w")
    print("printing uniformCost Algorithm Solution for puzzle "+ str(index))
    solution = []
    totalCost = 0
    next = node
    
    solution.append({"state":node.state, "depth": node.depth})
    
    while(next.parent is not None):
        solution.append({"state": next.parent.state, "depth":next.parent.depth})
        next = next.parent
    
    solution.reverse()

    f.write("0 0 ")
    print("0", "0", end=" ")
    for i in solution[0]['state']:
        f.write(str(i) + " ")
        print(i, end=" ")
    f.write('\n')
    print("")

    for i in range(len(solution)):
        if (i is not 0):
            
            print(solution[i]['state'].index(0), end=" ")
            f.write(str(solution[i]['state'].index(0)) + " ")
            
            print(solution[i]['depth'] - solution[i-1]['depth'], end=" ")
            f.write(str(solution[i]['depth'] - solution[i-1]['depth']) + " ")

            totalCost = totalCost + (solution[i]['depth'] - solution[i-1]['depth'])
            for i in solution[i]['state']:
                print(i, end=" ")
                f.write(str(i) + " ")
            print("")
            f.write("\n")

    f.write(str(totalCost) + " ")
    print(totalCost, end=" ")
    
    f.write(str(end-start))
    print(end-start)

    f.close()


goalState1 = [1, 2, 3, 4, 5, 6, 7, 0]
goalState2 = [1, 3, 5, 7, 2, 4, 6, 0]

# initialState = [3, 0, 1, 4, 2, 6, 5, 7]
# initialState = [1,2,3,4,0,5,7,6]
initialState = [1,2,3,4,5,0,6,7]

# accepts a puzzle of the form [1,2,3,4,5,0,6,7]
def uniformCost(index, puzzle):
    start = Node(puzzle)
    priorityQueue = []
    priorityQueue.append(start);
    start = timer()
    searching = True 
    while(searching):
        priorityQueue.sort(key= lambda x: x.depth);
        node = priorityQueue[0]
        isGoal = isGoalNode(node)
        
        if(isGoal):
            print('you have found the goal')
            end = timer()
            printSolution(node, start, end, index)
            searching = False
        else:
            listOfChildNodes = expandChildNodes(node)
            priorityQueue = priorityQueue + listOfChildNodes
            priorityQueue.remove(node)

# uniformCost(initialState)