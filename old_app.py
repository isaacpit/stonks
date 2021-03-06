import os 
import pprint as pp
from collections import defaultdict
import argparse

import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

IDX_DATE = 0
IDX_TRANSACTION_ID = 1
IDX_DESCRIPTION = 2
IDX_QUANTITY = 3
IDX_SYMBOL = 4
IDX_PRICE = 5
IDX_COMMISSION = 6
IDX_AMOUNT = 7
IDX_REG_FEE = 8
IDX_SHORT_TERM_RDM_FEE = 9
IDX_FUND_REDEMPTION_FEE = 10
IDX_DEFERRED_SALES_CHARGE = 11

parser = argparse.ArgumentParser(description='Gather Transaction Data')
parser.add_argument("-v", "--verbose",action="store_true")
parser.add_argument("-f", "--file", nargs=1, type=str, default=["all_transactions.csv"])
parser.add_argument("-t", "--transactions", action="store_true")
parser.add_argument("-l", "--list", action="store_true")
# only run once 
parser.add_argument("-a", "--api", action="store_true")

parsed_args = parser.parse_args()

if parsed_args.verbose: 
  parser.print_help()
  print(parsed_args)


f=None
try:
  f = open(parsed_args.file[0], "r")
except Exception as ex:
  print(ex)
  raise ex
# print(f.read())

i = 0

str_heading = f.readline();
arr_headings = str_heading.split(",")
n_arr_headings = len(arr_headings)
def clean_str(a):
  res = a.strip()
  return res

def validate_input(a_input):
  
  for j in range(len(a_input)):
    a_input[j] = clean_str(a_input[j])


