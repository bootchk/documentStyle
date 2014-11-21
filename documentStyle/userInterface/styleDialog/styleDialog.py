'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PyQt5.QtWidgets import QDialogButtonBox

from documentStyle.userInterface.styleDialog.styleDialogWidget import StyleSheetDialogWidget
from documentStyle.userInterface.styleDialog.styleDialogQML import StyleSheetDialogQML
  

'''
let user edit StyleSheet (which may be style of DocumentElement)

Abstract Base Class API:
buttonBox()
isEditable()
open()

Two subclasses: editable and noneditable.
The Editable one has accept/reject buttons.  Noneditable can only be closed.

When implemented by inheriting from QWidget QDialog, open() and signals accepted and rejected are inherited.
''' 
  
'''
Choice of implementation: QML or QWidget.
'''
class EditableStyleSheetDialog(StyleSheetDialogQML): 
#class EditableStyleSheetDialog(StyleSheetDialogWidget):
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

  def connectSignals(self, acceptSlot, cancelSlot):
    self.accepted.connect(acceptSlot)
    self.rejected.connect(cancelSlot)


class NoneditableStyleSheetDialog(StyleSheetDialogWidget):
  
  def buttonBox(self):
    return None

  def isEditable(self):
    return False
  
  def connectSignals(self, acceptSlot, cancelSlot):
    pass