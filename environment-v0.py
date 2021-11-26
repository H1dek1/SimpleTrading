import sys
import numpy as np
import gym
import enum
from simple_trading.common.stock_market import StockMarket
from simple_trading.common.position import ShareHolder

class SimpleTrading(gym.Env):
    def __init__(self, window_length=4, max_share=1, reward_gain=1.0, latent_gain=1.0):
        self.market = StockMarket()
        self.market.plot_price()
        self.max_share = max_share
        self.reward_gain = reward_gain
        self.l_gain = latent_gain
        self.n_actions = 2*self.max_share + 1

        self.buy_actions = dict()
        self.hold_actions = dict()
        self.sell_actions = dict()
        for i in range(self.n_actions):
            if i < self.max_share:
                self.buy_actions[i] = i + 1
            elif i == self.max_share:
                self.hold_actions[i] = 0
            elif i > self.max_share:
                self.sell_actions[i] = i - self.max_share

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

        self.action_space = gym.spaces.Discrete(self.n_actions)
        
        self.window_length = window_length
        self.episode_counter = 0
        self.min_index = window_length - 1
        self.max_index = self.market.get_max_index()

    def reset(self):
        self.holder = ShareHolder(
                self.max_share,
                reward_gain=self.reward_gain,
                )
        self.step_counter = 0
        self.current_index = self.min_index 
        current_price = self.market.get_price(self.current_index)
        self.total_reward = 0
        latent_gain = 0.0

        self.episode_counter += 1

        obs = [
                self.market.get_price_series(
                    init_index=self.current_index-self.window_length+1,
                    length=self.window_length
                    ),
                latent_gain
                ]
        return obs

    def step(self, action_index):
        current_price = self.market.get_price(self.current_index)
        if action_index in self.buy_actions:
            reward = self.holder.buy(
                    price=current_price,
                    volume=self.buy_actions[action_index]
                    )
        elif action_index in self.sell_actions:
            reward = self.holder.sell(
                    price=current_price,
                    volume=self.sell_actions[action_index]
                    )
        elif action_index in self.hold_actions:
            reward = 0
        else:
            raise ValueError('action value must be less than 3')


        self.total_reward += reward
        self.current_index += 1
        next_price = self.market.get_price(self.current_index)
        obs = [
                self.market.get_price_series(
                    init_index=self.current_index-self.window_length+1,
                    length=self.window_length
                    ),
                self.l_gain * self.holder.get_latent_gain(next_price)
                ]
        if self.current_index == self.max_index:
            done = True
        else:
            done = False

        info = dict()
        info['n_share'] = self.holder.n_share
        info['sum_share'] = self.holder.sum_share

        return obs, reward, done, info

    def debug(self):
        print('*** Debug ***')
        obs = self.reset()
        print('Obs', obs)
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
            print('reward', reward)
            i += 1

        print('Total reward', total_reward)
