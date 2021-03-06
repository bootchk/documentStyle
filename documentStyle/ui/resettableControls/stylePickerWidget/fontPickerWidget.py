'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtWidgets import QFontDialog
from PyQt5.QtGui import QFont

from .stylePickerWidget import StylePicker



class FontPicker(StylePicker):
  '''
  Specializes StylePicker for <style>: QFont
  '''
  valueChanged = Signal(QFont)
  
  
  def __init__(self, resettableValue):
    super(FontPicker, self).__init__(text='Font',   # i18ns translation by super
                                     styleType=QFont, 
                                     subDialog = self._baseDialog,
                                     resettableValue = resettableValue)

  
  def _baseDialog(self, parent, initialValue):
    '''
    Adapter: !!! the value returned by QFontDialog.getFont() is a tuple.
    Adapt (flip) to tuple required by Super
    '''
    # Use overloaded PyQt signature whose first parameter is initial, not a keyword.
    assert isinstance( initialValue, QFont)
    result, ok = QFontDialog.getFont(initialValue, parent=parent)
    assert isinstance(ok, bool), str(type(ok))
    assert result is None or isinstance(result, QFont), str(type(result))
    '''
    Qt docs say: ok==False implies canceled and result is Qt's default font
    But doesn't work??? assert isinstance(result, QFont)
    '''
    return ok, result
  
  
  """
  Not relevant: whether exactMatch or not, sometimes italic-light does not display?
  if not newValue.exactMatch():
    #print 'Not an exact match'
  """
  
  
    
    
  def setValue(self, newValue):
    '''
    Set widget <style>: font
    AND set widget local attribute.
    
    !!! Takes a value of type native to instrument i.e. QFont which is not pickleable.
    '''
    assert isinstance(newValue, QFont)
    
    self._feedbackFont(newValue)
    self._value = newValue
    self.valueChanged.emit(newValue)  # Propagate, e.g. to model
  
  
  
  
  def _feedbackFont(self, font):
    '''
    Set widget font style to same as user chosen value, as GUI feedback.
    
    For widget, font is composite of font: family, size, weight???
  
    ??? TODO styleName works on Windows?
    
    TODO why does italic-light not work
    TODO strikeout, underline, etc.
    '''
    self.setStyleSheet( '* { font-family: '+ font.family() \
                        + '; font-size: '+ str(font.pointSize()) + 'pt ' \
                        + '; font-style: ' + font.styleName() \
                        + '; font-weight: ' + str(font.weight()) \
                        + ' }' )
                        
    
    