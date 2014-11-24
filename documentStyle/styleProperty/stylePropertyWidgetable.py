
from documentStyle.styleProperty.styleProperty import BaseStyleProperty

from documentStyle.userInterface.layout.stylePropertyLayout import FloatStylePropertyLayout, IntStylePropertyLayout
from documentStyle.userInterface.layout.stylePropertyLayout import ColorStylePropertyLayout, FontStylePropertyLayout
from documentStyle.userInterface.layout.stylePropertyLayout import ComboBoxStylePropertyLayout

#from documentStyle.formation.resettableValue import ResettableIntValue  # , ResettableFloatValue, ResettableColorValue

'''
Subclasses specialize GUI, i.e. have unique layouts.
And some subclasses use wrapped style values.

BaseStyleProperty knows nothing about GUI.
These know they use QWidget GUI.
Alternatively, the GUI is QML.

TODO refactor using Pluggable Behavior??
'''

class FloatStyleProperty(BaseStyleProperty):
    
  def getLayout(self, isLabeled=False):
    return FloatStylePropertyLayout(parentStyleProperty=self, isLabeled=isLabeled)


#TODO default not needed by base class
class IntStyleProperty(BaseStyleProperty):
   
  def getLayout(self, isLabeled=False):
    return IntStylePropertyLayout(parentStyleProperty=self, isLabeled=isLabeled)
  

class ColorStyleProperty(BaseStyleProperty):
    
  def getLayout(self, isLabeled=False):
    return ColorStylePropertyLayout(parentStyleProperty=self, isLabeled=isLabeled)
  
  
class UnwrappedComboBoxStyleProperty(BaseStyleProperty):
  " Combobox for style objects that don't need wrapping (pickle.) "
    
  def getLayout(self, isLabeled=False):
    return ComboBoxStylePropertyLayout(parentStyleProperty=self, isLabeled=isLabeled)
  
  
class ComboBoxStyleProperty(BaseStyleProperty):
    
  def getLayout(self, isLabeled=False):
    return ComboBoxStylePropertyLayout(parentStyleProperty=self, isLabeled=isLabeled)
  

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
  
  def getLayout(self, isLabeled=False):
    return FontStylePropertyLayout(parentStyleProperty=self, isLabeled=isLabeled)
  
  
class PSComboBoxStyleProperty(Wrappable, ComboBoxStyleProperty):
  ''' Needed for PySide, but not for PyQt. '''
  pass

  
  