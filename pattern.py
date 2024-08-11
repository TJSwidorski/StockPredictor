import yfinance as yf
import numpy as np
import statistics

class Pattern():
  def __init__(self, ticker_set):
    self.__tickers = ticker_set
    self.__score_results = None

  def __create_top_x(self, x, sorted_dict):
    """
    Given a sorted dictionary, returns the top [x] values as a list of
    (key, value) tuples.
    """
    top_x = []
    for key, value in sorted_dict[:x]:
      top_x.append((key, value))

    return top_x
  
  def __check_dates(self, ticker, start_date, end_date):
    if start_date and end_date:
      stock = yf.download(ticker, start=start_date, end=end_date)
    elif start_date:
      stock = yf.download(ticker, start=start_date)
    elif end_date:
      stock = yf.download(ticker, end=end_date)
    else:
      stock = yf.download(ticker)

    return stock
  
  def score(self, scoring: callable, start_date: str = None, end_date: str = None):
    """
    Scores all of the stock tickers within the set [self.__tickers] to find
    the highest scoring given scoring class [type] and may include [start_date]
    and/or [end_date].
    """
    accum_dict = {}
    progress = 0
    for ticker in self.__tickers:
      progress += 1
      print(f'Progress: {progress} of {len(self.__tickers)}')
      try:
        stock = self.__check_dates(ticker, start_date, end_date)
        ticker_score = scoring(stock)
        accum_dict[ticker] = ticker_score
      except:
        continue

    sorted_results = sorted(accum_dict.items(), \
                            key=lambda item: item[1], reverse=True)
    self.__score_results = sorted_results

    return sorted_results
  
  def get_top_x(self, x):
    """
    Returns the top ten values of the scored results in [self.__score_results]
    """
    return self.__create_top_x(x, self.__score_results)
  
class ScoringSystems():
  def result_scoring(stock):
    stock['Result'] = np.where(stock['Close'] > stock['Open'], 1, \
                      np.where(stock['Close'] == stock['Open'], None, 0))
    return statistics.mean([r for r in stock['Result'] if r is not None])
  
  def growth_scoring(stock):
    open_index = 0
    while stock['Open'].iloc[open_index] == 0:
      open_index += 1
      if open_index >= len(stock):
        break

    first_open = stock['Open'].iloc[open_index]
    last_close = stock['Close'].iloc[-1]
    return (last_close - first_open) / first_open
