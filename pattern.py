import yfinance as yf
import numpy as np
import statistics

class ResultPattern():
  def __init__(self, ticker_set):
    self.__tickers = ticker_set
    self.__score_results = None

  def __remove_none(self, result_list):
    """
    Removes all None values from the list and returns the mean of the list.
    """
    results = []
    for r in result_list:
      if r != None:
        results.append(r)
  
    return statistics.mean(results)
  
  def __create_top_ten(self, sorted_dict):
    """
    Given a sorted dictionary, returns the top ten values as a list of ten
    (key, value) tuples.
    """
    top_ten = []
    for key, value in sorted_dict[:10]:
      top_ten.append((key, value))

    return top_ten

  def score(self, end_date):
    """
    Scores all of the stock tickers within the set [self.__tickers] to find
    the highest result frequencies up to [end_date].
    """
    results_dict = {}
    progress = 0
    for ticker in self.__tickers:
      progress += 1
      print(f'Progress: {progress} of {len(self.__tickers)}')
      try:
        stock = yf.download(ticker, end=end_date)
        stock['Result'] = \
          np.where(stock['Close'] > stock['Open'], 1, \
            np.where(stock['Close'] == stock['Open'], None, 0))
        ticker_results = self.__remove_none(list(stock['Result']))
        results_dict[ticker] = ticker_results
      except:
        continue
    
    sorted_results = sorted(results_dict.items(), \
                            key=lambda item: item[1], reverse=True)
    self.__score_results = sorted_results

    return sorted_results

  def get_top_ten(self):
    """
    Returns the top ten values of the scored results in [self.__score_results]
    """
    return self.__create_top_ten(self.__score_results)

class GrowthPattern():
  def __init__(self, ticker_set):
    self.__tickers = ticker_set
    self.__score_results = None

  def __find_open(self, stock):
    """
    Finds the first [open_index] where the open value is not zero.
    """
    open_index = 0
    while stock['Open'].iloc[open_index] == 0:
      open_index += 1
      if open_index >= len(stock):
        break
    
    return open_index
  
  def __create_top_ten(self, sorted_dict):
    """
    Given a sorted dictionary, returns the top ten values as a list of ten
    (key, value) tuples.
    """
    top_ten = []
    for key, value in sorted_dict[:10]:
      top_ten.append((key, value))

    self.__top_ten = top_ten

  def score(self, end_date):
    """
    Scores all of the stock tickers within the set [self.__tickers] to find
    the highest growth rates up to [end_date].
    """    
    growth_dict = {}
    progress = 0
    for ticker in self.__tickers:
      progress += 1
      print(f'Progress: {progress} of {len(self.__tickers)}')
      try:
        stock = yf.download(ticker, end=end_date)
        open_index = self.__find_open(stock)
        if open_index >= len(stock):
          continue
        first_open = stock['Open'].iloc[open_index]
        last_close = stock['Close'].iloc[-1]
        ticker_growth = (last_close - first_open) / first_open
        growth_dict[ticker] = ticker_growth
      except:
        continue
    
    sorted_results = sorted(growth_dict.items(), \
                            key=lambda item: item[1], reverse=True)
    self.__score_results = sorted_results

    return sorted_results

  def get_top_ten(self):
    """
    Returns the top ten values of the scored results in [self.__score_results]
    """
    return self.__create_top_ten(self.__score_results)