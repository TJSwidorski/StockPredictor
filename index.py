import yfinance as yf
import numpy as np

class IndexFundAPI():
  def __init__(self):
    self.__sp_500 = yf.Ticker('^GSPC').history(period='max')
    self.__nasdaq = yf.Ticker('^IXIC').history(period='max')
    self.__dow = yf.Ticker('^DJI').history(period='max')
    self.__all = [self.__sp_500, self.__nasdaq, self.__dow]

  def clean_data(self, data):
      del data['Dividends']
      del data['Stock Splits']
      del data['High']
      del data['Low']
      del data['Volume']
      data = data.loc['1990-01-01':].copy()
      data = data.resample('D').mean() 
      not_NaN = (data['Open'].notna()) & (data['Close'].notna())
      growth = (data['Close'] - data['Open']) / data['Open']
      data['Growth'] = np.where(not_NaN & (data['Open'] != 0), growth, np.nan)

      inc = (data['Close'] > data['Open'])
      eq = (data['Close'] == data['Open'])
      data['Result'] = np.where(not_NaN & inc, 1, \
                        np.where(not_NaN & eq, np.nan, np.where(not_NaN, 0, np.nan)))
      return data

  def sp_500_data(self):
    self.__sp_500 = self.clean_data(self.__sp_500)
    return self.__sp_500
  
  def nasdaq_data(self):
    self.__nasdaq = self.clean_data(self.__nasdaq)
    return self.__nasdaq
  
  def dow_data(self):
    self.__dow = self.clean_data(self.__dow)
    return self.__dow

indFund = IndexFundAPI()
sp = indFund.sp_500_data()
n = indFund.nasdaq_data()
d = indFund.dow_data()

print(f'sp_500 data: {sp}')
print(f'nasdaq data: {n}')
print(f'dow data: {d}')