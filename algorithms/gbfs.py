from timeit import default_timer as timer
import numpy as np
from algorithms.moves import Moves
from algorithms.huristics import Heuristics

moves = Moves(2, 4)

class Node:
    def __init__(self, state=None, parent=None, depth=0, g=0, h=0):
        self.state = state
        self.parent = parent
        self.depth = depth
        self.g = g
        self.h = h
        self.f = g+h

goalState1 = [1, 2, 3, 4, 5, 6, 7, 0]
goalState2 = [1, 3, 5, 7, 2, 4, 6, 0]

# return T/F if state is a goal state
def is_goal_node(node):
    return (node.state == goalState1 or node.state == goalState2)

# returns a list of childern nodes
def expand_child_nodes(node, heuris):
    childNodes = []
    state = node.state
    indexOfBlank = state.index(0)
    startTime = timer()
    possibleMoves = moves.check_moves(indexOfBlank) # [[0, 1], [2, 1], [5, 1]]
    for move in possibleMoves:
        childState = state.copy()
        childState[indexOfBlank] = state[move[0]]
        childState[move[0]] = 0
        startTime = timer()
        h = heuris.get_heuristic_weight(childState, goalState1, goalState2 )
        if(node.parent is not None):
            # prevent a move be a move that would 
            # result into being the state of the parent
            if(childState != node.parent.state):    
                newNode = Node(childState, node, node.depth + h, move[1], h)
                childNodes.append(newNode)
        else: #root node does'nt need this check ^
            newNode = Node(childState, node, node.depth + h, 0, h)
            childNodes.append(newNode)
    
    return childNodes



def print_solution(node, startTime, endTime, index, heur_number):
    f = open("output/"+ str(index) + "_" + "gbfs_"+heur_number+"_solution.txt", "w")
    print("printing gbfs Algorithm Solution for puzzle "+ str(index)+ " for heuristic "+heur_number)
    solution = []
    totalCost = 0
    next = node
    
    solution.append({"state":node.state, "depth": node.depth, "g": node.g})
    
    while(next.parent is not None):
        solution.append({"state": next.parent.state, "depth":next.parent.depth, "h": node.h, "g": node.g})
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

            totalCost = totalCost + solution[i]['g']
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

def print_nosolution(index, heur_number):
    f = open("output/"+ str(index) + "_" + "gbfs_"+heur_number+ "_solution.txt", "w")
    f.write("no solution")
    f.close()

def get_heur_numb(heuris):
    if(heuris is "hamming"):
        return "h0"
    
    elif(heuris is "manhattan"):
        return "h1"
    
    elif(heuris is "h0"):
        return "h0"

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
def gbfs(index, heuris, puzzle):
    start = Node(puzzle)
    priorityQueue = [start]
    startTime = timer()
    searching = True 
    endTime = 0
    heur_number = get_heur_numb(heuris.heuristic)
    
    solution = []
    totalCost = []
    search = []
    time = []
    
    f = open("output/"+ str(index) + "_" + "gbfs_"+heur_number+"_search.txt", "w")

    while(searching):
        priorityQueue.sort(key= lambda x: x.depth);
        node = priorityQueue[0]
        search.append(node)

        f.write("0 0 ")
        f.write(str(node.h))
        f.write(" ")
        for i in node.state:
            f.write(str(i) + " ")
        f.write("\n")
        
        isGoal = is_goal_node(node)
        
        if(isGoal):
            endTime = timer()
            output = print_solution(node, startTime, endTime, index, heur_number)
            solution = output["solution"]
            totalCost = output["totalCost"]
            time = endTime - startTime
            searching = False
        else:
            listOfChildNodes = expand_child_nodes(node, heuris)
            priorityQueue.remove(node)
            priorityQueue = merge_and_remove_highest_duplicate(priorityQueue,listOfChildNodes)
        
        # comment below to stop at 60 seconds

        endTime = timer()
        if (endTime-startTime > 60):
            print("uc more than 60 seconds for puzzle"+ str(index))
            print_nosolution(index, heur_number)
            searching = False
            solution = "no solution"
            search = "no solution"
            totalCost = "no solution"
            time = "no solution"

    f.close()
    return {
        "solution": solution,
        "totalCost": totalCost,
        "search": search,
        "time": time,
    }