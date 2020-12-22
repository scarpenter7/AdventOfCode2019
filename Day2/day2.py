# you need to determine what pair of inputs produces the output 19690720.

def run(codes):

    for num in range(0, len(codes), 4):
        if codes[num] == 99:
            return codes
        index1 = codes[num + 1]
        index2 = codes[num + 2]
        storeIndex = codes[num + 3]
        if codes[num] == 1:
            codes[storeIndex] = codes[index1] + codes[index2]
        elif codes[num] == 2:
            codes[storeIndex] = codes[index1] * codes[index2]
        else:
            print("ERROR: " + str(codes[num]))
            return

if __name__ == "__main__":
    codesOriginal = []
    with open("code.txt", 'r') as myfile:
        input = myfile.read()
        codesOriginal = [int(num) for num in input.split(',')]
    ansFound = False
    for i in range(100):
        if ansFound:
            break
        for j in range(100):
            codes = codesOriginal.copy()
            codes[1] = i
            codes[2] = j
            finalCodes = run(codes)
            if finalCodes is not None and finalCodes[0] == 19690720:
                print("Answer:")
                print(finalCodes[1] * 100 + finalCodes[2])
                break





