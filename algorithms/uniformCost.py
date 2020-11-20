from timeit import default_timer as timer
import numpy as np
from algorithms.moves import Moves

moves = Moves(2, 4)

class Node:
    def __init__(self, state=None, parent=None, depth=0):
        self.state = state
        self.parent = parent
        self.depth = depth

# return T/F if state is a goal state
def is_goal_node(node):
    goal_state1 = [1, 2, 3, 4, 5, 6, 7, 0]
    goal_state_2 = [1, 3, 5, 7, 2, 4, 6, 0]
    return (node.state == goal_state1 or node.state == goal_state_2)

# return array of [index, cost] where I can move


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
        if(node.parent is not None):
            if(childState != node.parent.state):    
                newNode = Node(childState, node, node.depth + move[1])
                childNodes.append(newNode)
        else:
            newNode = Node(childState, node, node.depth + move[1])
            childNodes.append(newNode)
    
    return childNodes

def print_solution(node, startTime, endTime, index):
    f = open("output/"+ str(index) + "_" + "ucs_solution.txt", "w")
    print("printing uniformCost Algorithm Solution for puzzle "+ str(index))
    # print("uc "+ str(index), end=" ")
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
    return {"solution": solution, "totalCost": totalCost}

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
def uniformCost(index, puzzle):
    start = Node(puzzle)
    priorityQueue = [start]
    startTime = timer()
    searching = True 
    endTime = 0

    solution = []
    totalCost = []
    search = []
    time = []

    f = open("output/"+ str(index) + "_" + "uc_search.txt", "w")
    
    while(searching):

        priorityQueue.sort(key= lambda x: x.depth);

        node = priorityQueue[0]
        search.append(node)

        f.write("0 0 0 ")
        for i in node.state:
            f.write(str(i) + " ")
        f.write("\n")

        isGoal = is_goal_node(node)

        
        if(isGoal):
            endTime = timer()
            # print_solution(node, startTime, endTime, index)
            output = print_solution(node, startTime, endTime, index)
            solution = output["solution"]
            totalCost = output["totalCost"]
            time = endTime - startTime
            searching = False
        else:
            listOfChildNodes = expand_child_nodes(node)
            priorityQueue.remove(node)
            priorityQueue = merge_and_remove_highest_duplicate(priorityQueue,listOfChildNodes)
        
        # comment below to stop at 60 seconds

        endTime = timer() 
        if (endTime-startTime > 60):
            print("uc more than 60 seconds for puzzle"+ str(index))
            print_nosolution(index)
            searching = False
            solution = "no solution"
            search = "no solution"
            totalCost = "no solution"
            time = "no solution"

    # f.close()
    return {
        "solution": solution,
        "totalCost": totalCost,
        "search": search,
        "time": time,
    }