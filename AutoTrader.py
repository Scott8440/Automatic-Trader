import csv
import datetime
import matplotlib.pyplot as plt
import statistics as stats
from Trade import Trade

class AutoTrader:
    dataFilename = ''
    completedTrades = []
    startingFunds = 0
    funds = 0
    coins = 0
    shortLength = 0
    longLength = 0
    shouldCreatePlot = False

    # coin data
    btcTime = []
    btcPrice = []

    # Results
    tradingValue = 0
    holdingValue = 0
    valudeDifference = 0

    def __init__(self,
                 dataFilename,
                 startingFunds,
                 shortLength,
                 longLength,
                 shouldCreatePlot):
        self.dataFilename = str(dataFilename)
        self.funds = float(startingFunds)
        self.startingFunds = float(startingFunds)
        self.shortLength = shortLength
        self.longLength = longLength
        self.shouldCreatePlot = bool(shouldCreatePlot)

    def getPriceData(self, filename, numTrades, startingTrade):
        time = []
        price = []
        volume = []
        with open(filename) as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                if startingTrade > 0:
                    startingTrade -= 1
                    continue
                if numTrades > 0:
                    time.append(datetime.datetime.fromtimestamp(int(row[0])))
                    price.append(float(row[1]))
                    volume.append(float(row[2]))
                    numTrades -= 1
                else:
                    break
        self.btcPrice = price
        self.btcTime = time
        return {'time': time, 'price': price, 'volume': volume}

    def simulate(self, btcTime, btcPrice, startingFunds):
        length = len(btcTime)
        shortAvg = 0
        longAvg = 0
        outlierAverage = 0
        shortAboveLong = False
        holding = False
        for i in range(length):
            shortAvg = stats.singleMovingAverage(
                btcPrice, i, self.shortLength, shortAvg)
            longAvg = stats.singleMovingAverage(
                btcPrice, i, self.longLength, longAvg)
            outlierAverage = stats.singleMovingAverage(
                btcPrice, i, 100, outlierAverage)
            if (stats.tradeIsOutlier(btcPrice[i], outlierAverage, 0.04)):
                continue

            if (holding and shortAboveLong and shortAvg < longAvg):
                shortAboveLong = False
                holding = False
                totalSale = self.coins * btcPrice[i]
                self.funds += totalSale
                soldCoins = self.coins
                self.coins = 0
                trade = Trade('sell', btcTime[i], btcPrice[i], soldCoins)
                self.completedTrades.append(trade)
            elif (not holding and not shortAboveLong and shortAvg > longAvg):
                shortAboveLong = True
                holding = True
                self.coins += self.funds / btcPrice[i]
                self.funds = 0
                trade = Trade('buy', btcTime[i], btcPrice[i], self.coins)
                self.completedTrades.append(trade)

    def calcResults(self):
        finalPosition = self.funds + self.coins * self.btcPrice[-1]
        self.tradingValue = (
            finalPosition - self.startingFunds) / self.startingFunds
        startingValue = self.btcPrice[0]
        endingValue = self.btcPrice[-1]
        self.holdingValue = ((endingValue - startingValue) / startingValue)
        self.valueDifference = self.tradingValue - self.holdingValue

    def printResults(self):
        self.calcResults()
        print("Holding Gain: {:.2f}%".format(self.holdingValue * 100))
        print("Trading Value: {:.2f}%".format(self.tradingValue * 100))
        print("Value Difference: {}".format(self.valueDifference * 100))

    def plotTrades(self):
        numTrades = len(self.completedTrades)
        shortMovingAverageList = stats.movingAverage(
            btcPrice, self.shortLength)
        longMovingAverageList = stats.movingAverage(btcPrice, self.longLength)
        plt.plot(btcTime, btcPrice, '#5DADE2')
        plt.plot(btcTime, shortMovingAverageList, 'green')
        plt.plot(btcTime, longMovingAverageList, 'orange')
        for i in range(numTrades):
            trade = self.completedTrades[i]
            color = 'green' if trade.tradeType == 'buy' else 'red'
            stats.plotSinglePoint(trade.time, trade.price, color)
        ax = plt.gca()
        ax.patch.set_facecolor('#ABB2B9')
        plt.show()
