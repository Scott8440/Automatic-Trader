from AutoTrader import AutoTrader
from BackTester import BackTester
from MovingAverageStrategy import MovingAverageStrategy
from Wallet import Wallet

btcFile = './PriceData/coinbaseUSD.csv'
numTrades = 10000
startingTradeIndex = 200000
strategy = MovingAverageStrategy(1500, 3000)

wallet = Wallet(500, 0)
trader = AutoTrader(wallet, strategy)
tester = BackTester(btcFile, startingTradeIndex, numTrades, trader, wallet)

tradeHistory = tester.getPriceData(btcFile, numTrades, startingTradeIndex)
tester.simulate(trader, tradeHistory)
tester.printResults()
tester.plotTrades()
