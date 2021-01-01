import itertools

#INFINITE LOOP BUG???

class Machine(object):
    def __init__(self, codes, phaseSettings):
        codesCopy = codes.copy()
        self.amps = [Amp(codesCopy, phaseSettings[i], i) for i in range(5)]
        self.amps[0].input = 0

    def runMachine(self):
        while not self.amps[-1].halted:
            for i, amp in enumerate(self.amps):
                amp.runAmp()
                if amp.output is not None:
                    nextAmpIndex = (i + 1) % 5
                    self.amps[nextAmpIndex].input = amp.output
        return self.amps[-1].output

class Amp(object):
    def __init__(self, codes, phaseSetting, ID):
        self.memory = codes
        self.phaseSetting = phaseSetting
        self.phaseSettingUsed = False
        self.opCodeIndex = 0
        self.input = None
        self.output = None
        self.ID = ID
        self.paused = True
        self.halted = False

    def runAmp(self):
        if self.halted:
            raise RuntimeError("This amplifier is halted!")
        self.paused = False
        while not self.halted and not self.paused:
            opCode = self.memory[self.opCodeIndex]
            modes = self.processOpCode(opCode)
            operation = modes[3:]
            self.executeOp(operation, modes)

    def processOpCode(self, opCode):
        modes = [int(num) for num in str(opCode)]
        while len(modes) < 5: # Put 0's in front of the list until the list has size 5
            modes.insert(0, 0)
        return modes

    def executeOp(self, operation, modes):
        param1 = self.memory[self.opCodeIndex + 1]
        param2 = self.memory[self.opCodeIndex + 2]
        param3 = self.memory[self.opCodeIndex + 3]

        if operation == [0, 1]:  # Add
            self.add(param1, param2, param3, modes)
        elif operation == [0, 2]:  # Multiply
            self.multiply(param1, param2, param3, modes)
        elif operation == [0, 3]:  # Store input at address
            self.storeInput(param1)
        elif operation == [0, 4]:  # Output element at address and store output
            self.storeOutput(param1)
        elif operation == [0, 5]:  # Jump if true
            self.jumpIfTrue(param1, param2, modes)
        elif operation == [0, 6]:  # Jump if false
            self.jumpIfFalse(param1, param2, modes)
        elif operation == [0, 7]:  # Is less than
            self.isLessThan(param1, param2, param3, modes)
        elif operation == [0, 8]:  # equals
            self.equals(param1, param2, param3, modes)
        elif operation == [0, 9]: # Halt
            self.halt()
        else:
            raise IndexError("Invalid OpCode: " + str(self.memory[self.opCodeIndex] +
                                                      "\nOpCodeIndex: " + str(self.opCodeIndex)))

    def getNumsFromModes(self, params, modes):
        modesCopy = modes.copy()
        digitModes = modesCopy[:3]
        digitModes.reverse()
        nums = []

        for i, param in enumerate(params):
            num = None
            if digitModes[i] == 0:
                num = self.memory[param]
            elif digitModes[i] == 1:
                num = param
            nums.append(num)

        return nums

    def add(self, param1, param2, param3, modes):
        nums = self.getNumsFromModes([param1, param2], modes)
        self.memory[param3] = nums[0] + nums[1]
        self.opCodeIndex += 4

    def multiply(self, param1, param2, param3, modes):
        nums = self.getNumsFromModes([param1, param2], modes)
        self.memory[param3] = nums[0] * nums[1]
        self.opCodeIndex += 4

    def storeInput(self, param1):
        if not self.phaseSettingUsed:
            useInput = self.phaseSetting
            self.phaseSettingUsed = True
        else:
            if self.input is None: #Need to pause this amp until we receive imput
                self.pause()
                return
            else:
                useInput = self.input
        self.memory[param1] = useInput
        self.opCodeIndex += 2

    def storeOutput(self, param1):
        output = self.memory[param1]
        # print(output)
        self.output = output
        self.opCodeIndex += 2

    def jumpIfTrue(self, param1, param2, modes):
        nums = self.getNumsFromModes([param1, param2], modes)
        if nums[0] != 0:
            return nums[1]
        self.opCodeIndex += 3

    def jumpIfFalse(self, param1, param2, modes):
        nums = self.getNumsFromModes([param1, param2], modes)
        if nums[0] == 0:
            return nums[1]
        self.opCodeIndex += 3

    def isLessThan(self, param1, param2, param3, modes):
        nums = self.getNumsFromModes([param1, param2], modes)
        if nums[0] < nums[1]:
            self.memory[param3] = 1
        else:
            self.memory[param3] = 0
        self.opCodeIndex += 4

    def equals(self, param1, param2, param3, modes):
        nums = self.getNumsFromModes([param1, param2], modes)
        if nums[0] == nums[1]:
            self.memory[param3] = 1
        else:
            self.memory[param3] = 0
        self.opCodeIndex += 4

    def pause(self):
        self.paused = True
        print("Amp " + str(self.ID) + " paused.")

    def halt(self):
        self.halted = True
        self.paused = True
        print("Amp " + str(self.ID) + " halted.")


if __name__ == "__main__":
    with open("input.txt", 'r') as myfile:
        input = myfile.read()
        originalCodes = [int(num) for num in input.split(',')]
    phasePerms = itertools.permutations(range(5, 10))
    maxOutput = 0
    bestPhaseSettings = None
    for phaseSettings in phasePerms:
        machine = Machine(originalCodes, phaseSettings)
        output = machine.runMachine()
        if output > maxOutput:
            maxOutput = output
            bestPhaseSettings = phaseSettings
    print("Answer:")
    print(maxOutput)
    print(bestPhaseSettings)





