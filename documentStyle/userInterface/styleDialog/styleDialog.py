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
class StyleDialog(StyleSheetDialogQML): 
#class StyleDialog(StyleSheetDialogWidget):
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
  " This is here so we can rename it to mean asynchronous window modal (not synchronous app modal) "
  def open(self):
    super().open()
  
  def converseAppModal(self):
    " Synchronous (doesn't return) and app modal (no other windows take user input and centered in parent) "
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