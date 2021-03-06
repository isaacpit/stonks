import pandas as pd

import argparse 

from TickerWrapper import TickerWrapper
from Context import Context, ContextType

parser = argparse.ArgumentParser(description='Gather Transaction Data')
parser.add_argument("-f", "--file_name", nargs=1, type=str, default="all_transactions.csv")
parser.add_argument("-t", "--transactions", action="store_true")
parser.add_argument("-l", "--list_tickers", action="store_true")

parsed_args = parser.parse_args()
print(parsed_args)

context = Context(parsed_args)

tickerWrapper = TickerWrapper(context)

the_context = tickerWrapper.get_context()
print(the_context)

is_list_transaction = tickerWrapper.get_context_val(ContextType.LIST_TRANSACTIONS)
file_name = tickerWrapper.get_context_val(ContextType.FILE_NAME)
is_list_tickers = tickerWrapper.get_context_val(ContextType.LIST_TICKERS)
print("list_trans?: ", is_list_transaction)
print("f?: ", file_name)
print("tickers?: ", is_list_tickers)