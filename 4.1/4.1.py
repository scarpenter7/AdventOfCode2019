# Your puzzle input is 271973-785961


def checkValid(num):
    digitList = [int(digit) for digit in str(num)]
    doubleSet = False
    for i in range(len(digitList) - 1):
        digit1 = digitList[i]
        digit2 = digitList[i + 1]
        if digit1 > digit2:
            return 0
        if (not doubleSet) and getRepeatLength(digitList, digit1) == 2:
            doubleSet = True
    if not doubleSet:
        return 0
    return 1

def getRepeatLength(digitList, num):
    length = 0
    numFound = False
    for i in range(len(digitList)):
        if digitList[i] == num:
            length += 1
            numFound = True
        elif numFound:
            break
    return length


print(sum([checkValid(num) for num in range(271973, 785962)]))



