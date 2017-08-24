
class Trade:
    volume = 0
    price = 0
    time = 0

    def __init__(self, time, price, volume):
        self.time = time
        self.price = price
        self.volume = volume
