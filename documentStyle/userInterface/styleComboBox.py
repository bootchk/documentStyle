'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PySide.QtCore import Signal, Slot, Qt
from PySide.QtGui import QComboBox

from resettable import Resettable


class StyleComboBox(Resettable, QComboBox):
  '''
  Control widget:
  - GUI behaviour of QComboBox
  - adapts QComboBox to have value(), setValue(), valueChanged() API
  - takes a model that is an enum of Style
  - resettable
  
  QComboBox is too broad for our use: includes editing of text
  AND QComboBox is too narrow for our use: doesn't implement setValue().
  '''
  
  valueChanged = Signal()
  

  def __init__(self, model, resettableValue ):
  
    QComboBox.__init__(self)
    self.model = model
    self.addItems(model.values.keys())
    
    Resettable.__init__(self, resettableValue)  # MUST follow QComboBox init and create model
    
    # connect adapted widget signal to adapter
    # !!! connecting to str type signal
    self.currentIndexChanged[str].connect(self.adaptValueChanged)
    
    self.alignItems()
  

  '''
  Adaption augments inherited Widget with these methods.
  
  Inherited Widget uses int index.
  These are agnostic of type.
  '''
  def setValue(self, newValue):
    # print "styleComboBoxWidget setValue", newValue
    self.setCurrentIndex( self._indexOfValue(newValue) )
  
  
  def value(self):
    return self._adaptNewValue(self.currentText())
  
  
  
    
  '''
  Adapt signal.
  '''
  @Slot(str)
  def adaptValueChanged(self, newValue):
    '''
    Receive signal currentIndexChanged[str], adapt to signal valueChanged.
    
    Dumb down: discard any passed newValue.
    '''
    #print "Combo box value changed", newValue
    self.valueChanged.emit() # adaptedValue)
    
  
  '''
  Convert to and from Widget text values to model values.
  '''
  
  def _adaptNewValue(self, newValue):
    '''
    Adapt Widget's string value to model value, i.e. enum value.
    '''
    # assert value is unicode. Use str() to decode
    convertedValue = self.model.values[str(newValue)] # 
    #print "Adapted ", newValue, "converted type", type(convertedValue)
    return convertedValue
  
    
  
  def _indexOfValue(self, searchValue):
    # searchValue is an enum value or None, and None can be a value in dictionary
    i = 0
    foundKey = False
    for _, value in self.model.values.items():
      #print searchValue, value
      # if searchValue is None and None is in dictionary, or searchValue == value
      if value is searchValue or value == searchValue:  # !!! is, not ==, to match None
        foundKey = True
        break
      i += 1
    assert foundKey, "Missing value: " + str(searchValue) + " in model" + str(self.model) # dict is complete on values
    return i


  def alignItems(self):
    " See web. "
    self.setEditable(True)
    self.lineEdit().setReadOnly(True)
    self.lineEdit().setAlignment(Qt.AlignRight)
    for i in range(0, self.count()):
      self.setItemData(i, Qt.AlignRight, Qt.TextAlignmentRole)
    
    
