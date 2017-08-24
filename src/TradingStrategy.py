class TradingStrategy:
    # Abstract class meant to be extended to implement various trading strategies

    # Class members should include various statistical measure.
    # E.g. movingAverage

    def updateStatistics(self, history, trade):
        # Update class members based on new market conditions (more trades on books)
        return None

    def checkIfShouldTrade(self, history, holding, wallet):
        # Checks if a trader should make a trade, based on the current market
        # environment. Returns None if no trade should be made,
        # otherwise returns a Trade
        return None

    def plotStatistics(self, plot):
        # overlay stastical plots onto the plot of stock prices
        return None
