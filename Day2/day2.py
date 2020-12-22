

def run(codes):

    for num in range(0, len(codes), 4):
        if codes[num] == 1:
            codes[num + 3] = codes[num + 1] + codes[num + 2]
        elif codes[num] == 2:
            codes[num + 3] = codes[num + 1] * codes[num + 2]
        elif codes[num] == 99:
            return codes
        else:
            print("ERROR: " + str(codes[num]))

    return codes

if __name__ == "__main__":
    codes = []
    with open("code.txt", 'r') as myfile:
        lines = myfile.readlines()
        for line in lines:
            codes += line.split(',')
        codes = [int(num) for num in codes if num != '\n']
    print(codes)
    finalCodes = run(codes)


