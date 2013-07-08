'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

#from PySide.QtCore import QObject

from documentStyle.selector import fieldSelector
from documentStyle.userInterface.layout.stylePropertyLayout import FloatStylePropertyLayout, IntStylePropertyLayout
from documentStyle.userInterface.layout.stylePropertyLayout import ColorStylePropertyLayout, FontStylePropertyLayout
from documentStyle.userInterface.layout.stylePropertyLayout import ComboBoxStylePropertyLayout
from documentStyle.formation.resettableValue import ResettableValue

#from documentStyle.debugDecorator import report

# Inherit QObject if signals
# Signals are not needed unless we want live dialogs showing WYSIWYG style changes to document before OK button is pressed.
class BaseStyleProperty(object): 
  '''
  StyleProperty: leaves of a Formation tree.
  A Property: (name, value) pair.
  The thing that a StylingAct changes.
  
  A property that:
  - facades a framework styling value 
  - knows a widget(layout) that displays it for editing
  
  Facades a framework styling value (e.g. QPen.width ).
  Knows setter methods for instrument (in framework) of the value (e.g. QPen.width() and QPen.setWidth())
  We don't need getter of instrument: this is master with one-way data flow set() to instrument.
  
  Abstract: partially deferred.
  
  Responsibilities:
  - conventional Property responsibilities: get and set
  - knows selector
  - knows resetness and how to roll: delegated to ResettableValue
  
  !!! Independent of framework, unless Qt signals used.
  '''

  # stylePropertyValueChanged = Signal()
  
  def __init__(self, name, instrumentSetter, parentSelector, default, minimum=0, maximum=0, singleStep=0.1, model=None ):
    '''
    '''
    self.name = name
    self.instrumentSetter = instrumentSetter
    # TODO: simplify by asking model for default (requires model not optional.)
    self.resettableValue = ResettableValue(default) # Initialize local cache with default from instrument
    assert self.resettableValue.value() is not None, "Default is required."
    # My selector describes parents and field of self e.g. Foo,Line,Pen,Color
    self.selector = fieldSelector(parentSelector, name)
    
    " GUI attributes, e.g. for spin box and combo box"
    self.minimum = minimum
    self.maximum = maximum
    self.singleStep = singleStep
    self.model = model  # enum dictionary maps GUI strings to values
    
    
    
  def __repr__(self):
    return self.name + ":" + str(self.selector) + ":" + str(self.resettableValue)
  
  
  def layout(self):
    ''' Layout widget that displays this StyleProperty'''
    raise NotImplementedError # deferred
  
  
  #@report
  def set(self, newValue):
    '''
    Every set() may change state of resettableValue.
    This may be called programmatically, from StylingActs.
    '''
    #print "StyleProperty.set()", newValue
    self._throughSet(newValue) # Model
      
    # self.stylePropertyValueChanged.emit()
    
  
  def get(self):
    " get from self (master), not from instrument. "
    return self.resettableValue.value()
  
  
  def _throughSet(self, value):
    ''' Set cached value and propagate to instrument. '''
    self.resettableValue.setValue(value)
    # TODO propagate now, OR flush values at end (dumb dialog)
    self.propagateValueToInstrument()
  
  
  def propagateValueToInstrument(self):
    '''
    Propagate my value thru facade to framework instrument.
    
    Default implementation.  Some subclasses reimplement to wrap values.
    '''
    self.instrumentSetter(self.resettableValue.value())

  
  
  def isReset(self):
    return self.resettableValue.isReset()
  
  def wasReset(self):
    return self.resettableValue.wasReset()

  def roll(self):
    self.resettableValue.roll()



'''
Subclasses specialize GUI, i.e. have unique layouts.
And some subclasses use wrapped style values.

TODO refactor using Pluggable Behavior??
'''

'''
These return pickleable values, without wrapping or adaption.
'''
class FloatStyleProperty(BaseStyleProperty):
  def layout(self):
    return FloatStylePropertyLayout(parentStyleProperty=self)
  
  
class IntStyleProperty(BaseStyleProperty):
  def layout(self):
    return IntStylePropertyLayout(parentStyleProperty=self)


class ColorStyleProperty(BaseStyleProperty):
  def layout(self):
    return ColorStylePropertyLayout(parentStyleProperty=self)


class UnwrappedComboBoxStyleProperty(BaseStyleProperty):
  " Combobox for style objects that don't need wrapping (pickle.) "
  def layout(self):
    return ComboBoxStylePropertyLayout(parentStyleProperty=self)


'''
These return pickleable values via wrapping or other adaption.
Reimplement propagateValueToInstrument() to wrap instruments type with a pickleable type
'''
  
class ComboBoxStyleProperty(BaseStyleProperty):
  def layout(self):
    return ComboBoxStylePropertyLayout(parentStyleProperty=self)
    
  def propagateValueToInstrument(self):
    self.instrumentSetter(self.resettableValue.value().getWrappedValue())


class FontStyleProperty(BaseStyleProperty):
  def layout(self):
    return FontStylePropertyLayout(parentStyleProperty=self)
  
  def propagateValueToInstrument(self):
    self.instrumentSetter(self.resettableValue.value().getWrappedValue()) 
  
  