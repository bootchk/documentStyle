
from PyQt5.QtGui import QFont

from documentStyle.styleProperty.styleProperty import BaseStyleProperty


'''
Subclasses specialize to wrap unpickleable ResettableValue values.

These return pickleable values via wrapping or other adaption.
This is the API to StylingAct, which requires pickleable values.
'''
  
class FontStyleProperty(BaseStyleProperty):
  '''
  Reimplement getPropertyValue, setPropertyValue to unwrap before setting, wrap after getting
  
  Property values internal are not pickleable.
  They are the native type of the instrument e.g. QFont, which is the one that is not pickleable.
  '''
  
  
  def setPropertyValue(self, newValue):
    '''
    Reimplement
    '''
    # newValue is not pickleable
    assert isinstance(newValue, str)
    unwrappedValue = QFont()
    success = unwrappedValue.fromString(newValue)
    if not success:
      raise RuntimeError("Failed to unwrap font string.")
    # assert QFont is still valid, just not the desired one.
    super().setPropertyValue(unwrappedValue)
    
  
  def getPropertyValue(self):
    unwrappedValue = super().getPropertyValue()
    " QFont.toString() is pickleable "
    result = unwrappedValue.toString()
    # assert result is pickleable
    return result
  
  
  
  
"""
class PSComboBoxStyleProperty(Wrappable, ComboBoxStyleProperty):
  ''' Needed for PySide, but not for PyQt. '''
  pass
"""
  
  