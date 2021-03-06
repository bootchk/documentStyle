'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox

from .resettable import Resettable


class StyleComboBox(Resettable, QComboBox):
  '''
  Control widget:
  - GUI behaviour of QComboBox
  - adapts QComboBox to have value(), setValue(), valueChanged() API
  - takes a domainModel that is an enum of Style
  - resettable
  
  QComboBox is too broad for our use: includes editing of text
  AND QComboBox is too narrow for our use: doesn't implement setValue().
  '''
  
  valueChanged = Signal()
  

  def __init__(self, domainModel, resettableValue ):
  
    QComboBox.__init__(self)
    assert domainModel is not None
    self.domainModel = domainModel
    self.addItems(list(domainModel.values.keys()))
    
    Resettable.__init__(self, resettableValue)  # MUST follow QComboBox init and create domainModel
    
    # connect adapted widget signal to adapter
    # !!! connecting to str type signal
    self.currentIndexChanged[str].connect(self.adaptValueChanged)
    
    self._alignSelf()
  

  '''
  Adaption augments inherited Widget with these methods.
  
  Inherited Widget uses int index.
  These are agnostic of type.
  '''
  def setValue(self, newValue):
    '''
    !!! Note the setValue API requires emit valueChanged.
    Implemented below (not here) because setCurrentIndex()
    emits a signal which below we re emit as valueChanged.
    '''
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
  Convert to and from Widget text values to domainModel values.
  '''
  
  def _adaptNewValue(self, newValue):
    '''
    Adapt Widget's string value to domainModel value, i.e. enum value.
    '''
    # assert value is unicode. Use str() to decode
    convertedValue = self.domainModel.values[str(newValue)] # 
    #print "Adapted ", newValue, "converted type", type(convertedValue)
    return convertedValue
  
    
  
  def _indexOfValue(self, searchValue):
    # searchValue is an enum value or None, and None can be a value in dictionary
    i = 0
    foundKey = False
    for _, value in self.domainModel.values.items():
      #print searchValue, value
      # if searchValue is None and None is in dictionary, or searchValue == value
      if value is searchValue or value == searchValue:  # !!! is, not ==, to match None
        foundKey = True
        break
      i += 1
    assert foundKey, "Missing value: " + str(searchValue) + " in domainModel" + str(self.domainModel) # dict is complete on values
    return i


  '''
  Widget alignment
  '''
  def _alignSelf(self):
    '''
    See web for much discussion.
     
    right alignment didn't seem to have desired effect on Linux May 2014.
    right alignment cut off right side of text under scroll bar on Win Vista May 2014 see QTBUG 33176
    
    Apple HIG guidelines don't seem to suggest an alignment.
    But since the widget is left aligned (in a form), might as well left align the items also?
    
    If aligning right, does this help:
    comboBox.view().setLayoutDirection(Qt.RightToLeft)
    '''
    # Align both widget, and items inside it in the same direction
    direction = Qt.AlignLeft
    self._alignTextEdit(direction=direction)
    ##self.view().setLayoutDirection(Qt.RightToLeft)
    self._alignItems(direction)
  
  def _alignItems(self, direction):
    for i in range(0, self.count()):
      #print("Aligning item")
      self.setItemData(i, direction, Qt.TextAlignmentRole)
    
  def _alignTextEdit(self, direction):
    '''
    lineEdit must be editable to set alignment, but then can be made readOnly
    '''
    self.setEditable(True)
    self.lineEdit().setReadOnly(True)
    self.lineEdit().setAlignment(direction)
    
    
  def alignItems(self):
    " See web. "
    self.setEditable(True)
    self.lineEdit().setReadOnly(True)
    self.lineEdit().setAlignment(Qt.AlignRight)
    for i in range(0, self.count()):
      self.setItemData(i, Qt.AlignRight, Qt.TextAlignmentRole)
    
    
