class Wallet:

    funds = 0
    coins = 0

    def __init__(self, initialFunds=0, initialCoins=0):
        if (initialFunds < 0 or initialCoins < 0):
            raise ValueError('cannot initiate wallet with negative values')
        self.funds = initialFunds
        self.coins = initialCoins

    def withdrawFunds(self, amount):
        if (amount < 0):
            raise ValueError('cannot withdraw negative funds')
            return
        if (amount > self.funds):
            print(amount)
            raise ValueError('cannot withdraw more funds ({}) than available ({})'.format(amount, self.funds))
            return
        self.funds -= amount

    def withdrawCoins(self, amount):
        if (amount < 0):
            raise ValueError('cannot withdraw negative coins')
            return
        if (amount > self.coins):
            raise ValueError('cannot withdraw more coins than available')
            return
        self.coins -= amount

    def depositFunds(self, amount):
        if (amount < 0):
            raise ValueError('cannot deposit negative funds')
        self.funds += amount

    def depositCoins(self, amount):
        if (amount < 0):
            raise ValueError('cannot deposit negative coins')
        self.coins += amount

    def getFunds(self):
        return self.funds

    def getCoins(self):
        return self.coins
