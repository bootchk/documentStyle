
from documentStyle.styleProperty.styleProperty import BaseStyleProperty

#from documentStyle.formation.resettableValue import ResettableIntValue  # , ResettableFloatValue, ResettableColorValue

'''
Subclasses specialize GUI, i.e. have unique layouts.
And some subclasses use wrapped style values.

BaseStyleProperty knows nothing about GUI.
These know they use QWidget GUI.
Alternatively, the GUI is QML.

TODO refactor using Pluggable Behavior??
'''

'''
These return pickleable values via wrapping or other adaption.
Reimplement propagateValueToInstrument() to wrap instruments type with a pickleable type
'''
  
class Wrappable(object):
  '''
  Mixin class for StyleProperty classes that wrap.
  '''
  def propagateValueToInstrument(self):
    ''' Apply unwrapped value to instrument. '''
    self.instrumentSetter(self.resettableValue.value.rawValue())
  
  
  
  
class FontStyleProperty(Wrappable, BaseStyleProperty):
  ''' Needed for both PySide and PyQt. '''
  pass
  
  
  
"""
class PSComboBoxStyleProperty(Wrappable, ComboBoxStyleProperty):
  ''' Needed for PySide, but not for PyQt. '''
  pass
"""
  
  