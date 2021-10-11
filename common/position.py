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

class ShareHolder:
    def __init__(self):
        self.number = 0
        self.net_bought_price = 0.0

    def buy(self, price):
        self.number += 1
        self.net_bought_price += price * 1

    def sell(self, price):
        thresh_price = self.net_bought_price

        self.number = 0
        self.net_bought_price = 0
        #self.number -= n TODO
        #self.net_bought_price = min(0.0, self.net_bought_price-price) TODO
        return (price - thresh_price) * 1

    def average_net_bought_price(self):
        return self.net_bought_price / self.number

    def get_latent_gain(self, price):
        if self.number == 0:
            return 0;
        else:
            return price - self.net_bought_price


