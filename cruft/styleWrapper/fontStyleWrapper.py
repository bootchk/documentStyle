'''
'''
from PyQt5.QtGui import QFont


class FontStyleWrapper(object):
  '''
  Wrap a QFont so it is Pickleable as string rep.
  
  Needed for both PySide and PyQt (neither pickles QFont.)
  
  A QFont is composite of many values (fontfamily, fontstyle, fontsize)
  (Most other StyleProperty values are simple types such as int or Qt enum.)
  '''
  
  def __init__(self, wrapped=None):
    self.wrapped = wrapped
  
    
  def rawValue(self):
    ''' Get wrapped value, of type QFont. '''
    return self.wrapped
  
  
  def __repr__(self):
    " QFont.toString() is readable "
    return self.wrapped.toString()
  
  " No setter currently required. "
  
  
  def __eq__(self, other):
    return self.wrapped == other.wrapped
  
  
  def __reduce__(self):
    '''
    Reduce to string (pickleable), not QFont value (unpickleable.)
    '''
    #print "FontStyleWrapper.reduce called"
    # Arbitrary name for key.
    return (self.__class__, (), {'fontDescriptionString': self.wrapped.toString()})

  
  def __setstate__(self, state):
    '''
    Create state (attribute: wrapped, of type: QFont.)
    On the local machine, this executes the font finding algorithm of framework,
    to create a font object that best matches the string description of the font.
    '''
    # Should be only one key: fontDescriptionString
    for key in state.keys():
      #print "key:", key, "value:", state[key]
      fontString = state[key]
      self.wrapped = QFont()  # default font
      self.wrapped.fromString(fontString) # change to best matching font (returns a boolean status!)
      #print "FontStyleWrapper.__setstate__ result:", self.wrapped
    assert isinstance(self.wrapped, QFont), "Invariant: wrapped state is a QFont"
      

  
  
  
  