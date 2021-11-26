import numpy as np


class ShareHolder:
    def __init__(self, max_share, reward_gain):
        self.max_share = max_share
        self.n_share = 0
        self.sum_share = 0.0
        self.reward_gain = reward_gain

    def buy(self, price, volume):
        if volume + self.n_share > self.max_share:
            return -1
        else:
            self.n_share += volume
            self.sum_share += price * volume
            return 0

    def sell(self, price, volume):
        if self.n_share == 0:
            return -1

        else:
            actual_volume = min(volume, self.n_share)
            average_price = self.sum_share / self.n_share
            self.n_share -= actual_volume
            total_price = price * actual_volume
            self.sum_share = max(0, self.sum_share-total_price)

            return self.reward_gain * actual_volume * (price - average_price)

    def get_latent_gain(self, price):
        if self.n_share == 0:
            return 0;
        else:
            return price - (self.sum_share / self.n_share)


