import sqlite3
import database
import yfinance as yf
import numpy as np
import statistics

class ResultPattern():
  def __init__(self, ticker_set):
    self.__tickers = ticker_set
    self.__top_ten = None

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

    self.__top_ten = top_ten

  def top_ten_train(self, end_date):
    #Find the top ten stocks with the highest result frequencies given the end date for the "training" data
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
    self.__create_top_ten(sorted_results)

    return self.__top_ten
  
  def top_ten_test(self, start_date):
    #Test the top ten stocks beginning at the start date and record their frequencies.
    results_dict = {}
    progress = 0
    for ticker, _ in self.__top_ten:
      progress += 1
      print(f'Progress: {progress} of {len(self.__top_ten)}')
      try:
        stock = yf.download(ticker, start=start_date)
        stock['Result'] = \
          np.where(stock['Close'] > stock['Open'], 1, \
            np.where(stock['Close'] == stock['Open'], None, 0))
        ticker_results = self.__remove_none(list(stock['Result']))
        results_dict[ticker] = ticker_results
      except:
        continue
    
    sorted_results = sorted(results_dict.items(), \
                            key=lambda item: item[1], reverse=True)

    return sorted_results
  
  def set_top_ten(self, sorted_results):
    self.__top_ten = sorted_results

  def get_top_ten(self):
    return self.__top_ten

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

  def __remove_none(self, result_list):
    """
    Removes all None values from the list and returns the mean of the list.
    """
    results = []
    for r in result_list:
      if (r != None) and (r != 0):
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
        stock['Growth'] = \
          np.where(stock['Open'] != 0, \
                   (stock['Close'] - stock['Open']) / stock['Open'], None) 
        ticker_growth = self.__remove_none(list(stock['Growth']))
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
        stock['Growth'] = \
          np.where(stock['Open'] != 0, \
                   (stock['Close'] - stock['Open']) / stock['Open'], None)
        ticker_results = self.__remove_none(list(stock['Growth']))
        growth_dict[ticker] = ticker_results
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