import numpy as np
from scipy import sparse

def getIntersections(wireSegmentsList):
    intersectionPts = set()
    for i in range(len(wireSegmentsList[0])):
        for j in range(i, len(wireSegmentsList[1])):
            seg1 = wireSegmentsList[0][i]
            seg2 = wireSegmentsList[1][j]
            intersection = seg1.intersection(seg2)
            if len(intersection) != 0:
                for pt in intersection:
                    intersectionPts.add(pt)
    return intersectionPts

def contructGrid(wires):
    wireSegments = [] * len(wires)
    for wire in wires:
        currWireSegs = computeSegments(wire)
        wireSegments.append(currWireSegs)
    return wireSegments

def computeSegments(wire):
    currPosition = [0, 0]
    wireSegs = []
    for instruction in wire:
        direction, dist = parseInstruction(instruction)
        if direction == 'R':
            segmentRange = list(range(currPosition[0], currPosition[0] + dist + 1))
            currPosition[0] += dist
            segmentTuples = set([(x, currPosition[1]) for x in segmentRange])
        elif direction == 'L':
            segmentRange = list(range(currPosition[0], currPosition[0] - dist - 1, -1))
            currPosition[0] -= dist
            segmentTuples = set([(x, currPosition[1]) for x in segmentRange])
        elif direction == 'U':
            segmentRange = list(range(currPosition[1], currPosition[1] + dist + 1))
            currPosition[1] += dist
            segmentTuples = set([(currPosition[0], y) for y in segmentRange])
        elif direction == 'D':
            segmentRange = list(range(currPosition[1], currPosition[1] - dist - 1, -1))
            currPosition[1] -= dist
            segmentTuples = set([(currPosition[0], y) for y in segmentRange])
        else:
            raise TypeError("Invalid Direction!")
        wireSegs.append(segmentTuples)
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
        intersectionPts = getIntersections(wireSegmentsList)
        intersectionPts.remove((0,0))
        print("Answer:")
        print(min([abs(pt[0]) + abs(pt[1]) for pt in intersectionPts]))
