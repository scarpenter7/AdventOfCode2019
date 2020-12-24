# you need to determine what pair of inputs produces the output 19690720.

def run(codes):
    opCodeIndex = 0
    while True:
        opCode = codes[opCodeIndex]
        modes = processOpCode(opCode)
        operation = modes[3:]
        if operation == [9, 9]: # Halt
            return codes
        codeLength = executeOp(codes, modes, operation, opCodeIndex)
        opCodeIndex += codeLength


def processOpCode(opCode):
    modes = [int(num) for num in str(opCode)]
    while len(modes) < 5:
        modes.insert(0, 0)
    return modes

def executeOp(codes, modes, operation, opCodeIndex):
    #Returns how far the instruction ptr needs to travel
    param1 = codes[opCodeIndex + 1]
    param2 = codes[opCodeIndex + 2]
    param3 = codes[opCodeIndex + 3]

    if operation == [0, 1]:  # Add
        add(codes, param1, param2, param3, modes)
        return 4
    elif operation == [0, 2]:  # Multiply
        multiply(codes, param1, param2, param3, modes)
        return 4
    elif operation == [0, 3]:  # Store input at address
        codes[param1] = 1 # input?
        return 2
    elif operation == [0, 4]:  # Output element at address
        print(codes[param1])
        return 2
    else:
        print("ERROR: " + str(codes[opCodeIndex]))
        return

def add(codes, param1, param2, param3, modes):
    mode1 = modes[2]
    mode2 = modes[1]
    num1, num2 = None, None

    if mode1 == 0:
        num1 = codes[param1]
    elif mode1 == 1:
        num1 = param1

    if mode2 == 0:
        num2 = codes[param2]
    elif mode2 == 1:
        num2 = param2

    codes[param3] = num1 + num2

def multiply(codes, param1, param2, param3, modes):
    mode1 = modes[2]
    mode2 = modes[1]
    num1, num2 = None, None

    if mode1 == 0:
        num1 = codes[param1]
    elif mode1 == 1:
        num1 = param1

    if mode2 == 0:
        num2 = codes[param2]
    elif mode2 == 1:
        num2 = param2

    codes[param3] = num1 * num2

if __name__ == "__main__":
    with open("input.txt", 'r') as myfile:
        input = myfile.read()
        originalCodes = [int(num) for num in input.split(',')]
    finalCodes = run(originalCodes)






