from enum import Enum

class ContextType(Enum):
  LIST_TRANSACTIONS = "transactions"
  LIST_TICKERS = "list_tickers"
  FILE_NAME = "file_name"
  INTERACTIVE = "interactive"


class Context:
  
  def __init__(self, parsed_args = None):
    if parsed_args:
      self.__init__from_parsed_args(parsed_args)

    else:
      pass

  def __init__from_parsed_args(self, parsed_args):
    self.context = {}
    i = 0
    context_keys = [a for a in dir(parsed_args) if not a.startswith('_')]
    for context_key in context_keys:
      print(i, context_key)
      
      i+=1
      self.context[context_key] = getattr(parsed_args, context_key)
      print(self.context)
    print("context: ", self.context)

  