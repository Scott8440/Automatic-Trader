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

    # Trading Strategy
    strategy = None

    def __init__(self,
                 wallet,
                 strategy):
        self.wallet = wallet
        self.history['price'] = []
        self.history['time'] = []
        # TODO: Should abstract the stats out
        self.strategy = strategy

    def marketUpdate(self, trade):
        self.history['price'].append(trade.price)
        self.history['time'].append(trade.time)
        self.strategy.updateStatistics(self.history, trade)
        trade = self.strategy.checkIfShouldTrade(
            self.history, self.holding, self.wallet)
        if (trade):
            self.tradeCoins(trade)

    def tradeCoins(self, trade):
        vol = trade.volume
        price = trade.price
        if (vol > 0):
            self.wallet.depositCoins(vol)
            self.wallet.withdrawFunds(vol * price)
        else:
            self.wallet.withdrawCoins(-vol)
            self.wallet.depositFunds(-vol * price)
        self.holding = self.wallet.getCoins() > 0
        self.completedTrades.append(trade)

    def getCompletedTrades(self):
        return self.completedTrades

    def getStrategy(self):
        return self.strategy

    def getHistory(self):
        return self.history
