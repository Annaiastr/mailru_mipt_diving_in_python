import sys

steps = int(sys.argv[1])

for stair in range(1, (steps+1)):
    print(' ' * (steps-stair) + '#'*stair)