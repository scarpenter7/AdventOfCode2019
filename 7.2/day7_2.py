import itertools

class Machine(object):
    def __init__(self, codes, phaseSettings):
        codesCopy = codes.copy()
        self.amps = [Amp(codesCopy, phaseSettings[i], i) for i in range(5)]
        self.currAmpIndex = 0

    def runMachine(self):
        output = 0
        box = OutputBox()

        while not self.amps[-1].halted:
            for amp in self.amps:
                amp.runAmp(output, box)
            output = box.outputs[-1]
        return output

class Amp(object):
    def __init__(self, codes, phaseSetting, ID):
        self.memory = codes
        self.phaseSetting = phaseSetting
        self.opCodeIndex = 0
        self.output = None
        self.ID = ID
        self.paused = True
        self.halted = False

    def runAmp(self, input, box):
        if self.halted:
            raise RuntimeError("This amplifier is halted!")
        self.paused = False
        phaseSettingUsed = False
        while not self.halted and not self.paused:
            opCode = self.memory[self.opCodeIndex]
            modes = self.processOpCode(opCode)
            operation = modes[3:]
            if not phaseSettingUsed:
                useInput = self.phaseSetting
                phaseSettingUsed = True
            else:
                useInput = input
            self.opCodeIndex = self.executeOp(self.memory, useInput, modes, operation, self.opCodeIndex, box)

    def processOpCode(self, opCode):
        modes = [int(num) for num in str(opCode)]
        while len(modes) < 5:
            modes.insert(0, 0)
        return modes

    def executeOp(self, memory, input, modes, operation, opCodeIndex, box):
        # Returns new location of instruction ptr
        param1 = memory[opCodeIndex + 1]
        param2 = memory[opCodeIndex + 2]
        param3 = memory[opCodeIndex + 3]

        if operation == [0, 1]:  # Add
            return self.add(memory, param1, param2, param3, opCodeIndex, modes)
        elif operation == [0, 2]:  # Multiply
            return self.multiply(memory, param1, param2, param3, opCodeIndex, modes)
        elif operation == [0, 3]:  # Store input at address
            memory[param1] = input
            return opCodeIndex + 2
        elif operation == [0, 4]:  # Output element at address and store output in the output box
            return self.storeOutput(memory, param1, box, opCodeIndex)
        elif operation == [0, 5]:  # Jump if true
            return self.jumpIfTrue(memory, param1, param2, opCodeIndex, modes)
        elif operation == [0, 6]:  # Jump if false
            return self.jumpIfFalse(memory, param1, param2, opCodeIndex, modes)
        elif operation == [0, 7]:  # Is less than
            return self.isLessThan(memory, param1, param2, param3, opCodeIndex, modes)
        elif operation == [0, 8]:  # equals
            return self.equals(memory, param1, param2, param3, opCodeIndex, modes)
        elif operation == [0, 9]: # Halt
            self.halt()
            return opCodeIndex
        else:
            raise IndexError("Invalid OpCode: " + str(memory[opCodeIndex] + "\nOpCodeIndex: " + str(opCodeIndex)))

    def getNumsFromModes(self, memory, params, modes):
        modesCopy = modes.copy()
        digitModes = modesCopy[:3]
        digitModes.reverse()
        nums = []

        for i, param in enumerate(params):
            num = None
            if digitModes[i] == 0:
                num = memory[param]
            elif digitModes[i] == 1:
                num = param
            nums.append(num)

        return nums

    def add(self, memory, param1, param2, param3, opCodeIndex, modes):
        nums = self.getNumsFromModes(memory, [param1, param2], modes)
        memory[param3] = nums[0] + nums[1]
        return opCodeIndex + 4

    def multiply(self, memory, param1, param2, param3, opCodeIndex, modes):
        nums = self.getNumsFromModes(memory, [param1, param2], modes)
        memory[param3] = nums[0] * nums[1]
        return opCodeIndex + 4

    def storeOutput(self, memory, param1, box, opCodeIndex):
        output = memory[param1]
        # print(output)
        box.outputs.append(output)
        return opCodeIndex + 2

    def jumpIfTrue(self, codes, param1, param2, opCodeIndex, modes):
        nums = self.getNumsFromModes(codes, [param1, param2], modes)
        if nums[0] != 0:
            return nums[1]
        return opCodeIndex + 3

    def jumpIfFalse(self, codes, param1, param2, opCodeIndex, modes):
        nums = self.getNumsFromModes(codes, [param1, param2], modes)
        if nums[0] == 0:
            return nums[1]
        return opCodeIndex + 3

    def isLessThan(self, codes, param1, param2, param3, opCodeIndex, modes):
        nums = self.getNumsFromModes(codes, [param1, param2], modes)
        if nums[0] < nums[1]:
            codes[param3] = 1
        else:
            codes[param3] = 0
        return opCodeIndex + 4

    def equals(self, codes, param1, param2, param3, opCodeIndex, modes):
        nums = self.getNumsFromModes(codes, [param1, param2], modes)
        if nums[0] == nums[1]:
            codes[param3] = 1
        else:
            codes[param3] = 0
        return opCodeIndex + 4

    def halt(self):
        self.halted = True
        print("Amp " + str(self.ID) + " halted.")

class OutputBox(object):
    def __init__(self):
        self.outputs = []


if __name__ == "__main__":
    with open("input.txt", 'r') as myfile:
        input = myfile.read()
        originalCodes = [int(num) for num in input.split(',')]
    phasePerms = itertools.permutations(range(5, 10))
    maxOutput = 0
    bestPhaseSettings = None
    for phaseSettings in phasePerms:
        machine = Machine(originalCodes, phaseSettings)
        output = machine.runMachine(originalCodes, phaseSettings)
        if output > maxOutput:
            maxOutput = output
            bestPhaseSettings = phaseSettings
    print("Answer:")
    print(maxOutput)
    print(bestPhaseSettings)





