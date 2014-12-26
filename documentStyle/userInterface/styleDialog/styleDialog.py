'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

# TODO remove: this module should not depend on QtWidgets
from PyQt5.QtWidgets import QDialogButtonBox

from documentStyle.userInterface.styleDialog.styleDialogWidget import StyleSheetDialogWidget
from documentStyle.qmlUI.styleDialogQML import StyleSheetDialogQML

'''
Choice of implementation: QML or QWidget.
Uncomment one, and see config.useQML
'''
#class StyleDialog(StyleSheetDialogQML): 
class StyleDialog(StyleSheetDialogWidget):
  '''
  let user edit StyleSheet (which may be style of DocumentElement)
  
  Adaptor (wrapper) around alternative implementations.
  When implemented by inheriting from QWidget QDialog, open() and signals accepted and rejected are inherited.
  
  Abstract Base Class API: (but it is not formally declared. TODO declare it and inherit.)
  buttonBox()
  isEditable()
  open()
  converseAppModal()
  connectSignals()
  
  Two subclasses: editable and noneditable.
  The Editable one has accept/reject buttons.  Noneditable can only be closed.
  
  '''
  
  '''
  Note there is no Qt method to show a dialog as a popup: under the cursor, but modal.
  print("here")
  self.move(0,0)  TODO to cursor
  self.show()
  '''
  
  def open(self):
    '''
    Show:
    - asynchronous (call returns immediately)
    - window modal (other app top windows may receive input, but not the parent window. I.E. transient.
    - position in center of parent or drawer from parent (depends on platform)
    '''
    super().open()
  
  def converseAppModal(self):
    '''
    Show:
    - Synchronous for some implementations (QWidget) (call doesn't return)
    - app modal (no other app windows take user input)
    - position in center in parent
    '''
    self.exec_()
    #print("After exec_")
  


class EditableStyleSheetDialog(StyleDialog):
  '''
  Editable has buttons and is enabled.
  '''
  
  def buttonBox(self):
    " buttonBox, with connected signals"
    buttonBox = QDialogButtonBox(QDialogButtonBox.Ok
                                 | QDialogButtonBox.Cancel)
    #buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.apply)
    buttonBox.accepted.connect(self.accept)
    buttonBox.rejected.connect(self.reject)
    return buttonBox

  def isEditable(self):
    return True


class NoneditableStyleSheetDialog(StyleDialog):
  
  def buttonBox(self):
    return None

  def isEditable(self):
    return False
  
  def connectSignals(self, acceptSlot, cancelSlot):
    pass