'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PySide.QtCore import QCoreApplication
from PySide.QtGui import QDialog, QVBoxLayout


class NoneditableStyleSheetDialog(QDialog):
  '''
  Let user view (not change) style.
  Used for AppStyleSheet, not editable.
  
  Does not change the passed Formation.
  
  Only window Close, no OK button.
  '''


  def __init__(self, formation):
    parentWindow = parentWindow = QCoreApplication.instance().activeWindow()
    super(NoneditableStyleSheetDialog, self).__init__(parentWindow)
    
    # Create component widgets
    formationLayout = formation.display()
    
    # Layout components
    layout = QVBoxLayout()
    layout.addItem(formationLayout)
    self.setLayout(layout)
    
    self.setWindowTitle(formation.name)
    
    self.setDisabled(True)
    