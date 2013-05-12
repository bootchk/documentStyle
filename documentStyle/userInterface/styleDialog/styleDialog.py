'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''
from PySide.QtCore import QCoreApplication, Qt
from PySide.QtGui import QDialog, QDialogButtonBox, QVBoxLayout, QWidget, QScrollArea


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
    
    # Layout components
    dialogLayout = QVBoxLayout()
    
    dialogLayout.addWidget(self.createDialogCenterWidget(formation))
    
    if self.hasButtons():
      dialogLayout.addWidget(self.buttonBox())
    self.setLayout(dialogLayout)
    
    self.setWindowTitle(title)  # formation.name + " Style")
    
    self.setDisabled(not self.isEditable())
    self.setSizeGripEnabled(True)
    
    ## This does not make the dialog have not horizontal scroll bar
    ## self.adjustSize()
    
    # TODO for user friendliness, size should be set so that horizontal scroll bar not visible,
    # and vertical scroll bar not visible unless necessary.
    
  """
  def apply(self):
    # TODO check each value for change
    # If changed, create a StylingAct in StyleSheet
    self.emit(SIGNAL("changed"))
  """
  
  
  def createDialogCenterWidget(self, formation):
    '''
    Scrolling list of editor widgets for editing StyleProperty.
    List comprises labels, and labeled editing widgets.
    But labels are indented as a tree.
    
    Canonical way: nest widget, layout, scrollarea
    '''
    formationLayout = formation.display(top=True)
    viewport = QWidget()
    viewport.setLayout(formationLayout)
    
    # A hack so scroll bars not obscure buttons.
    # TODO Size dialog so horiz scroll bar not necessary, and not obscure
    # !!! left, top, right, bottom (not top, left... as usual.)
    viewport.setContentsMargins(10, 10, 20, 10)
    
    scrollArea = QScrollArea()
    scrollArea.setWidget(viewport)
    ## This does not work: it obscures contents
    ## scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    return scrollArea
    
  
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