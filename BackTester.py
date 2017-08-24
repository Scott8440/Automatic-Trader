from AutoTrader import AutoTrader
import csv
import datetime
from Trade import Trade


class BackTester:
    dataFilename = ''
    startingTrade = 0
    numTrades = 0
    trader = None

    def __init__(self, dataFilename, startingTrade, numTrades, trader):
        self.dataFilename = dataFilename
        self.startingTrade = startingTrade
        self.numTrades = numTrades
        self.trader = trader

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

    def simulate(self, trader, trades, startingFunds):
        length = len(trades)
        for i in range(length):
            trader.marketUpdate(trades[i])
