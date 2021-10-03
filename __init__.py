from gym.envs.registration import register

register(
        id='SimpleTrading-v0',
        entry_point='simple_trading.environment-v0:SimpleTrading'
        )
