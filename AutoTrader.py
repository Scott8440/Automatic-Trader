import matplotlib.pyplot as plt
import statistics as stats
from Trade import Trade

class AutoTrader:
    completedTrades = []

    # wallet status
    startingFunds = 0
    funds = 0
    coins = 0
    holding = False

    # trade history
    history = {}

    # statistics
    marketStats = {}
    shortLength = 0
    longLength = 0

    # Results
    tradingValue = 0
    holdingValue = 0
    valudeDifference = 0

    def __init__(self,
                 startingFunds,
                 shortLength,
                 longLength):
        self.funds = float(startingFunds)
        self.startingFunds = float(startingFunds)
        self.history['price'] = []
        self.history['time'] = []
        # TODO: Should abstract the stats out
        self.shortLength = shortLength
        self.longLength = longLength
        self.marketStats['shortMovingAverageList'] = []
        self.marketStats['longMovingAverageList'] = []
        self.marketStats['shortAboveLong'] = False
        self.marketStats['longAboveShort'] = False
        self.marketStats['shortAvg'] = 0
        self.marketStats['longAvg'] = 0
        self.marketStats['outlierAverage'] = 0

    def marketUpdate(self, trade):
        self.history['price'].append(trade.price)
        self.history['time'].append(trade.time)
        self.updateStatistics(trade)
        self.checkIfShouldTrade()

    def updateStatistics(self, trade):
        shortAvg = stats.singleMovingAverage(
            self.history['price'], self.shortLength, self.marketStats['shortAvg'])
        longAvg =  stats.singleMovingAverage(
            self.history['price'], self.longLength, self.marketStats['longAvg'])
        outlierAverage = stats.singleMovingAverage(
            self.history['price'], 100, self.marketStats['outlierAverage'])
        self.marketStats['shortAboveLong'] = shortAvg > longAvg
        self.marketStats['longAboveShort'] = longAvg > shortAvg
        self.marketStats['shortAvg'] = shortAvg
        self.marketStats['longAvg'] = longAvg
        self.marketStats['shortMovingAverageList'].append(shortAvg)
        self.marketStats['longMovingAverageList'].append(longAvg)
        self.marketStats['outlierAverage'] = outlierAverage

    def checkIfShouldTrade(self):
        if (stats.tradeIsOutlier(self.history['price'][-1], self.marketStats['outlierAverage'], 0.04)):
            console.log('outlier')
            return
        if len(self.marketStats['shortMovingAverageList']) < 2:
            return
        prevShortAvg = self.marketStats['shortMovingAverageList'][-2]
        prevLongAvg = self.marketStats['longMovingAverageList'][-2]
        if (self.holding and self.marketStats['shortAboveLong'] and
              prevShortAvg < prevLongAvg):
            # Sell Coins
            print('sell')
            trade = Trade(self.history['time'][-1], self.history['price'][-1], -self.coins)
            self.tradeCoins(trade)
        elif (not self.holding and not self.marketStats['shortAboveLong'] and
                prevShortAvg > prevLongAvg):
            # Buy Coins
            print('buy')
            amountBought = self.funds / self.history['price'][-1]
            trade = Trade(self.history['time'][-1], self.history['price'][-1], amountBought)
            self.tradeCoins(trade)

    def tradeCoins(self, trade):
        self.coins += trade.volume
        self.funds -= trade.volume * trade.price
        self.holding = self.coins > 0
        self.completedTrades.append(trade)

    def calcResults(self):
        finalPosition = self.funds + self.coins * self.history['price'][-1]
        self.tradingValue = (
            finalPosition - self.startingFunds) / self.startingFunds
        startingValue = self.history['price'][0]
        endingValue = self.history['price'][-1]
        self.holdingValue = ((endingValue - startingValue) / startingValue)
        self.valueDifference = self.tradingValue - self.holdingValue

    def printResults(self):
        self.calcResults()
        print("Holding Gain: {:.2f}%".format(self.holdingValue * 100))
        print("Trading Value: {:.2f}%".format(self.tradingValue * 100))
        print("Value Difference: {}".format(self.valueDifference * 100))

    def plotTrades(self):
        numTrades = len(self.completedTrades)
        plt.plot(self.history['time'], self.history['price'], '#5DADE2')
        plt.plot(self.history['time'], self.marketStats['shortMovingAverageList'], 'green')
        plt.plot(self.history['time'], self.marketStats['longMovingAverageList'], 'orange')
        for i in range(numTrades):
            trade = self.completedTrades[i]
            color = 'green' if trade.volume >= 0 else 'red'
            stats.plotSinglePoint(trade.time, trade.price, color)
        ax = plt.gca()
        ax.patch.set_facecolor('#ABB2B9')
        plt.show()
