import sqlite3
from database import *
import ticker
import index
import penny

CONN = sqlite3.connect('stock_ticker_data_2024-08-11.db')

#Upload all current and relevant data into the dated database
StockTickerDatabase.create_sets_table(CONN)
StockTickerDatabase.insert_set(CONN, 'All Stock Tickers', ticker.TickerAPI().all_tickers())
StockTickerDatabase.insert_set(CONN, 'S&P500 Data', index.IndexFundAPI().sp_500_data())
StockTickerDatabase.insert_set(CONN, 'Nasdaq Data', index.IndexFundAPI().nasdaq_data())
StockTickerDatabase.insert_set(CONN, 'DOW Data', index.IndexFundAPI().dow_data())
# StockTickerDatabase.insert_set(CONN, 'Penny Stocks', penny.PennyStocks().get_penny_stocks())

#Test to check all information is stored correctly
set_names = ['All Stock Tickers', 'S&P500 Data', 'Nasdaq Data', 'DOW Data']
actual_names = StockTickerDatabase.retrieve_sets(CONN)

assert actual_names == set_names

