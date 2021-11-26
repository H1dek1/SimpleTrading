import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class StockMarket:
    def __init__(self):
        """
        custom function
        """
        #t = np.arange(-3, 3, 0.06)
        #val = np.tanh(t)

        t = np.arange(-np.pi, np.pi, np.pi/50)
        #val = -np.sin(2*t)
        #val = -np.sin(2*t) + 1
        val = np.sin(t) + 1.0

        # val = np.arange(0, 100, 1)

        self.df = pd.DataFrame({
            'price': val
            })

        """
        read from csv
        """
        """
        others
        """
    def plot_price(self):
        fig, ax = plt.subplots(1, 1)
        ax.plot(range(len(self.df['price'])), self.df['price'])
        ax.set_xlabel('time', fontsize=20)
        ax.set_ylabel('price', fontsize=20)
        fig.savefig('price.png')

    def get_max_index(self):
        return len(self.df) - 1

    def get_price(self, index):
        return self.df['price'][index]

    def get_price_series(self, init_index, length):
        return self.df['price'][init_index:init_index+length].values

