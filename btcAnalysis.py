from AutoTrader import AutoTrader
from BackTester import BackTester

btcFile = './PriceData/coinbaseUSD.csv'
numTrades = 10000
startingTrade = 200000
trader = AutoTrader(500, 1500, 3000)
tester = BackTester(btcFile, startingTrade, numTrades, trader)
tradeHistory = tester.getPriceData(btcFile, numTrades, startingTrade)

tester.simulate(trader, tradeHistory, 500)
trader.printResults()
trader.plotTrades()
