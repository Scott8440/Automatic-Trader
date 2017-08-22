from AutoTrader import AutoTrader

btcFile = './PriceData/coinbaseUSD.csv'
numTrades = 1000000
startingTrade = 200000

trader = AutoTrader(btcFile, 500, 1500, 3000, True)

data = trader.getPriceData(btcFile, numTrades, startingTrade)
btcTime = data.get('time')
btcPrice = data.get('price')

trader.simulate(btcTime, btcPrice, 500)
trader.printResults()
# trader.plotTrades()
