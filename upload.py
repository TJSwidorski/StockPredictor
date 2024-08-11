import sqlite3
from database import *
import ticker
import index
import penny
import pattern

CONN = sqlite3.connect('stock_ticker_data_2024-08-11.db')

#Upload all current and relevant data into the dated database
StockTickerDatabase.create_sets_table(CONN)
#The commented out data below has already been uploaded and running this code
#again would result in duplications of the information, any code uncommented 
#below has not been uploaded and will be uploaded when the file is run.
# StockTickerDatabase.insert_set(CONN, 'All Stock Tickers', ticker.TickerAPI().all_tickers())
# StockTickerDatabase.insert_set(CONN, 'S&P500 Data', index.IndexFundAPI().sp_500_data())
# StockTickerDatabase.insert_set(CONN, 'Nasdaq Data', index.IndexFundAPI().nasdaq_data())
# StockTickerDatabase.insert_set(CONN, 'DOW Data', index.IndexFundAPI().dow_data())
# StockTickerDatabase.insert_set(CONN, 'Penny Stocks', penny.PennyStocks().get_penny_stocks())
# penny_tickers = StockTickerDatabase.retrieve_set(CONN, 'Penny Stocks')
# base = pattern.Pattern(penny_tickers)

# result_train_data = base.score(pattern.ScoringSystems().result_scoring, end_date='2023-12-31')
# StockTickerDatabase.insert_set(CONN, 'Result Scoring end=2023-12-31', result_train_data)

# growth_train_data = base.score(pattern.ScoringSystems().growth_scoring, end_date='2023-12-31')
# StockTickerDatabase.insert_set(CONN, 'Growth Scoring end=2023-12-31', growth_train_data)

# result_test_data = base.score(pattern.ScoringSystems().result_scoring, start_date='2023-01-01')
# StockTickerDatabase.insert_set(CONN, 'Result Scoring start=2024-01-01', result_test_data)
# growth_test_data = base.score(pattern.ScoringSystems().growth_scoring, start_date='2023-01-01')
# StockTickerDatabase.insert_set(CONN, 'Growth Scoring start=2024-01-01', growth_test_data)

# result_train_data = StockTickerDatabase.delete_set(CONN, 'Result Scoring end=2023-12-31')
# growth_train_data = StockTickerDatabase.delete_set(CONN, 'Growth Scoring end=2023-12-31')

# result_test_data = StockTickerDatabase.delete_set(CONN, 'Result Scoring start=2024-01-01')
# growth_test_data = StockTickerDatabase.delete_set(CONN, 'Growth Scoring start=2024-01-01')

#Test to check all information is stored correctly
#The set_names variable below needs to be updated as new information is uploaded. 
set_names = ['All Stock Tickers', 'S&P500 Data', 'Nasdaq Data', 'DOW Data', 'Penny Stocks']
actual_names = StockTickerDatabase.retrieve_sets(CONN)

assert actual_names == set_names

CONN.close()