'''
Copyright 2013 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PyQt4.QtCore import Qt

class StyleWrapper(object):
  '''
  Wrap a StyleProperty that is Qt enum so that it is Pickleable.
  
  Only needed for PySide.  Qt enums are already pickleable in PyQt, but not in PySide.
  
  Also isolates Qt.
  
  Instances are true instances, unlike PySide Qt enum values, which are class attributes.
  (That's why they are not pickleable.)
  
  StyleProperty's that are not Qt enums (e.g. of type int) do not need wrapping.
  '''
  
  def __init__(self, raw):
    assert raw is not None
    # ??? How to make this work: raw value is not an instance, but an attribute of the wrappedEnum
    # assert isinstance(raw, self.wrappedEnum)
    self.raw = raw
  
  
  
  def __repr__(self):
    ''' '''
    # Don't know why this fails, it works below in reduce() ???
    # return self.raw.name
  
    return str(self.wrappedEnum) + "as int:" + str(int(self.raw))
  
    
    
  def rawValue(self):
    ''' Raw (unwrapped) Qt enum value. '''
    return self.raw
  
  
  " No setter currently required. "
  
  
  def __eq__(self, other):
    return self.raw == other.raw

  
  def __reduce__(self):
    '''
    Reduce state to key (enum name) string, not the value (an unpickleable Qt enum.)
    '''
    #print "reduce called"
    # Result is (factory class, args to factory, and state dictionary)
    return (self.__class__, (), {'name': self.raw.name})

  
  def __setstate__(self, state):
    
    keys = state.keys()
    assert len(keys) == 1
    for key in keys:
      #print "key:", key, "value:", state[key]
      result = self.__class__.wrappedEnum.values[state[key]]
      #print "result:", result
      self.raw = result
    assert isinstance(self.raw, self.__class__.wrappedEnum)
      
      
      
'''
Each subclass has-a wrapped class
Wrapped instrument class knows dictionary of the wrapped domain.
Used by __setstate__().

Note here "PenStyle" means "PenPattern", a particular StyleProperty.
'''

class PenStyleWrapper(StyleWrapper):
  wrappedEnum = Qt.PenStyle
  
  
class BrushStyleWrapper(StyleWrapper):
  wrappedEnum = Qt.BrushStyle
  
  
class AlignmentStyleWrapper(StyleWrapper):
  wrappedEnum = Qt.AlignmentFlag
  
  
  
