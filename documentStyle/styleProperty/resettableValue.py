
from PyQt5.QtCore import pyqtProperty, QObject
from PyQt5.QtGui import QColor
from PyQt5.QtCore import pyqtSignal as Signal

#from documentStyle.debugDecorator import reportReturn, reportFalseReturn


class BaseResettableValue(QObject):
  ''')  # 
  A value whose current value can be reset to an valueToResetTo,
  and whose current value can be rolled into valueToResetTo.
  
  Responsibilities:
  - know valueToResetTo and current value
  - knows reset state
  
  This is a model part of MVC.
  A model that can be used by QML.
  
  This base class is agnostic of type of value.
  
  FUTURE:
  - know 'isInlined' i.e. is overridden
  This distinguishes values set by the program (for an existing in-line StylingAct)
  from values set by the user editing (in creating a new in-line StylingAct.)
  In other words, if the program sets a value for an in-line StylingAct, isReset becomes False,
  which is distinct from a user editing the value, where also isReset becomes False.
  An optimization for deleting existing StylingActs,
  but not absolutely necessary.
  '''
  
  isResetChanged = Signal()
  
  def __init__(self, valueToResetTo):
    super().__init__()  # MUST init QObject)  # 
    self._value = valueToResetTo
    self._valueToResetTo = valueToResetTo
    self._isReset = True
    self._touched = False
    
    
  def __str__(self):
    return "ResettableValue(original=" + str(self._valueToResetTo) + " value=" + str(self._value)

  '''
  value property is deferred to subclasses
  '''
  
  '''
  isReset property
  '''
  
  @pyqtProperty(bool, notify=isResetChanged)
  def isReset(self):
    ''' A getter for convenience of debugging. '''
    return self._isReset

  ''' 
  formerly reset()
  '''
  @isReset.setter
  def isReset(self, newResetness):
    ''' 
    Restore current value to valueToResetTo. 
    At behest of user.
    '''
    assert newResetness == True # Semantics is: can reset, cannot set isReset to False
    if self._isReset:
      #print "Resetting twice?"
      pass
    '''
    Don't set private _value, use setter so signal is emitted.
    '''
    self.value = self._valueToResetTo
    self._isReset = True
    self.isResetChanged.emit()


  '''
  touched property
  
  User chose a value, or chose reset button.
  We don't know which here, so we can't set isReset:
  User chose a value, isReset should be False.
  User chose reset button, isReset should be True.
  '''
  @pyqtProperty(bool)
  def touched(self):
    return self._touched

  @touched.setter
  def touched(self, newTouchedness):
    assert newTouchedness == True # Semantics is: can reset, cannot set isReset to False
    self._touched = newTouchedness


  def roll(self):
    '''
    Current value becomes new valueToResetTo. 
    AND _wasReset becomes False.
    '''
    self.__init__(valueToResetTo = self._value)
    


'''
Subclasses specialized by type.
Don't know a way to get around this:
pyqtProperty needs to know the type
'''


class ResettableIntValue(BaseResettableValue):
  
  valueChanged = Signal()
  # TODO does this clash with pre-defined QML signal valueChanged?
  
  def __init__(self, valueToResetTo):
    super().__init__(valueToResetTo)
  
  '''
  Define getter of 'value' property.  
  The C++ type of the property is int
  '''
  @pyqtProperty(int, notify=valueChanged)
  def value(self):
    #print("get value", self._value)
    return self._value
  
  '''
  Define setter of 'value' property.
  Formerly setValue()
  '''
  @value.setter
  def value(self, newValue):
    '''
    Setting value always changes state to not isReset, even if value equals valueToResetTo.
    IOW, setValue 'touches' and isReset() means 'not touched.'
    If the GUI calls setValue() to what it thinks is valueToResetTo,
    it should also call reset() to set the state.
    '''
    #print("set value")
    self._value = newValue
    '''
    !!! Only the view knows whether this value change constitutes a touch.
    Programmatic value changes are not a touch.
    self.touched = True
    '''
    '''
    !!! Use the setter so signal emitted.
    '''
    self.isReset = False
    self.valueChanged.emit()


class ResettableColorValue(BaseResettableValue):
  
  valueChanged = Signal()
  
  def __init__(self, valueToResetTo):
    super().__init__(valueToResetTo)
  
  @pyqtProperty("QColor", notify=valueChanged)
  #@pyqtProperty(int, notify=valueChanged)
  def value(self):
    return self._value
  
  @value.setter
  def value(self, newValue):
    assert isinstance(newValue, QColor)
    self._value = newValue
    self._isReset = False
    self.valueChanged.emit()
    
    