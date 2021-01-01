# The image you received is 25 pixels wide and 6 pixels tall.
import numpy as np

def countNums(layer, numCheck):
    return sum([1 for num in layer if num == numCheck])

def findMinZeros(layers):
    minZeros = countNums(layers[0], 0)
    minLayer = layers[0]
    for layer in layers[1:]:
        numZeros = countNums(layer, 0)
        if numZeros < minZeros:
            minZeros = numZeros
            minLayer = layer
    return minLayer

if __name__ == "__main__":
    with open("input.txt", 'r') as myfile:
        input = myfile.read()

    nums = [int(num) for num in input]
    layerSize = 25 * 6
    numLayers = len(nums) // layerSize
    layers = [np.array(nums[(i * layerSize):((i + 1) * layerSize)]) for i in range(numLayers)]
    minZerosLayer = findMinZeros(layers)
    answer = countNums(minZerosLayer, 1) * countNums(minZerosLayer, 2)
    print("Answer: " + str(answer))


