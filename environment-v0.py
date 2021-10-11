import numpy as np
import gym
import enum
from simple_trading.common.stock_market import StockMarket
from simple_trading.common.position import Position, ShareHolder

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
        self.market.plot_price()

        self.observation_space = gym.spaces.Dict({
            'series_data': gym.spaces.Box(
                shape=(window_length, 1),
                low=-10.0,
                high=10.0
                ),
            'sub_input': gym.spaces.Dict({
                'latent_gain': gym.spaces.Box(
                    shape=(1,), 
                    low=-10.0, 
                    high=10.0
                    ),
                })
            })
        #print(self.observation_space['series_data'].shape)
        #print(self.observation_space['sub_input']['latent_gain'].shape)
        #print(type(self.observation_space['sub_input']))

        #for item in self.observation_space['sub_input']:
        #    print(item, type(item))

        self.action_space = gym.spaces.Discrete(3)
        
        self.window_length = window_length
        self.episode_counter = 0
        self.min_index = window_length - 1
        self.max_index = self.market.get_max_index()

    def reset(self):
        self.holder = ShareHolder()
        self.step_counter = 0
        self.current_index = self.min_index 
        current_price = self.market.get_price(self.current_index)
        self.total_reward = 0

        self.episode_counter += 1

        obs = [
                self.market.get_price_series(
                    init_index=self.current_index-self.window_length+1,
                    length=self.window_length
                    ),
                0.0
                ]
        return obs

    def step(self, action_index):
        if not Action.has_value(action_index):
            raise ValueError('action value must be less than 3')

        current_price = self.market.get_price(self.current_index)

        if Action(action_index) == Action.SELL:
            #print('SELL')
            if self.holder.number != 0:
                reward = 10 * self.sell(current_price)
                #print('Sold:', current_price)
            else:
                reward = -1

        elif Action(action_index) == Action.BUY:
            #print('BUY')
            if self.holder.number == 0:
                self.buy(current_price)
                reward = 0
                #print('Bought:', current_price)
                #reward = self.buy(current_price)
            else:
                reward = -1

        elif Action(action_index) == Action.HOLD:
            #print('HOLD')
            reward = 0

        self.total_reward += reward
        self.current_index += 1
        next_price = self.market.get_price(self.current_index)
        obs = [
                self.market.get_price_series(
                    init_index=self.current_index-self.window_length+1,
                    length=self.window_length
                    ),
                10*self.holder.get_latent_gain(next_price)
                ]
        if self.current_index == self.max_index:
            done = True
        else:
            done = False

        info = dict()

        return obs, reward, done, info

    def buy(self, price):
        self.holder.buy(price)
        return -price

    def sell(self, price):
        interests = self.holder.sell(price)
        #return price
        return interests


    def debug(self):
        print('*** Debug ***')
        obs = self.reset()
        print('Obs', obs)
        #for i in range(3):
        #    obs, reward, done, info = self.step(i)
        #    print(obs, reward, done, info)
        obs, reward, done, _ = self.step(1)
        print(obs, reward, done)
        obs, reward, done, _ = self.step(1)
        print(obs, reward, done)

    def random_play(self):
        obs = self.reset()

        done = False
        total_reward = 0
        i = 0
        while not done:
            print('*'*40)
            print('i =', i)
            if i == 0:
                action = 1
            elif i == 96:
                action = 2
            else:
                action = 0
            action = self.action_space.sample()
            print('latent_gain: ', obs[1])
            print('action is', action)
            obs, reward, done, info = self.step(action)
            total_reward += reward 
            #print(obs, reward, done, info)
            print('reward', reward)
            i += 1

        print('Total reward', total_reward)
