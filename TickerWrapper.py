from Context import Context, ContextType

class ContextError(Exception):
  pass

class TickerWrapper:
  _instance = None
  context = None
  def __new__(self, initial_state):
    if self._instance is None:
      # raise Exception("Duplicate singletons!")
      _instance=self
      self._instance = super(TickerWrapper, self).__new__(self)
      self._instance.set_context(initial_state)

    return self._instance

  def read_file(self, filename):
    try:
      open(filename)
    except FileNotFoundError as ex:
      print("no such file found!")
  
  def set_context(self, state):
    # context = Context(state)
    print("interpreted context: ", state)
    self.context = state
    
  def get_context(self):
    if self.context == None:
      raise ContextError("No context defined")
    return self.context

  def get_context_val(self, context_type : ContextType):
    # print("context attr: ", self.context.context)
    print("attr: ", context_type)
    return self.context.context[context_type.value]




def test():
  print("is testing")

if __name__ == '__main__':
  test()
