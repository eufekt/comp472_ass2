from  algorithms.uniformCost import uniformCost
from  algorithms.gbfs import gbfs

filepath = './input/samplePuzzles.txt'

# open file, for each line remove /n, split into chars and convert to int
# 
with open(filepath) as f:
    inputLines = [list(map(int, line.rstrip().split())) for line in f]
    # print(inputLines)

for i in range(len(inputLines)):
    uniformCost(i,inputLines[i])

# for i in range(len(inputLines)):
#     gbfs(i,inputLines[i])


