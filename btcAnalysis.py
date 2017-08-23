from AutoTrader import AutoTrader
import csv
import datetime
from Trade import Trade

btcFile = './PriceData/coinbaseUSD.csv'
numTrades = 10000
startingTrade = 200000

def getPriceData(filename, numTrades, startingTrade):
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

def simulate(trader, trades, startingFunds):
    length = len(trades)
    for i in range(length):
        trader.marketUpdate(trades[i])

tradeHistory = getPriceData(btcFile, numTrades, startingTrade)

trader = AutoTrader(500, 1500, 3000)
simulate(trader, tradeHistory, 500)
trader.printResults()
trader.plotTrades()
