import yfinance as yf
import pattern

def normalize(tuple_group):
  total = 0
  for t in tuple_group:
    total += t[1]

  folder = []
  for ticker, percentage in tuple_group:
    n = percentage / total
    folder.append((ticker, n))
  
  return folder

class Portfolio():
  def __init__(self, portfolio):
    """
    Where [portfolio] is a list of tuples containing the stock ticker and the 
    portion of the portfolio which the ticker will obtain. (ticker, percentage)

    The sum of all the ticker percentages must add up to one.
    """
    self.__portfolio = portfolio
    self.__results = []
    self.__result = None
    self.__current_amount = None
    self.__percent_change = None

  def invest(self, start_date, end_date, total_investment_amount):
        self.__current_amount = total_investment_amount
        self.__results = []
        for ticker, portion in self.__portfolio:
            stock = yf.download(ticker, start=start_date, end=end_date)
            first_open = stock['Open'].iloc[0]
            last_close = stock['Close'].iloc[-1]

            start_amount = total_investment_amount * portion
            number_of_shares = start_amount / first_open
            end_amount = last_close * number_of_shares

            self.__results.append(end_amount)

        self.__current_amount = sum(self.__results)
        self.__result = self.__current_amount - total_investment_amount
        self.__percent_change = (self.__current_amount - total_investment_amount) / total_investment_amount
      
  def get_result(self):
    return self.__result
  
  def get_end_amount(self):
    return self.__current_amount
  
  def get_percent_change(self):
    return self.__percent_change
  
  def find_standard(self, start_date, end_date, investment_amount):
    #Runs the investment on the S&P 500 index as a standard for the overall i/d
    standard_portfolio = Portfolio([('^GSPC', 1)])
    standard_portfolio.invest(start_date, end_date, investment_amount)
    result = standard_portfolio.get_result()
    percent_change = standard_portfolio.get_percent_change()
    end_amount = standard_portfolio.get_end_amount()
    return (result, percent_change, end_amount)

# #Test Portfolio creation and investment for Results Pattern
# P = Portfolio(normalize(pattern.train_results))
# P.invest('2024-01-01', '2024-08-10', 100)
# result = P.get_result()
# percent_change = P.get_percent_change()
# end_amount = P.get_end_amount()
# print('\nPenny stock results: ')
# print(f'Penny result amount: {result}')
# print(f'Percent change: {percent_change}')
# print(f'End amount: {end_amount}\n')
# standard, p_change, e_amount = P.find_standard('2024-01-01', '2024-08-10', 100)
# print('Standard market results: ')
# print(f'Standard result amount: {standard}')
# print(f'Percent change: {p_change}')
# print(f'End amount: {e_amount}')

#Test Portfolio creation and investment for Growth Pattern
# growth_results = [('FSI', 317.3333250031704), ('PRPH', 35.15999984741211), ('ZJYL', 30.0062499194406), ('KRMD', 21.318181245533886), ('ACCD', 20.836363579221995), ('NTIP', 15.76923189783947), ('RFIL', 15.213333129882812), ('SOTK', 14.738181374289773), ('GGB', 12.61880750537609), ('JCTCF', 11.611599507221607)]
# P = Portfolio(normalize(growth_results))
# P.invest('2024-01-01', '2024-08-10', 1000)
# result = P.get_result()
# percent_change = P.get_percent_change()
# end_amount = P.get_end_amount()
# print('\nPenny stock results: ')
# print(f'Penny result amount: {result}')
# print(f'Percent change: {percent_change}')
# print(f'End amount: {end_amount}\n')
# standard, p_change, e_amount = P.find_standard('2024-01-01', '2024-08-10', 1000)
# print('Standard market results: ')
# print(f'Standard result amount: {standard}')
# print(f'Percent change: {p_change}')
# print(f'End amount: {e_amount}')

