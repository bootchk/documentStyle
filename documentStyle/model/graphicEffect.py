'''
'''

class Model(object):
  '''
  Mimics a PyQt5 enum: has "values" attribute that is a dictionary
  
  There is no Qt enum for graphics effect.
  Thus values here are pickleable (not wrapped, like Qt enums.)
  But the GraphicsEffectInstrument adapts these values to QGraphicsEffect objects before applying.
  '''
  def __init__(self):
    self.values = {"None": 0,  # In Qt, does not exist NullGraphicsEffect
                   "Blur": 1,
                   "Shadow": 2 }   # Drop Shadow too long
    # TODO other effects
  
graphicEffectModel = Model()