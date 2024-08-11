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

  def invest(self, start_date, end_date, investment_amount):
    self.__current_amount = investment_amount
    for ticker, portion in self.__portfolio:
      stock = yf.download(ticker, start=start_date, end=end_date)

      day_start = investment_amount * portion
      number_of_shares = day_start / stock['Open'].iloc[0]

      day_start_totals = [day_start]
      day_end_totals = []
      profits_losses = []

      for i in range(len(stock)):
        if i > 0:
          day_start = day_end_totals[i-1]
          number_of_shares = day_start / stock['Open'].iloc[i]

          day_start_totals.append(day_start)

        day_end = number_of_shares * stock['Close'].iloc[i]
        profit_loss = (stock['Close'].iloc[i] - stock['Open'].iloc[i]) * number_of_shares

        day_end_totals.append(day_end)
        profits_losses.append(profit_loss)

      stock['Day Start'] = day_start_totals
      stock['Day End'] = day_end_totals
      stock['Profit/Loss'] = profits_losses
      # print(stock)

      total_profit_loss = day_end_totals[-1] - investment_amount * portion
      self.__results.append(total_profit_loss)

    #Returns the overall increase/decrease, not the percent increase/decrease
    self.__result = sum(self.__results)
    self.__current_amount = self.__result + investment_amount
    self.__percent_change = self.__result / investment_amount 
    #Could return + investment_amount to have current amount
    #Could return percent increase/decrease
  
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

#Test Portfolio creation and investment for Results Pattern
P = Portfolio(normalize(pattern.train_results))
P.invest('2024-01-01', '2024-08-10', 100)
result = P.get_result()
percent_change = P.get_percent_change()
end_amount = P.get_end_amount()
print('\nPenny stock results: ')
print(f'Penny result amount: {result}')
print(f'Percent change: {percent_change}')
print(f'End amount: {end_amount}\n')
standard, p_change, e_amount = P.find_standard('2024-01-01', '2024-08-10', 100)
print('Standard market results: ')
print(f'Standard result amount: {standard}')
print(f'Percent change: {p_change}')
print(f'End amount: {e_amount}')

