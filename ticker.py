from yahoo_fin import stock_info as si
import pandas as pd

class TickerAPI():
  def __init__(self):
    #Initialize DataFrames
    sp_500_df = pd.DataFrame(si.tickers_sp500())
    nasdaq_df = pd.DataFrame(si.tickers_nasdaq())
    dow_df = pd.DataFrame(si.tickers_dow())
    other_df = pd.DataFrame(si.tickers_other())

    #Global Variables
    self.__sp_500 = set(s for s in sp_500_df[0].values.tolist())
    self.__nasdaq = set(s for s in nasdaq_df[0].values.tolist())
    self.__dow = set(s for s in dow_df[0].values.tolist())
    self.__other = set(s for s in other_df[0].values.tolist())

    self.__all_tickers = set.union(self.__sp_500, self.__nasdaq, self.__dow, self.__other)

    self.__del_suffix = ['W', 'R', 'P', 'Q']

  def __get_tickers(self, tickers):
    del_set = set()
    save_set = set()
    for ticker in tickers:
      if len(ticker) > 4 and ticker[-1] in self.__del_suffix:
        del_set.add(ticker)
      elif len(ticker) == 0:
        del_set.add(ticker)
      else:
        save_set.add(ticker)

    return save_set

  def sp_500_tickers(self):
    sp_500_tickers = self.__get_tickers(self.__sp_500)
    return sp_500_tickers
  
  def nasdaq_tickers(self):
    nasdaq_tickers = self.__get_tickers(self.__nasdaq)
    return nasdaq_tickers
  
  def dow_tickers(self):
    dow_tickers = self.__get_tickers(self.__dow)
    return dow_tickers

  def other_tickers(self):
    other_tickers = self.__get_tickers(self.__other)
    return other_tickers

  def all_tickers(self):
    all_tickers = self.__get_tickers(self.__all_tickers)
    return all_tickers
