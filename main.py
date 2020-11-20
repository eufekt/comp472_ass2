from  algorithms.uniformCost import uniformCost
from  algorithms.gbfs import gbfs
from  algorithms.huristics import Heuristics
from  algorithms.a_alg import a_star
import numpy as np

filepath = './input/samplePuzzles.txt'
random50Filepath = './input/random50.txt'

# open file, for each line remove /n, split into chars and convert to int
# 

heuris0 = Heuristics(2, 4, heuristic='hamming')
heuris1 = Heuristics(2, 4, heuristic='manhattan')



with open(filepath) as f:
    inputLines = [list(map(int, line.rstrip().split())) for line in f]

# with open(random50Filepath) as f:
#     inputLines = [list(map(int, line.rstrip().split())) for line in f]

for i in range(len(inputLines)):
    uniformCost(i,inputLines[i])

for i in range(len(inputLines)):
    gbfs(i, heuris0, inputLines[i])

for i in range(len(inputLines)):
    gbfs(i,heuris1, inputLines[i])

for i in range(len(inputLines)):
    a_star(i, heuris0, inputLines[i])

for i in range(len(inputLines)):
    a_star(i,heuris1, inputLines[i])

# average & total of solution path
# average & total of search path
# average & total of no solution
# average & total cost
# average & total execution time

def analyse(heuris, heurisName, algoName):
    solutions = []
    searches = []
    costs = []
    time = []


    if(algoName is "gbfs"):
        for i in range(len(inputLines)):
            output = gbfs(i, heuris, inputLines[i])
            solutions.append(output["solution"])
            searches.append(output["search"])
            costs.append(output["totalCost"])
            time.append(output["time"])
    
    if(algoName is "uc"):
        for i in range(len(inputLines)):
            output = uniformCost(i, inputLines[i])
            solutions.append(output["solution"])
            searches.append(output["search"])
            costs.append(output["totalCost"])
            time.append(output["time"])
    
    if(algoName is "astar"):
        for i in range(len(inputLines)):
            output = a_star(i, heuris, inputLines[i])
            solutions.append(output["solution"])
            searches.append(output["search"])
            costs.append(output["totalCost"])
            time.append(output["time"])


    totalSolutionLength = 0
    totalSearchLength = 0
    totalNoSolutions = 0
    totalCost = 0
    totalTime = 0

    for solutions in solutions:
        if(solutions != "no solution"):
            totalSolutionLength = totalSolutionLength + len(solutions)
        else:
            totalNoSolutions = totalNoSolutions + 1

    for searches in searches:
        if(searches != "no solution"):
            totalSearchLength = totalSearchLength + len(searches)

    for cost in costs:
        if (cost != "no solution"):
            print(cost)
            totalCost = totalCost + cost

    for time in time:
        if (time != "no solution"):
            totalTime = totalTime + time

    print(" ")
    print(algoName+ "___"+ heurisName)
    print("total length solutions      : " + str(totalSolutionLength))
    print("average length solutions    : " + str(totalSolutionLength/50))
    print("total length searches       : " + str(totalSearchLength))
    print("average length searches     : " + str(totalSearchLength/50))
    print("total no solutions          : " + str(totalNoSolutions))
    print("average no solutions        : " + str(totalNoSolutions/50))
    print("total cost                  : " + str(totalCost))
    print("average cost                : " + str(totalCost/50))
    print("total execution time        : " + str(totalTime))
    print("average execution time      : " + str(totalTime/50))
    

def generate50RandomPuzzle():
    f = open(random50Filepath, "w")
    for puzzle in range(50):
        rand_arr =  np.random.permutation(8)
        for i in rand_arr:
            f.write(str(i)+" ")
        f.write("\n")

# generate50RandomPuzzle()


# analyse(heuris0, "hamming", "gbfs")

# analyse(heuris0, "manhattan", "gbfs")
# analyse(heuris1, "hamming", "gbfs")
# analyse(heuris0, "manhattan", "astar")
# analyse(heuris1, "hamming", "astar")
# analyse(heuris0, "manhattan", "uc")