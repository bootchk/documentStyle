'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PySide.QtGui import QDialog, QDialogButtonBox, QVBoxLayout


class StyleDialog(QDialog):
  '''
  Let user edit style of DocumentElement.
  
  Smart: configures itself according to a passed Formation.
  
  Only changes the passed Formation, which subsequently should used:
  - be applyTo'd DocumentElement (if DocumentElement haa a Formation)
  - OR made part of a StyleSheet (if DocumentElement has a StyleSheet, more sophisticated cascading)
  '''


  def __init__(self, parent, formation):
    super(StyleDialog, self).__init__(parent)
    
    # Create component widgets
    formationLayout = formation.display()
    buttonBox = QDialogButtonBox(QDialogButtonBox.Ok
                                 | QDialogButtonBox.Cancel)
    
    # Layout components
    dialogLayout = QVBoxLayout()
    dialogLayout.addItem(formationLayout)
    dialogLayout.addWidget(buttonBox)
    self.setLayout(dialogLayout)
    

    #buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.apply)
    buttonBox.accepted.connect(self.accept)
    buttonBox.rejected.connect(self.reject)
    
    self.setWindowTitle(formation.name + " Style")
    
    
  """
  def apply(self):
    # TODO check each value for change
    # If changed, create a StylingAct in StyleSheet
    self.emit(SIGNAL("changed"))
  """