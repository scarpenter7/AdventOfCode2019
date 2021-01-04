import Amp

if __name__ == "__main__":
    with open("input.txt", 'r') as myfile:
        input = myfile.read()
        originalCodes = [int(num) for num in input.split(',')]
    amp = Amp.Amp(originalCodes, 0)
    amp.inputQueue.put(2)
    amp.runAmp()