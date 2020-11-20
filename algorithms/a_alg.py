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


goal_state_1 = [1, 2, 3, 4, 5, 6, 7, 0]
goal_state_2 = [1, 3, 5, 7, 2, 4, 6, 0]

# returns a list of childern nodes
def expand_child_nodes(node, heuris):
    child_nodes = []
    state = node.state
    index_of_blank = state.index(0)
    possible_moves = moves.check_moves(index_of_blank)  # [[0, 1], [2, 1], [5, 1]]

    for move in possible_moves:
        child_state = state.copy()
        child_state[index_of_blank] = state[move[0]]
        child_state[move[0]] = 0
        h = heuris.get_heuristic_weight(child_state, goal_state_1, goal_state_2)

        if node.parent is not None:
            # prevent a move be a move that would result into being the state of the parent
            if child_state != node.parent.state:
                child_nodes.append(Node(child_state, node, node.depth + h + move[1], move[1], h))
        else:  # root node does'nt need this check ^
            child_nodes.append( Node(child_state, node, node.depth + h + move[1], move[1], h))

    return child_nodes


def print_closed_list(closed_list):
    total_cost = 0
    closed_list.reverse()
    
    the_list = [closed_list[0]]

    for node in closed_list:
        # print(node.state, " | f=", node.f)
        if the_list[len(the_list) - 1].parent is node:
            the_list.append(node)

    for node in the_list:
        total_cost += node.g
        # print(node.state, " | g=", node.g)

    return total_cost
    


def print_solution(node, startTime, endTime, index, heur_number):
    f = open("output/" + str(index) + "_" + "astar_"+heur_number+"_solution.txt", "w")
    print("printing astar Algorithm Solution for puzzle " + str(index)+" for heuristic "+ heur_number)
    # print("gbfs "+ str(index), end=" ")
    solution = []
    totalCost = 0
    next = node

    solution.append({"state": node.state, "depth": node.depth, "g": node.g})

    while (next.parent is not None):
        solution.append({"state": next.parent.state, "depth": next.parent.depth, "g": node.g})
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

            print(solution[i]['depth'] - solution[i - 1]['depth'], end=" ")
            f.write(str(solution[i]['depth'] - solution[i - 1]['depth']) + " ")
            
            totalCost = totalCost + solution[i]['g']
            for i in solution[i]['state']:
                print(i, end=" ")
                f.write(str(i) + " ")
            print("")
            f.write("\n")

    f.write(str(totalCost) + " ")
    print(totalCost, end=" ")

    f.write(str(endTime - startTime))
    print(endTime - startTime)

    f.close()
    return {"solution": solution, "totalCost": totalCost}


def print_nosolution(index, heur_number):
    f = open("output/" + str(index) + "_" + "astar_"+heur_number+"_solution.txt", "w")
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
def merge_and_remove_highest_duplicate(priority_queue, list_of_child_nodes):
    for node in list_of_child_nodes:
        index = next((i for i, v in enumerate(priority_queue) if node.state == v.state), False)

        if index:
            if (priority_queue[index].depth > node.depth):  # remove from priority queue
                priority_queue.remove(priority_queue[index])
            elif (priority_queue[index].depth <= node.depth):
                list_of_child_nodes.remove(node)

    return list_of_child_nodes + priority_queue


# accepts an index representing position of puzzle in input and a puzzle of the form [1,2,3,4,5,0,6,7]
def a_star(index, heuris, puzzle):
    start = Node(puzzle)
    priority_queue = [start]
    start_time = timer()
    searching = True
    end_time = 0
    heur_number = get_heur_numb(heuris.heuristic)

    solution = []
    totalCost = []
    search = []
    time = []

    f = open("output/"+ str(index) + "_" + "astar_"+heur_number+"_search.txt", "w")

    closed_list = []

    while searching:

        priority_queue.sort(key=lambda x: x.depth);

        node = priority_queue[0]
        search.append(node)
        
        f.write(str(node.f)+ " ")
        f.write(str(node.g)+ " ")
        f.write(str(node.h)+ " ")
        for i in node.state:
            f.write(str(i) + " ")
        f.write("\n")

        closed_list.append(node)

        if node.state == goal_state_1 or node.state == goal_state_2 or timer() - start_time > 60:
            end_time = timer()
            if end_time - start_time > 60:
                print_nosolution(index, heur_number)
                print("timed out")
                solution = "no solution"
                search = "no solution"
                totalCost = "no solution"
                time = "no solution"
            else:
                output = print_solution(node, start_time, end_time, index, heur_number)
                solution = output["solution"]
                totalCost = output["totalCost"]
                time = end_time - start_time
                # totalCost = print_closed_list(closed_list)
            searching = False
        else:
            listOfChildNodes = expand_child_nodes(node, heuris)
            # print_solution(node, startTime, endTime, index)
            priority_queue.remove(node)
            priority_queue = merge_and_remove_highest_duplicate(priority_queue, listOfChildNodes)

    # f.close()
    return {
        "solution": solution,
        "totalCost": totalCost,
        "search": search,
        "time": time,
    }


def a_star_scale(index, heuris, puzzle, goal):
    start = Node(puzzle)
    priority_queue = [start]
    start_time = timer()
    searching = True
    end_time = 0
    heur_number = get_heur_numb(heuris.heuristic)

    solution = []
    totalCost = []
    search = []
    time = []

    f = open("output/"+ str(index) + "_" + "astar_"+heur_number+"_search.txt", "w")

    closed_list = []

    while searching:

        priority_queue.sort(key=lambda x: x.depth);

        node = priority_queue[0]
        search.append(node)
        
        f.write(str(node.f)+ " ")
        f.write(str(node.g)+ " ")
        f.write(str(node.h)+ " ")
        for i in node.state:
            f.write(str(i) + " ")
        f.write("\n")

        closed_list.append(node)

        if node.state == goal:
            end_time = timer()
            if end_time - start_time > 60:
                print("timed out")
                solution = "no solution"
                search = "no solution"
                totalCost = "no solution"
                time = "no solution"
            else:
                output = print_solution(node, start_time, end_time, index, heur_number)
                solution = output["solution"]
                totalCost = output["totalCost"]
                time = end_time - start_time
                # totalCost = print_closed_list(closed_list)
            searching = False
        else:
            listOfChildNodes = []
            state = node.state
            index_of_blank = state.index(0)
            possible_moves = moves.check_moves(index_of_blank)  # [[0, 1], [2, 1], [5, 1]]

            for move in possible_moves:
                child_state = state.copy()
                child_state[index_of_blank] = state[move[0]]
                child_state[move[0]] = 0
                h = heuris.get_heuristic_weight(child_state, goal, goal)

                if node.parent is not None:
                    # prevent a move be a move that would result into being the state of the parent
                    if child_state != node.parent.state:
                        listOfChildNodes.append(Node(child_state, node, node.depth + h + move[1], move[1], h))
                else:  # root node does'nt need this check ^
                    listOfChildNodes.append( Node(child_state, node, node.depth + h + move[1], move[1], h))
            # print_solution(node, startTime, endTime, index)
            priority_queue.remove(node)
            priority_queue = merge_and_remove_highest_duplicate(priority_queue, listOfChildNodes)

    # f.close()
    return {
        "solution": solution,
        "totalCost": totalCost,
        "search": search,
        "time": time,
    }