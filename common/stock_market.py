import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class StockMarket:
    def __init__(self):
        """
        custom function
        """
        t = np.arange(0, 100, 1)
        val = t
        self.df = pd.DataFrame({
            'price': val
            })

        """
        read from csv
        """
        """
        others
        """
    def get_max_index(self):
        return len(self.df) - 1

    def get_price(self, index):
        return self.df['price'][index]

    def get_price_series(self, init_index, length):
        return self.df['price'][init_index:init_index+length].values

