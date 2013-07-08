'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PySide.QtCore import Signal
from PySide.QtGui import QFontDialog, QFont

from stylePickerWidget import StylePicker

from documentStyle.styleWrapper.fontStyleWrapper import FontStyleWrapper



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
    result = fontTuple[0]
    assert isinstance(result, QFont)
    return result
  
  
  def _chooseNewValue(self):
    '''
    Reimplement to wrap.
    
    Invoke subDialog for choosing <style>.  
    Parent in self's StyleDialog.
    '''
    myDialog = self.parentWidget()
    newValue = self.subDialogMethod(parent=myDialog)
    assert isinstance(newValue, QFont)

    """
    Not relevant: whether exactMatch or not, sometimes italic-light does not display?
    if not newValue.exactMatch():
      print "Not an exact match"
    """
    # TODO if no real change in value?
    
    self.setValue(FontStyleWrapper(newValue)) # wrap
  
  
  def setValue(self, newValue):
    '''
    Set widget <style>: font
    AND set widget local attribute.
    
    !!! Note use of wrapped versus unwrapped value.
    '''
    assert isinstance(newValue, FontStyleWrapper) # Not: QFont
    newQFont = newValue.getWrappedValue()
    self._feedbackFont(newQFont)
    self._value = newValue
    self.valueChanged.emit(newQFont)  # Propagate, e.g. to model
  
  
  
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
                        
    
    