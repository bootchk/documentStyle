'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PySide.QtCore import Signal
from PySide.QtGui import QFontDialog, QFont

from stylePickerWidget import StylePicker


class FontPicker(StylePicker):
  '''
  Specializes StylePicker for <style>: QFont
  '''

  def __init__(self, resettableValue):
    super(FontPicker, self).__init__(text="Font", 
                                     styleType=QFont, 
                                     subDialogMethod = self._baseDialog,
                                     resettableValue = resettableValue)
  
  valueChanged = Signal(QFont)

  
  def _baseDialog(self, parent):
    '''
    Adapter: !!! the value returned by QFontDialog.getFont() is a tuple
    '''
    fontTuple = QFontDialog.getFont(parent)
    return fontTuple[0]
  
  
  def setValue(self, newValue):
    '''
    Set widget <style>: font
    AND set widget local attribute
    '''
    
    # fontValue = value[0]
    # assert isinstance(fontValue, QFont)
    assert isinstance(newValue, QFont)
    # A QFont is composite of font: family, size, weight
    self.setStyleSheet( '* { font-family: '+ newValue.family() + '; font-size: ' + str(newValue.pointSize()) + 'pt }')
    self._value = newValue
    self.valueChanged.emit(newValue)  # Propagate, e.g. to model
  