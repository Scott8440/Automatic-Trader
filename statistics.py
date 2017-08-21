import matplotlib.pyplot as plt

def movingAverage(data, n=3):
    averages = []
    dataLen = len(data)
    psum = 0
    for i in range(dataLen):
        if i < n:
            psum = prevSum(data, i, i)
            averages.append(psum / (i + 1))
        else:
            # print('old lost data: {}'.format(data[i - n]))
            # print('old gained data: {}'.format(data[i]))
            psum = psum - data[i - n] + data[i]
            averages.append(psum / n)
    return averages

def singleMovingAverage(data, index, n, previousValue):
    psum = 0
    result = 0
    if index < n:
        # print('index smaller than n')
        psum = prevSum(data, index, index)
        # print('prevSum: {}'.format(psum))
        result = (psum / (index + 1))
    else:
        # print('new lost data: {}'.format(data[index - n]))
        # print('new gained data: {}'.format(data[index]))
        oldSum = previousValue * n
        psum = oldSum - data[index - n] + data[index]
        newVal = psum / n
        # newVal = previousValue + ((data[index - n] + data[index]) / n)
        # print('new: {}'.format(newVal))
        result = newVal
    return result

def prevSum(data, index, len):
    psum = 0
    for i in range(len + 1):
        psum += data[index - i]
    return psum

# Plotting Utilities
def plotSinglePoint(x, y, color):
    plt.plot(x, y, marker='o', markersize=4, color=color)
