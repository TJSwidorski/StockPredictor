import ticker
import yfinance as yf

class PennyStocks():
  def __init__(self, date):
    """
    Where [date] is the current date.
    """
    self.__ticker_pool = ticker.TickerAPI().all_tickers()
    self.__penny_stocks = set()
    #Create set for all current penny stocks
    count = 0
    for t in self.__ticker_pool:
      count += 1
      print(f'{count} of {len(self.__ticker_pool)}')
      try:
        stock = yf.download(t, start=date)
        if stock['Close'].item() <= 5:
          self.__penny_stocks.add(t)
      except:
        continue

  def update(self, date):
    """
    Where [date] is the current date.
    """
    #Creates a new set with all current penny stocks
    self.__penny_stocks = set()
    count = 0
    for t in self.__ticker_pool:
      count += 1
      print(f'{count} of {len(self.__ticker_pool)}')
      try:
        stock = yf.download(t, start=date)
        if stock['Close'].item() <= 5:
          self.__penny_stocks.add(t)
      except:
        continue

  def get_penny_stocks(self):
    return self.__penny_stocks