class TickerWrapper:
  data = None
  map_tickers = defaultdict(lambda : 0)
  map_transactions =  defaultdict(lambda : [])
  map_transaction_fees =  defaultdict(lambda : 0)
  is_verbose = parsed_args.verbose
  is_show_transactions = parsed_args.transactions
  is_api = parsed_args.api

  def __init__(self):
    pass

  @staticmethod
  def run_all_eligibile_api():
      pass

  @staticmethod
  def run():
    cls()
    parser.print_help()
    
    if TickerWrapper.is_api:
      TickerWrapper.run_all_eligibile_api()
      return
    user_choice = TickerWrapper.get_input()
    continue_playing = TickerWrapper.handle_input(user_choice)
    while(continue_playing):
      
      user_choice = TickerWrapper.get_input()
      continue_playing=TickerWrapper.handle_input(user_choice)

  @staticmethod 
  def handle_input(str_input):
      print(str_input)
      continue_playing = True
      if str_input == "t":
        TickerWrapper.display_transactions()
      elif str_input == "q":
        continue_playing = False
      print("continue? : ", continue_playing)
      return continue_playing
    
  @staticmethod
  def get_input():
    return input("> ")

  @staticmethod
  def display_transactions_helper(txs):
    for tx in txs:
      # print(tx)
      print("\t\t{0:>70} {1:>10}".format(tx[0], tx[1]))
      if tx[2]:
        print("\t\t{0:70} {1:25.2f}".format("", tx[2]))

  @staticmethod 
  def display_transactions(ticker = None):
    if ticker == None:
      
      tickers = TickerWrapper.map_tickers.keys()
      for ticker in tickers:
        # print(ticker, "show_transactions: ", TickerWrapper.is_show_transactions)
        TickerWrapper.display_transactions_helper(TickerWrapper.map_transactions[ticker])

    else:
      TickerWrapper.display_transactions_helper(TickerWrapper.map_transactions[ticker])

  @staticmethod
  def set_data(data_matrix):
    
    arr_funds=[]
    
    # print( TickerWrapper.is_verbose: ", TickerWrapper.is_verbose)

    TickerWrapper.data = data_matrix
    # loop through all rows
    for i in range(len(TickerWrapper.data)):
      arr_row_items = TickerWrapper.data[i]
      # print(arr_row_items)
      
      description = arr_row_items[IDX_DESCRIPTION]
      str_symbol_text = arr_row_items[IDX_SYMBOL]
      str_amount = arr_row_items[IDX_AMOUNT]
      str_date = arr_row_items[IDX_DATE]
      
      if TickerWrapper.is_verbose:
        print(description)
      has_fund=description.lower().find("fund".lower()) > 0
      has_now=description.lower().find("now".lower()) > 0
      is_funding= has_fund and has_now

      # print("S: ", str_symbol_text)
      if is_funding:
        arr_funds.append(("FUNDING", arr_row_items[IDX_AMOUNT], str_date))
      
      if len(str_symbol_text) > 0:
        symbol = str_symbol_text.split()[0]
        str_bought_sold = description.split()[0]
        
        
        is_bought = str_bought_sold == "Bought"
        is_sold = str_bought_sold == "Sold"

        # print("---", arr_row_items[IDX_COMMISSION])
        f_reg_fee = None
        if arr_row_items[IDX_REG_FEE]:
          f_reg_fee = abs(float(arr_row_items[IDX_COMMISSION]))
          if is_bought or is_sold:
            # print("ipit: ", TickerWrapper.map_transaction_fees[symbol])
            TickerWrapper.map_transaction_fees[symbol] += f_reg_fee

        if is_bought:
          # print("BOUGHT")
          TickerWrapper.map_tickers[symbol] -= abs(float(arr_row_items[IDX_AMOUNT]))
          TickerWrapper.map_transactions[symbol].append(("BOUGHT {0} {1}".format(symbol, description), float(str_amount), f_reg_fee, str_date))
        elif is_sold:
          # print("SOLD") 
          TickerWrapper.map_tickers[symbol] += abs(float(arr_row_items[IDX_AMOUNT]))
          TickerWrapper.map_transactions[symbol].append(("SOLD {0} {1}".format(symbol, description), float(str_amount), f_reg_fee, str_date))

        # print(arr_headings)
        # print(arr_row_items)
        # pp.pprint TickerWrapper.map_transactions[symbol])
        # if len(arr_headings) == len(arr_row_items):
        #   for i in range(len(arr_headings)):
        #     print(i, arr_headings[i], arr_row_items[i])
    
    if TickerWrapper.is_verbose:
      pp.pprint(arr_funds)
    
    # print TickerWrapper.map_tickers)
    if TickerWrapper.is_verbose:
      
      print(TickerWrapper.map_tickers)
      TickerWrapper.map_tickers = {k: v for k, v in sorted(TickerWrapper.map_tickers.items(), key=lambda item: item[1])}

      # print TickerWrapper.map_tickers)
      # pp.pprint TickerWrapper.map_tickers)
      # pp.pprint TickerWrapper.map_transactions)
      # TickerWrapper.map_tickers = {k: v for k, v in sorted TickerWrapper.map_tickers.items(), key=lambda item: item[1])}
      # print("x: ", x)
    total = 0

    for ticker in TickerWrapper.map_tickers:
      
      print("{0:15} {1:>10.2f}".format(ticker, TickerWrapper.map_tickers[ticker]))
      # print("{0:15} {1:10.2f}".format("fees", TickerWrapper.map_transaction_fees[ticker]))  
      # print("{0:>20} {1:10.2f}".format("", TickerWrapper.map_tickers[ticker] - TickerWrapper.map_transaction_fees[ticker]))  

      total += TickerWrapper.map_tickers[ticker]
      
      # print("\t\t", end="")
      # pp.pprint TickerWrapper.map_transactions[ticker], indent=8)
      if TickerWrapper.is_show_transactions:
        TickerWrapper.display_transactions(ticker)
        # print("tx:", tx)
        # pp.pprint TickerWrapper.map_transactions[ticker])

    arr_fee_totals = [abs(x[1])  for x in TickerWrapper.map_transaction_fees.items()]
    # print(arr_fee_totals)
    print("{0:15} {1:>10.2f}".format("total fees = ", sum(arr_fee_totals)))  
    print("------------")
    print("{0:15} {1:>10.2f}".format("total = ", total))
    
    if parsed_args.list:  
      
      # arr_transactions = [x for x in TickerWrapper.map_transactions.values()]
      # # for x in TickerWrapper.map_transactions.values():
      #   # print(* x)
      # print(arr_transactions)
      # for x in arr_transactions:
      #   print(x)
      # arr_fund_amounts = [float(x[1]) for x in arr_funds]
      arr_fund_amounts = [float(x[1]) for x in arr_funds]
      # print("arr_fund_amounts: ", arr_fund_amounts)
      sum_funds = sum(arr_fund_amounts)
      net_transactions = sum_funds
      arr_transactions = []
      
      for k, v in TickerWrapper.map_transactions.items():
        # print(k, " --- ", v)
        arr_transactions.extend(v)
        # arr_transactions.append(*v)
      # print(x)
      if TickerWrapper.is_verbose:
        print(arr_transactions)
        print(TickerWrapper.map_transactions)
        print("{0:>60}{1:>20}{2:>20}".format("FUNDING", "", sum_funds))
      sorted_arr_transactions = sorted(arr_transactions,key=lambda item: item[3])
      for x in sorted_arr_transactions:
        # print("ip length: ", len(x))
        # print(x)
        net_transactions += x[1]
        if TickerWrapper.is_verbose:
          print("{0:>60}{1:>20}{2:>20}".format(x[0], x[3], x[1]))
          print("{0:>120.2f}".format(net_transactions))
          print()



try:
  validate_input(arr_headings)
  data_matrix = []
  for x in f:
    # print(i, "=", x)
    i += 1
    
    
    row_items = x.split(",")
    n_row_items = len(row_items)
    # print(i, n_row_items, x.split())
    if n_row_items != n_arr_headings:
      # print(n_row_items, i, x)
      continue
    data_matrix.append(row_items)
    
      
  app = TickerWrapper()
  TickerWrapper.set_data(data_matrix)
  
  TickerWrapper.run()

# except NameError as ex:
  # print("Named exception", ex)
except Exception as ex:
  print("RAISED EXCEPTION")
  print(ex)
  raise
  # raise
  
