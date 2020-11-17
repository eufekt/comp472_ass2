from timeit import default_timer as timer
import numpy as np
from algorithms.moves import Moves
from algorithms.huristics import Heuristics


moves = Moves(2, 4)
heuris = Heuristics(2, 4, heuristic='manhattan')

class Node:
    def __init__(self, state=None, parent=None, depth=0):
        self.state = state
        self.parent = parent
        self.depth = depth

goalState1 = [1, 2, 3, 4, 5, 6, 7, 0]
# goalState2 = [1, 3, 5, 7, 9,  2, 4, 6, 0]

# return T/F if state is a goal state
def is_goal_node(node):
    return (node.state == goalState1)

# return array of [index, cost] where I can move
def check_moves(index):
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

# returns a list of childern nodes
def expand_child_nodes(node):
    childNodes = []
    state = node.state
    indexOfBlank = state.index(0)
    possibleMoves = moves.check_moves(indexOfBlank) # [[0, 1], [2, 1], [5, 1]]

    for move in possibleMoves:
        childState = state.copy()
        childState[indexOfBlank] = state[move[0]]
        childState[move[0]] = 0
        h = heuris.get_heuristic_weight(childState, goalState1)

        
        if(node.parent is not None):
            # prevent a move be a move that would 
            # result into being the state of the parent
            if(childState != node.parent.state):    
                newNode = Node(childState, node, node.depth + h)
                childNodes.append(newNode)
        else: #root node does'nt need this check ^
            newNode = Node(childState, node, node.depth + h)
            childNodes.append(newNode)
    
    return childNodes

def print_solution(node, startTime, endTime, index):
    f = open("output/"+ str(index) + "_" + "gbfs_solution.txt", "w")
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
    
    f.write(str(endTime-startTime))
    print(endTime-startTime)

    f.close()

def print_nosolution(index):
    f = open("output/"+ str(index) + "_" + "ucs_solution.txt", "w")
    f.write("no solution")
    f.close()

# returns merged list
def merge_and_remove_highest_duplicate(priorityQueue, listOfChildNodes):        

    for node in listOfChildNodes:
        index = next((i for i,v in enumerate(priorityQueue) if node.state == v.state), False)

        if(index):
            if(priorityQueue[index].depth > node.depth): #remove from priority queue
                priorityQueue.remove(priorityQueue[index])
            elif(priorityQueue[index].depth < node.depth):
                listOfChildNodes.remove(node)
        
    return listOfChildNodes + priorityQueue

# accepts an index representing position of puzzle in input and a puzzle of the form [1,2,3,4,5,0,6,7]
def gbfs(index, puzzle):
    start = Node(puzzle)
    priorityQueue = [start]
    startTime = timer()
    searching = True 
    endTime = 0
    
    while(searching):

        priorityQueue.sort(key= lambda x: x.depth);

        node = priorityQueue[0]
        isGoal = is_goal_node(node)
        
        if(isGoal):
            endTime = timer()
            print_solution(node, startTime, endTime, index)
            searching = False
        else:
            listOfChildNodes = expand_child_nodes(node)
            # print_solution(node, startTime, endTime, index)
            priorityQueue.remove(node)
            priorityQueue = merge_and_remove_highest_duplicate(priorityQueue,listOfChildNodes)
        
        # comment below to stop at 60 seconds

        # endTime = timer()
        # if (endTime-startTime > 60):
        #     print("uc more than 60 seconds for puzzle"+ str(index))
        #     printNosolution(index)
        #     searching = False
