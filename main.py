from  algorithms.uniformCost import uniformCost

filepath = './input/samplePuzzles.txt'

# open file, for each line remove /n, split into chars and convert to int
with open(filepath) as f:
    inputLines = [list(map(int, line.rstrip().split())) for line in f]
    # print(inputLines)

for i in range(len(inputLines)):
    uniformCost(i,inputLines[i])


