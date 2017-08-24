from AutoTrader import AutoTrader
import csv
import datetime
from Trade import Trade
from Wallet import Wallet
import matplotlib.pyplot as plt
import statistics as stats

class BackTester:
    dataFilename = ''
    startingTradeIndex = 0
    numTrades = 0
    trader = None
    wallet = None
    startingFunds = 0

    # Results
    tradingValue = 0
    holdingValue = 0
    valudeDifference = 0

    def __init__(self, dataFilename, startingTradeIndex, numTrades, trader, wallet):
        self.dataFilename = dataFilename
        self.startingTradeIndex = startingTradeIndex
        self.numTrades = numTrades
        self.trader = trader
        self.wallet = wallet
        self.startingFunds = wallet.getFunds()

    def getPriceData(self, filename, numTrades, startingTrade):
        trades = []
        with open(filename) as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                if startingTrade > 0:
                    startingTrade -= 1
                    continue
                if numTrades > 0:
                    time = (datetime.datetime.fromtimestamp(int(row[0])))
                    price = (float(row[1]))
                    volume = (float(row[2]))
                    trade = Trade(time, price, volume)
                    trades.append(trade)
                    numTrades -= 1
                else:
                    break
        return trades

    def simulate(self, trader, trades):
        length = len(trades)
        for i in range(length):
            trader.marketUpdate(trades[i])

    def calcResults(self):
        funds = self.wallet.getFunds()
        coins = self.wallet.getCoins()
        history = self.trader.getHistory()
        finalPosition = funds + coins * history['price'][-1]
        self.tradingValue = (
            finalPosition - self.startingFunds) / self.startingFunds
        startingValue = history['price'][0]
        endingValue = history['price'][-1]
        self.holdingValue = ((endingValue - startingValue) / startingValue)
        self.valueDifference = self.tradingValue - self.holdingValue

    def printResults(self):
        self.calcResults()
        print("Holding Gain: {:.2f}%".format(self.holdingValue * 100))
        print("Trading Value: {:.2f}%".format(self.tradingValue * 100))
        print("Value Difference: {}".format(self.valueDifference * 100))

    def plotTrades(self):
        completedTrades = self.trader.getCompletedTrades()
        numTrades = len(completedTrades)
        strategy = self.trader.getStrategy()
        history = self.trader.getHistory()

        plt.plot(history['time'], history['price'], '#5DADE2')
        plt.plot(history['time'],
                 strategy.shortMovingAverageList, 'green')
        plt.plot(history['time'],
                 strategy.longMovingAverageList, 'orange')
        for i in range(numTrades):
            trade = completedTrades[i]
            color = 'green' if trade.volume >= 0 else 'red'
            stats.plotSinglePoint(trade.time, trade.price, color)
        ax = plt.gca()
        ax.patch.set_facecolor('#ABB2B9')
        plt.show()
