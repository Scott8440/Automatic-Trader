import statistics as stats
from TradingStrategy import TradingStrategy
from Trade import Trade

class MovingAverageStrategy(TradingStrategy):
    shortLength = 0
    longLength = 0
    shortMovingAverageList = []
    longMovingAverageList = []
    shortAboveLong = False
    longAboveShort = False
    shortAvg = 0
    longAvg = 0
    outlierAverage = 0

    def __init__(self, shortLength, longLength):
        self.shortLength = shortLength
        self.longLength = longLength

    def updateStatistics(self, history, trade):
        shortAvg = stats.singleMovingAverage(
             history['price'], self.shortLength, self.shortAvg)
        longAvg =  stats.singleMovingAverage(
             history['price'], self.longLength, self.longAvg)
        outlierAverage = stats.singleMovingAverage(
             history['price'], 100, self.outlierAverage)
        self.shortAboveLong = shortAvg > longAvg
        self.longAboveShort = longAvg > shortAvg
        self.shortAvg = shortAvg
        self.longAvg = longAvg
        self.shortMovingAverageList.append(shortAvg)
        self.longMovingAverageList.append(longAvg)
        self.outlierAverage = outlierAverage

    def checkIfShouldTrade(self, history, holding, wallet):
        coins = wallet.getCoins()
        funds = wallet.getFunds()
        if (stats.tradeIsOutlier(history['price'][-1], self.outlierAverage, 0.04)):
            return None
        if len(self.shortMovingAverageList) < 2:
            return None
        prevShortAvg = self.shortMovingAverageList[-2]
        prevLongAvg = self.longMovingAverageList[-2]
        trade = None
        if (coins and self.shortAboveLong and
              prevShortAvg < prevLongAvg):
            # Sell Coins
            trade = Trade(history['time'][-1], history['price'][-1], -coins)
        elif (funds and not self.shortAboveLong and
                prevShortAvg > prevLongAvg):
            # Buy Coins
            # subtract a small amount from funds to avoid rounding errors resulting
            # in buying more than you can afford
            amountBought = (funds - 0.001) / history['price'][-1]
            trade = Trade(history['time'][-1], history['price'][-1], amountBought)
        return trade
