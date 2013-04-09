'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PySide.QtGui import QPushButton, QDialog # QLabel
from userInterface.resettable import Resettable

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
  - API for a "control" (has setValue(), and value() methods)
  - emit valueChanged signal
  
  !!! A QLabel: does not have visual cues to let user know can be clicked.
  Behaves like a button, without the visual cues that a GUI standard requires.
  '''


  def __init__(self, text, styleType, subDialogMethod, resettableValue ):
    '''
    Text may be blank char. 
    In subclasses: 
    Could be "Color", but <style> being set may be only the background color.
    Then the text could disappear into the background.
    Could be "Text", and <style> being set is font.
    '''
    QPushButton.__init__(self, text)  # Must be init before Resettable
    Resettable.__init__(self, resettableValue)
    
    self.styleType = styleType  # <style> being controlled e.g. QColor
    self.subDialogMethod = subDialogMethod  # method of some framework dialog that returns a value of <style> e.g. QColorDialog
    
    #self.setValue(initialValue)
    
    self.setAutoFillBackground(True)   # Needed to ensure background color change effective ??
    self.clicked.connect(self.handleClicked) # Any other handlers for Signal clicked will also be called.
  
  
  def handleClicked(self):
    self._chooseNewValue()
    
    
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

  ''' Subclasses must implement valueChanged Signal,  deferred. '''
  
  
  def _chooseNewValue(self):
    ''' 
    Invoke subDialog for choosing <style>.  
    Parent in self's StyleDialog.
    '''
    myDialog = self.parentWidget()
    assert isinstance(myDialog, QDialog)
    newValue = self.subDialogMethod(parent=myDialog)
    # TODO if no real change in value?
    
    self.setValue(newValue)
    
    
  def setValue(self):
    '''
    Change appearance of widget to reflect value
    AND remember the value (for as long as widget exists.)
    '''
    raise NotImplementedError  # deferred
  
  
  def value(self):
    # !!! attribute MUST have different name from method value(), otherwise Python gives preference to attribute
    return self._value

  