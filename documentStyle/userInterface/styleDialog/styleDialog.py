'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''
from PySide.QtCore import QCoreApplication
from PySide.QtGui import QDialog, QDialogButtonBox, QVBoxLayout


class StyleSheetDialog(QDialog):
  '''
  Let user edit StyleSheet (which may be style of DocumentElement)
  
  Smart: configures itself according to a passed Formation.
  
  Only changes the passed Formation, which subsequently should used:
  - be applyTo'd DocumentElement (if DocumentElement has a Formation)
  - OR made part of a StyleSheet (if DocumentElement has a StyleSheet, more sophisticated cascading)
  
  Abstract, uses Template pattern: subclasses specialize substeps of algorithm i.e. adding buttons and enabling
  '''


  def __init__(self, formation, title):
    
    # TODO, parentWindow should be the document, which may not be the activeWindow?
    parentWindow = QCoreApplication.instance().activeWindow()
    super(StyleSheetDialog, self).__init__(parentWindow)
    
    # Create component widgets for formation
    formationDisplay = formation.display(top=True)
    
    # Layout components
    dialogLayout = QVBoxLayout()
    formationDisplay.addTo(dialogLayout) # inversion: tell formationDisplay to add itself to layout
    if self.hasButtons():
      dialogLayout.addWidget(self.buttonBox())
    self.setLayout(dialogLayout)
    
    self.setWindowTitle(title)  # formation.name + " Style")
    
    self.setDisabled(not self.isEditable())
    
  """
  def apply(self):
    # TODO check each value for change
    # If changed, create a StylingAct in StyleSheet
    self.emit(SIGNAL("changed"))
  """
  
  
class EditableStyleSheetDialog(StyleSheetDialog):
  '''
  Editable has buttons and is enabled.
  '''
    
  def hasButtons(self):
    return True
  
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



class NoneditableStyleSheetDialog(StyleSheetDialog):
  
  def hasButtons(self):
    return False

  def isEditable(self):
    return False