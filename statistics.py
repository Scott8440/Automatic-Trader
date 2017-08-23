import matplotlib.pyplot as plt


def movingAverage(data, n=3):
    averages = []
    dataLen = len(data)
    psum = 0
    for i in range(dataLen):
        if i < n:
            psum = prevSum(data, dataLen, dataLen)
            averages.append(psum / (i + 1))
        else:
            psum = psum - data[i - n] + data[i]
            averages.append(psum / n)
    return averages


def singleMovingAverage(data, n, previousValue):
    psum = 0
    result = 0
    index = len(data)
    if (index == 1):
        return data[0]
    elif index < n:
        psum = prevSum(data, index - 1, index - 1)
        result = (psum / (index))
    else:
        oldSum = previousValue * n
        psum = oldSum - data[index - 1 - n] + data[index - 1]
        newVal = psum / n
        result = newVal
    return result


def tradeIsOutlier(tradePrice, currentAverage, threshold):
    return bool(abs(tradePrice - currentAverage) > threshold*currentAverage)


def prevSum(data, index, len):
    psum = 0
    for i in range(len + 1):
        psum += data[index - i]
    return psum


# Plotting Utilities
def plotSinglePoint(x, y, color):
    plt.plot(x, y, marker='o', markersize=4, color=color)
