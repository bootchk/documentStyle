'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QWidget, QScrollArea, QLabel
from PyQt5.QtWidgets import QDialogButtonBox

import documentStyle.config as config



class StyleSheetDialogWidget(QDialog):
  '''
  QWidget GUI form of StyleSheetDialog
  
  Smart: configures itself according to a passed Formation.
  
  Only changes the passed Formation, which subsequently should used:
  - be applyTo'd DocumentElement (if DocumentElement has a Formation)
  - OR made part of a StyleSheet (if DocumentElement has a StyleSheet, more sophisticated cascading)
  
  Abstract, uses Template pattern: subclasses specialize substeps of algorithm i.e. adding buttons and enabling
  '''


  def __init__(self, parentWindow, formation, titleParts, flags=Qt.Dialog, ):
    
    # TODO, parentWindow should be the document, which may not be the activeWindow?
    # parentWindow = QCoreApplication.instance().activeWindow()
    super(StyleSheetDialogWidget, self).__init__(parent=parentWindow, flags=flags)
    
    # Layout components
    dialogLayout = QVBoxLayout()
    
    if sys.platform.startswith('darwin'):
      # GUI sheet has no title bar
      dialogLayout.addWidget(QLabel(self._composeTitle(titleParts)))
    else:
      self.setWindowTitle(self._composeTitle(titleParts))
      
    dialogLayout.addWidget(self.createDialogCenterWidget(formation))
    
    buttonBox = self.buttonBox()
    if buttonBox is not None:
      dialogLayout.addWidget(buttonBox)
      
    self.setLayout(dialogLayout)
    
    self.setDisabled(not self.isEditable())
    self.setSizeGripEnabled(True)
    
    '''
    Assert contents of dialog is set, and dialog sizepolicy defaults to expanding?
    For user friendliness, horizontal scroll bar not visible,
    and vertical scroll bar not visible unless necessary.
    
    The contents is scrolling and determines the final dialog size.
    The contents (QScrollArea) must be statically sized to fit the screen,
    or dynamically sized.
    These are not sufficient:
    ## self.adjustSize()
    ## self.setMinimumSize( 320, 400 )
    '''
    
  """
  def apply(self):
    # TODO check each value for change
    # If changed, create a StylingAct in StyleSheet
    self.emit(SIGNAL("changed"))
  """
  
  def _composeTitle(self, titleTuple):
    '''
    Translate and compose title string from tuple of parts.
    '''
    # assert parts are strings
    assert isinstance(titleTuple, tuple), 'titleParts is a tuple'
    #print titleTuple[0], titleTuple[1]
    return config.i18ns.styleTranslate(titleTuple[0]) + " " + config.i18ns.styleTranslate(titleTuple[1])
  
  
  def createDialogCenterWidget(self, formation):
    '''
    Scrolling list of editor widgets for editing StyleProperty.
    List comprises labels, and labeled editing widgets.
    But labels are indented as a tree.
    
    Canonical way: nest widget, layout, scrollarea
    '''
    formationLayout = formation.getLayout(top=True)
    viewport = QWidget()
    viewport.setLayout(formationLayout)
    
    # A hack so scroll bars not obscure buttons?
    # !!! left, top, right, bottom (not top, left... as usual.)
    viewport.setContentsMargins(10, 10, 10, 10)
    
    scrollArea = QScrollArea()
    scrollArea.setWidget(viewport)
    
    '''
    Assert width of contents is less than screen width (even mobile screens.)
    Can't assert height of contents less than screen height,
    e.g. a stylesheet has large height that must be vertically scrolled.
    Note this is statically determined, at design time,
    by ensuring that all rows are narrow.
    TODO dynamically enable horizontal and vertical scroll bar policy
    by calculations based on screen size and size of dialog needs?
    
    At one time, this not work: it obscured contents.
    Before I shortened many labels and model names???
    '''
    scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    return scrollArea
  
  
  def connectSignals(self, acceptSlot, cancelSlot):
    '''
    Effect deferred method.
    
    Self is-a QDialog.
    Connect QDialog's signals to given slots.
    '''
    self.accepted.connect(acceptSlot)
    self.rejected.connect(cancelSlot)
    
    
  def converseAppModal(self):
    '''
    Show:
    - Synchronous for some implementations (QWidget) (call doesn't return)
    - app modal (no other app windows take user input)
    - position in center in parent
    '''
    self.exec_()
    #print("After exec_")
    
    
    
class EditableStyleSheetDialogWidget(StyleSheetDialogWidget):
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
  
  
class NoneditableStyleSheetDialogWidget(StyleSheetDialogWidget):
  
  def buttonBox(self):
    return None

  def isEditable(self):
    return False
  
  def connectSignals(self, acceptSlot, cancelSlot):
    pass
    