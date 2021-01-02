# The image you received is 25 pixels wide and 6 pixels tall.
# 0 is black, 1 is white, and 2 is transparent.
import numpy as np

def decodeLayers(layers):
    pic = np.full((6, 25), 2)

    for layer in layers:
        """for x, y in zip(np.nditer(pic), np.nditer(layer)):
            print(x)
            if x == 2:
                x = y"""
        with np.nditer(layer, op_flags=['readwrite']) as layerIt:
            with np.nditer(pic, op_flags=['readwrite']) as picIt:
                for x, y in zip(picIt, layerIt):
                    if x == 2:
                        x[...] = y
    return pic

if __name__ == "__main__":
    with open("input.txt", 'r') as myfile:
        input = myfile.read()

    nums = [int(num) for num in input]
    layerSize = 25 * 6
    numLayers = len(nums) // layerSize
    layers = [np.array(nums[(i * layerSize):((i + 1) * layerSize)]).reshape((6, 25)) for i in range(numLayers)]
    finalPic = decodeLayers(layers)
    print(finalPic)


