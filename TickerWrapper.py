from Context import Context, ContextType

class ContextError(Exception):
  pass

class TickerWrapper:
  _instance = None
  context = None
  file_input = None
  def __new__(self, initial_state):
    if self._instance is None:
      # raise Exception("Duplicate singletons!")
      _instance=self
      self._instance = super(TickerWrapper, self).__new__(self)
      self._instance.set_context(initial_state)

    return self._instance

  def run(self):
    if self._instance.get_context_val(ContextType.INTERACTIVE):
      pass
    else:
      self.next()
    
  def next(self):

    self.read_file(self._instance.get_context_val(ContextType.FILE_NAME))

  def read_file(self, filename):
    try:
      file_input = open(filename)
      print("file: ", file_input)
    except FileNotFoundError as ex:
      print("no such file found!")
      raise
  
  def set_context(self, state):
    # context = Context(state)
    print("interpreted context: ", state)
    self.context = state
    
  def get_context(self):
    print(self.context == None)
    if self.context == None:
      raise ContextError("No context defined")
    return self.context

  def get_context_val(self, context_type : ContextType):
    # print("context attr: ", self.context.context)
    print("attr: ", context_type)
    return self.context.context[context_type.value]


class TickerWrapperTest: 
  tw = None
  def __init__(self):
    TickerWrapper.tw = TickerWrapper(None)
    print("tw const: ", TickerWrapper.tw)

  def test_no_context(self):
    print("testing no context")
    TickerWrapper.tw.set_context(None)
    try:
      TickerWrapper.tw.get_context()
    except ContextError as ex:
      print(ex)
      print("Caught successfully!")

  

if __name__ == '__main__':
  print("Testing ----", __file__)
  test = TickerWrapperTest()
  test.test_no_context()