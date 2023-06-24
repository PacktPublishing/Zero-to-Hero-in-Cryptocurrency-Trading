# --- Do not remove these libs --- 
import numpy as np  # noqa 
import pandas as pd  # noqa 
from pandas import DataFrame 
  
from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter, 
                                IStrategy, IntParameter) 
  
# -------------------------------- 
# Add your lib to import here 
import talib.abstract as ta 
import freqtrade.vendor.qtpylib.indicators as qtpylib 
from functools import reduce 
  
  
class PrivateMACross(IStrategy): 
    INTERFACE_VERSION = 3 
  
    timeframe = '1d' 
    ma_short = 9 
    ma_long = 21 
  
    startup_candle_count: int = ma_long 
    can_short: bool = False 
  
    minimal_roi = { 
        "0": 10.5 
    } 
  
    stoploss = -1.0 
    trailing_stop = False 
  
    process_only_new_candles = False 
  
    use_exit_signal = True 
    exit_profit_only = False 
    ignore_roi_if_entry_signal = False 
  
    order_types = { 
        'entry': 'market', 
        'exit': 'market', 
        'stoploss': 'market', 
        'stoploss_on_exchange': False 
    } 
  
    order_time_in_force = { 
        'entry': 'gtc', 
        'exit': 'gtc' 
    } 
  
    plot_config = { 
        'main_plot': { 
            f'sma_short_9': {'color': 'red'}, 
            f'sma_long_21': {'color': 'yellow'} 
        } 
    } 
  
    def informative_pairs(self): 
        return [] 
  
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame: 
        dataframe['sma_short_9'] = ta.SMA(dataframe, timeperiod=self.ma_short) 
        dataframe['sma_long_21'] = ta.SMA(dataframe, timeperiod=self.ma_long) 
        return dataframe 
  
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame: 
        conditions_long = [] 
        conditions_long.append(qtpylib.crossed_above( 
            dataframe[f'sma_short_9'].shift(1), 
            dataframe[f'sma_long_21'].shift(1) 
            )) 
  
        if conditions_long: 
            dataframe.loc[ 
                    reduce(lambda x, y: x & y, conditions_long), 
                    'enter_long'] = 1 
  
        return dataframe 
  
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame: 
        conditions_exit_long = [] 
        conditions_exit_long.append(qtpylib.crossed_above( 
            dataframe[f'sma_long_21'], 
            dataframe[f'sma_short_9'] 
            )) 
  
        if conditions_exit_long: 
            dataframe.loc[ 
                    reduce(lambda x, y: x & y, conditions_exit_long), 
                    'exit_long'] = 1 
  
        return dataframe 