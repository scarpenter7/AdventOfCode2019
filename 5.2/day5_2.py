def run(codes, input):
    opCodeIndex = 0
    while True:
        opCode = codes[opCodeIndex]
        modes = processOpCode(opCode)
        operation = modes[3:]
        if operation == [9, 9]: # Halt
            return codes
        opCodeIndex = executeOp(codes, input, modes, operation, opCodeIndex)
    # for opcode 4, return a list of nums instead of printing them

def processOpCode(opCode):
    modes = [int(num) for num in str(opCode)]
    while len(modes) < 5:
        modes.insert(0, 0)
    return modes

def executeOp(codes, input, modes, operation, opCodeIndex):
    #Returns new location of instruction ptr
    param1 = codes[opCodeIndex + 1]
    param2 = codes[opCodeIndex + 2]
    param3 = codes[opCodeIndex + 3]

    if operation == [0, 1]:  # Add
        return add(codes, param1, param2, param3, opCodeIndex, modes)
    elif operation == [0, 2]:  # Multiply
        return multiply(codes, param1, param2, param3, opCodeIndex, modes)
    elif operation == [0, 3]:  # Store input at address
        codes[param1] = input
        return opCodeIndex + 2
    elif operation == [0, 4]:  # Output element at address
        print(codes[param1]) # for opcode 4, return a list of nums instead of printing them
        return opCodeIndex + 2
    elif operation == [0, 5]:  # Jump if true
        return jumpIfTrue(codes, param1, param2, opCodeIndex, modes)
    elif operation == [0, 6]:  # Jump if false
        return jumpIfFalse(codes, param1, param2, opCodeIndex, modes)
    elif operation == [0, 7]:
        return isLessThan(codes, param1, param2, param3, opCodeIndex, modes)
    elif operation == [0, 8]:
        return equals(codes, param1, param2, param3, opCodeIndex, modes)
    else:
        print("ERROR: " + str(codes[opCodeIndex]))
        return

def getNumsFromModes(codes, params, modes):
    modesCopy = modes.copy()
    digitModes = modesCopy[:3]
    digitModes.reverse()
    nums = []

    for i, param in enumerate(params):
        num = None
        if digitModes[i] == 0:
            num = codes[param]
        elif digitModes[i] == 1:
            num = param
        nums.append(num)

    return nums

def add(codes, param1, param2, param3, opCodeIndex, modes):
    nums = getNumsFromModes(codes, [param1, param2], modes)
    codes[param3] = nums[0] + nums[1]
    return opCodeIndex + 4

def multiply(codes, param1, param2, param3, opCodeIndex, modes):
    nums = getNumsFromModes(codes, [param1, param2], modes)
    codes[param3] = nums[0] * nums[1]
    return opCodeIndex + 4

def jumpIfTrue(codes, param1, param2, opCodeIndex, modes):
    nums = getNumsFromModes(codes, [param1, param2], modes)
    if nums[0] != 0:
        return nums[1]
    return opCodeIndex + 3

def jumpIfFalse(codes, param1, param2, opCodeIndex, modes):
    nums = getNumsFromModes(codes, [param1, param2], modes)
    if nums[0] == 0:
        return nums[1]
    return opCodeIndex + 3

def isLessThan(codes, param1, param2, param3, opCodeIndex, modes):
    nums = getNumsFromModes(codes, [param1, param2], modes)
    if nums[0] < nums[1]:
        codes[param3] = 1
    else:
        codes[param3] = 0
    return opCodeIndex + 4

def equals(codes, param1, param2, param3, opCodeIndex, modes):
    nums = getNumsFromModes(codes, [param1, param2], modes)
    if nums[0] == nums[1]:
        codes[param3] = 1
    else:
        codes[param3] = 0
    return opCodeIndex + 4

if __name__ == "__main__":
    with open("input.txt", 'r') as myfile:
        input = myfile.read()
        originalCodes = [int(num) for num in input.split(',')]
    finalCodes = run(originalCodes, 5)






