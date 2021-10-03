import numpy as np
import gym
from simple_trading.common.stock_market import StockMarket

class SimpleTrading(gym.Env):
    def __init__(self):
        market = StockMarket()
        print('get_one_price(1)', market.get_one_price(1))
        print('get_price_series(1, 10)', market.get_price_series(1, 10))
        self.observation_space = gym.spaces.Box(
                shape=(2,),
                low = np.array([0.0, 0.0], dtype=np.float32),
                high= np.array([1.0, 1.0], dtype=np.float32),
                )
        self.action_space = gym.spaces.Discrete(3)

    def reset(self):
        return 0

    def step(self, action):
        return 0
