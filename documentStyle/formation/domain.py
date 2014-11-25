
# TODO units: a string to be suffixed to the GUI
class Domain():
  '''
  Domain of a StyleProperty.
  Simple struct.
  '''
  def __init__(self, minimum, maximum, step, model):
    self.minimum = minimum
    self.maximum = maximum
    self.singleStep = step
    self.model = model
