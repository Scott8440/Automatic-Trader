from AutoTrader import AutoTrader
from BackTester import BackTester
from MovingAverageStrategy import MovingAverageStrategy

btcFile = './PriceData/coinbaseUSD.csv'
numTrades = 10000
startingTrade = 200000

strategy = MovingAverageStrategy(1500, 3000)
trader = AutoTrader(500, strategy)
tester = BackTester(btcFile, startingTrade, numTrades, trader)

tradeHistory = tester.getPriceData(btcFile, numTrades, startingTrade)
tester.simulate(trader, tradeHistory, 500)
trader.printResults()
trader.plotTrades()
