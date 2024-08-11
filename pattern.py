import sqlite3
import database
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
    return self.__create_top_ten(self.__score_results)

#Test ResultPattern for Penny Stocks
# CONN = sqlite3.connect("stock_tickers.db")
# set_name = "penny_stocks_2024-08-07"
# penny_set = database.StockTickerDatabase.retrieve_set(CONN, set_name)
# RP = ResultPattern(penny_set)
# train_results = RP.top_ten_train('2023-12-31')
# print(train_results)
# test_results = RP.top_ten_test('2024-01-01')
# print(test_results)


class GrowthPattern():
  def __init__(self, ticker_set):
    self.__tickers = ticker_set
    self.__top_ten = None

  def __find_open(self, stock):
    """
    Removes all None values from the list and returns the mean of the list.
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

  def top_ten_train(self, end_date):
    #Find the top ten stocks with the highest growth given the end date for the "training" data
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
    self.__create_top_ten(sorted_results)

    return self.__top_ten
  
  def top_ten_test(self, start_date):
    #Test the top ten stocks beginning at the start date and record their frequencies.
    growth_dict = {}
    progress = 0
    for ticker, _ in self.__top_ten:
      progress += 1
      print(f'Progress: {progress} of {len(self.__top_ten)}')
      try:
        stock = yf.download(ticker, start=start_date)
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

    return sorted_results
  
  def set_top_ten(self, sorted_results):
    self.__top_ten = sorted_results

  def get_top_ten(self):
    return self.__top_ten
  
#Test GrowthPattern for Penny Stocks
# CONN = sqlite3.connect("stock_tickers.db")
# set_name = "penny_stocks_2024-08-07"
# penny_set = database.StockTickerDatabase.retrieve_set(CONN, set_name)
# RP = GrowthPattern(penny_set)
# train_results = RP.top_ten_train('2023-12-31')
# print(train_results)
# test_results = RP.top_ten_test('2024-01-01')
# print(test_results)