import numpy as np
import gym
import enum
from simple_trading.common.stock_market import StockMarket
from simple_trading.common.position import Position

class Action(enum.Enum):
    HOLD = 0
    BUY  = 1
    SELL = 2

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class SimpleTrading(gym.Env):
    def __init__(self, window_length=4):
        self.market = StockMarket()

        self.observation_space = [
                gym.spaces.Box(
                    shape=(window_length,1), 
                    low=0.0, 
                    high=1.0),
                gym.spaces.Box(
                    shape=(1,), 
                    low=0.0, 
                    high=1.0)
                ]

        self.action_space = gym.spaces.Discrete(3)
        
        self.window_length = window_length
        self.episode_counter = 0
        self.min_index = window_length - 1
        self.max_index = self.market.get_max_index()

    def reset(self):
        self.position = Position()
        self.step_counter = 0
        self.current_index = self.min_index
        current_price = self.market.get_price(self.current_index)
        self.total_reward = 0

        self.episode_counter += 1

        return 0

    def step(self, action_index):
        if not Action.has_value(action_index):
            raise ValueError('action value must be less than 3')

        #print('current_index is', self.current_index)
        current_price = self.market.get_price(self.current_index)

        if Action(action_index) == Action.SELL:
            #print('SELL')
            if self.position.share != 0:
                reward = self.sell(current_price)
            else:
                reward = 0

        elif Action(action_index) == Action.BUY:
            #print('BUY')
            self.buy(current_price)
            reward = 0

        elif Action(action_index) == Action.HOLD:
            #print('HOLD')
            reward = 0


        self.total_reward += reward
        self.current_index += 1
        obs = [
                self.market.get_price_series(
                    init_index=self.current_index-self.window_length,
                    length=self.window_length
                    ),
                self.position.share
                ]
        if self.current_index == self.max_index + 1:
            done = True
        else:
            done = False

        info = dict()

        return obs, reward, done, info

    def buy(self, price):
        self.position.buy(price)
        return -price

    def sell(self, price):
        bought_price = self.position.sell()
        return price - bought_price


    def debug(self):
        print('*** Debug ***')
        self.reset()
        for i in range(3):
            obs, reward, done, info = self.step(i)
            print(obs, reward, done, info)

        self.reset()
        for i in range(3):
            obs, reward, done, info = self.step(i)
            print(obs, reward, done, info)

    def random_play(self):
        self.reset()

        done = False
        while not done:
            action = self.action_space.sample()
            obs, reward, done, info = self.step(action)
            print(obs, reward, done, info)
