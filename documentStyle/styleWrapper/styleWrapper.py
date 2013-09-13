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
  
  def __init__(self, wrapped=None):
    '''
    Wrapped object is optional: unpickling sets via setstate.
    '''
    self.wrapped = wrapped
  
    
  def getWrappedValue(self):
    ''' A Qt enum value. '''
    return self.wrapped
  
  
  " No setter currently required. "
  
  
  def __eq__(self, other):
    return self.wrapped == other.wrapped

  
  def __reduce__(self):
    '''
    Reduce state to key (enum name) string, not the value (an unpickleable Qt enum.)
    '''
    #print "reduce called"
    # Result is (factory class, args to factory, and state dictionary)
    return (self.__class__, (), {'name': self.wrapped.name})

  
  def __setstate__(self, state):
    
    # Should be only one key
    for key in state.keys():
      #print "key:", key, "value:", state[key]
      result = self.__class__.wrappedInstrument.values[state[key]]
      #print "result:", result
      self.wrapped = result
    assert isinstance(self.wrapped, self.__class__.wrappedInstrument)
      
      
      
'''
Each subclass has-a wrapped class
Wrapped instrument class knows dictionary of the wrapped domain.
Used by __setstate__().

Note here "PenStyle" means "PenPattern", a particular StyleProperty.
'''

class PenStyleWrapper(StyleWrapper):
  wrappedInstrument = Qt.PenStyle
  
  
class BrushStyleWrapper(StyleWrapper):
  wrappedInstrument = Qt.BrushStyle
  
  
class AlignmentStyleWrapper(StyleWrapper):
  wrappedInstrument = Qt.AlignmentFlag
  
  
  
