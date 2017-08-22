
class Trade:
    volume = 0
    price = 0
    time = 0
    tradeType = ''

    def __init__(self, tradeType, time, price, volume):
        self.tradeType = tradeType
        self.time = time
        self.price = price
        self.volume = volume
