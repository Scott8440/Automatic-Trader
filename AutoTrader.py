import matplotlib.pyplot as plt
import statistics as stats
from Trade import Trade
from TradingStrategy import TradingStrategy


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

    # Trading Strategy
    strategy = None

    def __init__(self,
                 startingFunds,
                 strategy):
        self.funds = float(startingFunds)
        self.startingFunds = float(startingFunds)
        self.history['price'] = []
        self.history['time'] = []
        # TODO: Should abstract the stats out
        self.strategy = strategy

    def marketUpdate(self, trade):
        self.history['price'].append(trade.price)
        self.history['time'].append(trade.time)
        self.strategy.updateStatistics(self.history, trade)
        trade = self.strategy.checkIfShouldTrade(
            self.history, self.holding, self.coins, self.funds)
        if (trade):
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
        plt.plot(self.history['time'],
                 self.strategy.shortMovingAverageList, 'green')
        plt.plot(self.history['time'],
                 self.strategy.longMovingAverageList, 'orange')
        for i in range(numTrades):
            trade = self.completedTrades[i]
            color = 'green' if trade.volume >= 0 else 'red'
            stats.plotSinglePoint(trade.time, trade.price, color)
        ax = plt.gca()
        ax.patch.set_facecolor('#ABB2B9')
        plt.show()
