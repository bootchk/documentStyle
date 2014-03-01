'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QFont
from documentStyle.userInterface.resettableControls.resettable import Resettable
import documentStyle.config as config

'''
Setting color via pallette is not reliable on all platforms, for some widgets.
(Since some platforms use pixmaps to draw some widgets, not colors.)
Requires widget stylesheet.
'''


class StylePicker(Resettable, QPushButton):
  '''
  Control widget.
  Whose visible <style> is chosen by user in a Q<style>Dialog
  
  Responsibility:
  - let user pick a <style> (using further, standard dialog) via mouse click on widget
  - display <style> (as a swatch)
  - API for a 'control' (has setValue(), and value() methods)
  - emit valueChanged signal
  
  !!! A QLabel: does not have visual cues to let user know can be clicked.
  Behaves like a button, without the visual cues that a GUI standard requires.
  '''

  ''' Subclasses must implement, and emit valueChanged Signal,  deferred. '''
  

  def __init__(self, text, styleType, subDialog, resettableValue ):
    '''
    Text may be blank char. 
    In subclasses: 
    Could be 'Color', but <style> being set may be only the background color.
    Then the text could disappear into the background.
    Could be 'Text', and <style> being set is font.
    '''
    QPushButton.__init__(self, config.i18ns.styleTranslate(text))  # Must be init before Resettable
    Resettable.__init__(self, resettableValue)
    
    '''
    type of styleType may actually be pyqtWrapperType, although conceptually it is QFont or QColor
    assert isinstance(styleType, QFont), str(type(styleType))
    '''
    self.styleType = styleType  # <style> being controlled e.g. QColor
    '''
    subDialog is typically static method of some framework dialog class, e.g. QFontDialog
    Or a method that adapts a framework dialog, e.g. QColorDialog, which returns a QColor that not isValid() if canceled.
    It must have API:
    -callable with parameter 'initialValue'
    -return a tuple: (ok, value of <style>) 
    '''
    self.subDialog = subDialog  
    
    self._value = None  # !!! no default value.  !!! See below, this is the Widget's value
    
    self.setAutoFillBackground(True)   # Ensure widget background color change effective ??
    self.clicked.connect(self.handleClicked) # Any other handlers for Signal clicked will also be called.
  
  
  def handleClicked(self):
    ok, value = self._chooseNewValue()
    if not ok:  # user canceled
      return
    '''
    If user did not cancel, but chose same style as before, we still set value:
    this is use case where user is in-lining to stabilize color to same as cascaded color.
    '''
    self.setWrappedValue(value)  # Setting widget value, which propagates to StyleProperty
    
    
  """
  If inherit from QLabel:
  
  def mouseReleaseEvent(self, event):
    '''
    Redefine: set visible <style> of widget.
    In lieu of "clicked" signal
    '''
    
    # Call AFTER setting <style> insures correct state visual feedback (button down and up? but it is not a QButton)
    # QLabel doesn't need this anyway, it is superfluous unless ancestor is QButton?
    super(StylePicker, self).mouseReleaseEvent(event)
    self._chooseNewValue()
  """

  
  
  
  def _chooseNewValue(self):
    ''' 
    Invoke subDialog for choosing <style>.  
    Parent in self's StyleDialog.
    parentWidget is not QDialog if self is nested inside a QScrollArea:
    CANNOT assert isinstance(parentWidget, QDialog)
    '''
    return self.subDialog(parent=self.parentWidget(), # parent to StyleDialog (parent of StylePicker)
                          initialValue=self._value)

    
  
  def setWrappedValue(self, value):
    '''
    Set value after wrapping given value to a type that is pickleable.
    Default: no actual wrapping.
    Some subclasses reimplement.
    '''
    assert isinstance(value, self.styleType) # e.g. QColor, QFont
    self.setValue(value)
    
    
  '''
  getter/setter of widget value.
  !!! These are not for resettableValue, which has methods of same name
  '''
    
  def setValue(self, value):
    '''
    Change appearance of widget to reflect value
    AND remember the value (for as long as widget exists.)
    '''
    raise NotImplementedError  # deferred
  
  
  def value(self):
    # !!! attribute MUST have different name from method value(), otherwise Python gives preference to attribute
    return self._value

  