import numpy as np
from scipy import sparse

def getIntersection(wireSegments1, wireSegments2):
    pts1 = set([(pt[0], pt[1]) for pt in wireSegments1])
    pts2 = set([(pt[0], pt[1]) for pt in wireSegments2])
    intersection = pts1.intersection(pts2)
    return intersection

def getMinLength(wireSegmentsList):
    minLength = -1
    minPt = (0,0)
    for i in range(len(wireSegmentsList[0])):
        for j in range(len(wireSegmentsList[1])):
            seg1 = wireSegmentsList[0][i]
            seg2 = wireSegmentsList[1][j]
            intersection = getIntersection(seg1, seg2)
            if len(intersection) != 0:
                for pt in intersection:
                    fullTuple1 = [tup for tup in seg1 if pt[0] == tup[0] and pt[1] == tup[1]]
                    fullTuple2 = [tup for tup in seg2 if pt[0] == tup[0] and pt[1] == tup[1]]
                    segDist = fullTuple1[0][2] + fullTuple2[0][2]
                    if segDist < minLength or minLength == -1:
                        minLength = segDist
                        minPt = pt
    return minLength, minPt

def contructGrid(wires):
    wireSegments = []
    for wire in wires:
        currWireSegs = computeSegments(wire)
        wireSegments.append(currWireSegs)
    return wireSegments

def computeSegments(wire):
    currPosition = [0, 0]
    wireSegs = []
    wireSegLength = 0
    for instruction in wire:
        direction, dist = parseInstruction(instruction)
        lengthRange = list(range(wireSegLength, wireSegLength + dist + 1))
        if direction == 'R':
            segmentRange = list(range(currPosition[0], currPosition[0] + dist + 1))
            currPosition[0] += dist
            segmentTuples = [(segmentRange[x], currPosition[1], lengthRange[x]) for x in range(len(segmentRange))]
        elif direction == 'L':
            segmentRange = list(range(currPosition[0], currPosition[0] - dist - 1, -1))
            currPosition[0] -= dist
            segmentTuples = [(segmentRange[x], currPosition[1], lengthRange[x]) for x in range(len(segmentRange))]
        elif direction == 'U':
            segmentRange = list(range(currPosition[1], currPosition[1] + dist + 1))
            currPosition[1] += dist
            segmentTuples = [(currPosition[0], segmentRange[y], lengthRange[y]) for y in range(len(segmentRange))]
        elif direction == 'D':
            segmentRange = list(range(currPosition[1], currPosition[1] - dist - 1, -1))
            currPosition[1] -= dist
            segmentTuples = [(currPosition[0], segmentRange[y], lengthRange[y]) for y in range(len(segmentRange))]
        else:
            raise TypeError("Invalid Direction!")
        wireSegLength += dist
        wireSegs.append(segmentTuples)
    wireSegs[0].remove((0, 0, 0))
    return wireSegs


def parseInstruction(instruction):
    if instruction[:-2] == "\n":
        direction = instruction[0]
        dist = int(instruction[1:-2])
        return direction, dist
    direction = instruction[0]
    dist = int(instruction[1:])
    return direction, dist

if __name__ == "__main__":
    with open("input.txt", 'r') as myfile:
        input = myfile.readlines()
        wires = [line.split(',') for line in input]
        wireSegmentsList = contructGrid(wires)
        minLength = getMinLength(wireSegmentsList)
        print("Answer:")
        print(minLength)