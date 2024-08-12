import matplotlib.pyplot as plt
from scipy.stats import norm
from database import *
import pattern
from sklearn.metrics import r2_score
import seaborn as sns
import pandas as pd

class StockGraph():
  def __init__(self, x, y):
    self.__x = x
    self.__y = y

  def scatter(self, title):
    df = pd.DataFrame({'Training Score': self.__x, 'Testing Score': self.__y})
    plot = sns.scatterplot(x='Training Score', y='Testing Score', data=df)
    plot.set_xlabel('Training Score')
    plot.set_ylabel('Testing Score')
    plot.set_title(title)
    sns.lmplot(x='Training Score', y='Testing Score', data=df)
    plt.show(block=True)

def sync_lists(list_a, list_b):
  common_tickers = set([ticker for ticker, _ in list_a]) & set([ticker for ticker, _ in list_b])
  list_a = [tup for tup in list_a if tup[0] in common_tickers]
  list_b = [tup for tup in list_b if tup[0] in common_tickers]

  list_a.sort(key=lambda x: x[0])
  list_b.sort(key=lambda x: x[0])

  return list_a, list_b
  

CONN = sqlite3.connect('stock_ticker_data_2024-08-11.db')

result_train_data = StockTickerDatabase.retrieve_set(CONN, 'Result Scoring end=2023-12-31')
result_test_data = StockTickerDatabase.retrieve_set(CONN, 'Result Scoring start=2024-01-01')

growth_train_data = StockTickerDatabase.retrieve_set(CONN, 'Growth Scoring end=2023-12-31')
growth_test_data = StockTickerDatabase.retrieve_set(CONN, 'Growth Scoring start=2024-01-01')

rx_data, ry_data = sync_lists(result_train_data, result_test_data)
gx_data, gy_data = sync_lists(growth_train_data, growth_test_data)

rx = [rx for _, rx in rx_data]
ry = [ry for _, ry in ry_data]
gx = [gx for _, gx in gx_data]
gy = [gy for _, gy in gy_data]

if __name__ == '__main__':
  result_scatter = StockGraph(rx, ry).scatter('Result Scoring Analysis')
  growth_scatter = StockGraph(gx, gy).scatter('Growth Scoring Analysis')