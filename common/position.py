import numpy as np

class Position:
    def __init__(self):
        self.share = 0
        self.buy_price = 0

    def buy(self, price):
        self.share = 1
        self.buy_price = price

    def sell(self):
        self.share = 0
        tmp_price = self.buy_price
        self.buy_price = 0
        return tmp_price
