'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

#from PyQt5.QtCore import QObject

from documentStyle.selector import fieldSelector
from documentStyle.formation.resettableValue import ResettableIntValue
from documentStyle.debugDecorator import report, reportReturn

import documentStyle.config as config


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
    
    # My selector describes parents and field of self e.g. Foo,Line,Pen,Color
    self.selector = fieldSelector(parentSelector, name)
    
    " GUI attributes, e.g. for spin box and combo box"
    self.minimum = minimum
    self.maximum = maximum
    self.singleStep = singleStep
    self.model = model  # enum dictionary maps GUI strings to values
    
    # TODO: simplify by asking model for default (requires model not optional.)
    " This is model.  Init with default from instrument. "
    self.resettableValue = ResettableIntValue(default)
    assert self.resettableValue.value is not None, "Default is required."
    
    
    
    
  def __repr__(self):
    return self.name + ":" + str(self.selector) + ":" + str(self.resettableValue)
  
  
  '''
  Gui related methods.
  
  exposeToQML() is analagous to getLayout().
  Neither is necessary unless self is part of an editedFormation
  '''
  
  def exposeToQML(self, view, styleSheetTitle):
    '''
    Expose self's model (resettableValue) to QQuickView of QML.
    
    TODO only if parent formation is editable.
    '''
    assert view is not None # created earlier
    view.rootContext().setContextProperty(self._QMLName(styleSheetTitle), self.resettableValue)

  
  def _QMLName(self, styleSheetTitle):
    '''
    String for id of self's model in QML.
    Qualified by stylesheet title.
    E.G. UserAnyPenColor or DocLinePenColor
    '''
    result = styleSheetTitle + str(self.selector)
    print("setContextProperty", result)
    return result
  
  
  def getLayout(self, isLabeled=False):
    ''' Layout widget that displays this StyleProperty'''
    raise NotImplementedError # deferred
  
  
  @report
  def setPropertyValue(self, newValue):
    '''
    Every set() may change state of resettableValue.
    This may be called programmatically, from StylingActs.
    '''
    #print("StyleProperty.set()", newValue)
    self._throughSet(newValue) # Model
      
    # self.stylePropertyValueChanged.emit()
    
  
  def get(self):
    " get from self (master), not from instrument. "
    return self.resettableValue.value
  
  
  def _throughSet(self, value):
    ''' Set cached value and propagate to instrument. '''
    # OLD self.resettableValue.setValue(value)
    self.resettableValue.value = value
    # TODO propagate now, OR flush values at end (dumb dialog)
    self.propagateValueToInstrument()
  
  
  @reportReturn
  def propagateValueToInstrument(self):
    '''
    Propagate my value thru facade to framework instrument.
    
    Default implementation.  Some subclasses reimplement to wrap values.
    '''
    value = self.resettableValue.value
    self.instrumentSetter(value)
    # for debugging, return value
    return value
    
    
    
  '''
  Did user touch by changing the value or by resetting the value?
  This does NOT assert that final value is different from initial value before editing,
  since user may have changed it many times, ending in the same value as initial.
  
  Note this is called from StylePropertyLayout.onValueChanged()
  '''
  """
  OLD: touched was attribute of StyleProperty
  def touch(self):
    self.touched = True
    
  def isTouched(self):
    return self.touched
  """
  '''
  Delegate to resettableValue.
  QWidget calls this touch()
  QML does resettableValue = True
  '''
  def touch(self):
    self.resettableValue.touch()
    
  def isTouched(self):
    return self.resettableValue.touched
  
  
  def isReset(self):
    return self.resettableValue.isReset

  def roll(self):
    self.resettableValue.roll()


