import pandas as pd

import argparse 

from TickerWrapper import TickerWrapper
from Context import Context, ContextType

parser = argparse.ArgumentParser(description='Gather Transaction Data')
parser.add_argument("-f", "--file_name", nargs=1, type=str, default="")
parser.add_argument("-t", "--transactions", action="store_true")
parser.add_argument("-l", "--list_tickers", action="store_true")
parser.add_argument("-i", "--interactive", action="store_true")

parsed_args = parser.parse_args()

context = Context(parsed_args)

tickerWrapper = TickerWrapper(context)
tickerWrapper.run()
