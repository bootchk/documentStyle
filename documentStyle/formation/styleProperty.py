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

class BaseStyleProperty(object): # QObject if signals
  '''
  StyleProperty: leaves of a Formation tree.
  A Property: (name, value) pair.
  The thing that a StylingAct changes.
  
  A property that:
  - facades a framework styling value 
  - knows a widget(layout) that displays it for editing
  
  Facades a framework styling value (e.g. QPen.width ).
  Knows getter and setter methods for holder (in framework) of the value (e.g. QPen.width() and QPen.setWidth())
  
  Abstract: partially deferred.
  
  Responsibilities:
  - conventional Property responsibilities: get and set
  - knows selector
  - knows resetness and how to roll: delegated to ResettableValue
  - 
  '''

  # stylePropertyValueChanged = Signal()
  
  def __init__(self, name, setter, getter, parentSelector, minimum=0, maximum=0, singleStep=0.1, model=None ):
    '''
    '''
    self.name = name
    self.setter = setter
    self.getter = getter
    self.resettableValue = ResettableValue(getter()) # local cache, get from base
    assert self.resettableValue.value() is not None
    self.minimum = minimum
    self.maximum = maximum
    self.singleStep = singleStep
    self.model = model  # enum dictionary maps GUI strings to values
    # My selector describes parents and field of self e.g. Foo,Line,Pen,Color
    self.selector = fieldSelector(parentSelector, name)
    
    
  def __repr__(self):
    # return self.name + "setter " + str(self.setter) + "getter " + str(self.getter)
    return self.name + ":" + str(self.selector) + ":" + str(self.resettableValue)
  
  
  def layout(self):
    ''' Layout widget that displays this StyleProperty'''
    raise NotImplementedError # deferred
  
  
  #@report
  def set(self, newValue):
    '''
    Set value. TODO rename??
    
    Every set() may change state of resettableValue.
    This may be called programmatically, from StylingActs.
    '''
    #print "StyleProperty.set()", newValue
    self._throughSet(newValue) # Model
      
    # self.stylePropertyValueChanged.emit()
    
  
  def get(self):
    return self.resettableValue.value()
    # return self.getter()
  
  
  def _throughSet(self, value):
    ''' Set cached value and propagate to base. '''
    self.resettableValue.setValue(value)
    # TODO propagate now, OR flush values at end (dumb dialog)
    self.propagateValueToInstrument()
  
  
  def propagateValueToInstrument(self):
    '''
    Propagate my value thru facade to framework holder.
    '''
    self.setter(self.resettableValue.value())
  
  
  def isReset(self):
    return self.resettableValue.isReset()
  
  def wasReset(self):
    return self.resettableValue.wasReset()

  def roll(self):
    self.resettableValue.roll()



# TODO refactor using Pluggable Behavior??
  
class FloatStyleProperty(BaseStyleProperty):
  
  def layout(self):
    return FloatStylePropertyLayout(parentStyleProperty=self)
  
  
class IntStyleProperty(BaseStyleProperty):
  
  def layout(self):
    return IntStylePropertyLayout(parentStyleProperty=self)
  
  
class ComboBoxStyleProperty(BaseStyleProperty):
  
  def layout(self):
    return ComboBoxStylePropertyLayout(parentStyleProperty=self)
    
  
class ColorStyleProperty(BaseStyleProperty):
  
  def layout(self):
    return ColorStylePropertyLayout(parentStyleProperty=self)


class FontStyleProperty(BaseStyleProperty):
  
  def layout(self):
    return FontStylePropertyLayout(parentStyleProperty=self)