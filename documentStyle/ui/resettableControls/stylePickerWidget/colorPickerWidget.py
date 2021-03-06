'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtGui import QColor

from .stylePickerWidget import StylePicker


class ColorPicker(StylePicker):
  '''
  Specializes StylePicker for <style>: QColor
  '''
  
  # !!! emitted by base class StylePicker
  valueChanged = Signal(QColor)
  
  
  def __init__(self, resettableValue):
    # text a blank char obviates problems with text disappearing in background
    super(ColorPicker, self).__init__(text=" ", 
                                      styleType=QColor, 
                                      subDialog = self._baseDialog,
                                      resettableValue = resettableValue)
  

  def _baseDialog(self, parent, initialValue):
    '''
    Adapter: !!! framework dialog returns a single value, which is not isValid() when user canceled.
    Adapt to return a tuple telling whether user canceled.
    
    parent not used; PyQt owns
    '''
    # Use the overloaded PyQt signature that takes initialValue.  Parent determines where dialog is centered (typically in StyleDialog.)
    result = QColorDialog.getColor(initial=initialValue, parent=parent)
    assert isinstance(result, QColor), str(type(result))
    
    # Adapt return a tuple
    ok = result.isValid()
    assert ok is True or ok is False
    return ok, result
    
    
  def setValue(self, newValue):
    '''
    Set widget <style>: color
    AND set widget local attribute
    '''
    #print "ColorPicker setValue()", newValue.name()
    assert isinstance(newValue, QColor)
    # !!! This is QStyleSheet, for widgets, not our StyleSheet
    self.setStyleSheet( '* { background-color: '+ newValue.name() + ' }')
    self.ensurePolished() # ??? necessary?  Does it recompute style?
    # self.update() # ??? necessary?  Does it recompute style?
    self._value = newValue
    self.valueChanged.emit(newValue)  # Propagate, e.g. to model


    