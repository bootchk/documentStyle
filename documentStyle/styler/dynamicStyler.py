'''
Copyright 2013 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''
from PySide.QtCore import QCoreApplication
from PySide.QtGui import QDialog

from .styler import Styler
from ..styleSheet.documentElementStyleSheet import DocumentElementStyleSheet
from documentStyle.userInterface.styleDialog.styleDialog import EditableStyleSheetDialog


class DynamicStyler(Styler):
  '''
  Dynamic: cascades.
  User editing of DocumentStyleSheet changes set of DocumentElements that have not been individually styled.
  
  Note this is pickleable since attributes are pickleable.
  !!! Assert a deserialized self does NOT have _styleSheet parented; must call addToStyleCascade()
  '''
  
  def __init__(self, selector):
    self._styleSheet = DocumentElementStyleSheet()
    self.selector = selector
    # ensure self is in style cascade (DESS() ensures it.)
  
  
  def formation(self):
    return self._styleSheet.getFormation(self.selector)
  
    
  def setFormation(self, newFormation):
    '''
    Reflect newFormation into new SAS
    '''
    target = self._styleSheet.stylingActSetCollection.getOrNew(newFormation.selector)
    newFormation.reflectToStylingActSet(target)
  
  
  def addToStyleCascade(self):
    '''
    Restore invariants.
    
    A quirk is that serializing starts at IntermediateStyleSheet.
    On deserializing, DocumentElementStyleSheet.__init__ is not called, and thus setParent() is not called.
    Call setParent() now.
    
    TODO a better way?
    '''
    self._styleSheet.setParent(QCoreApplication.instance().cascadion.docStyleSheet)
  
  
  def getEditedStyle(self, dialogTitle):
    ''' 
    Let user edit style held by styler.
    Return Style, or None if canceled.
    !!! Does not apply Style to DocumentElement
    '''
    editableCopyOfStyle = self.formation()
    '''
    Parent to app's activeWindow.
    FUTURE, if a document element is its own window, parent to it?
    Or position the dialog closer to the document element.
    '''
    styleDialog = EditableStyleSheetDialog(formation=editableCopyOfStyle, title=dialogTitle)
    styleDialog.exec_()
    if styleDialog.result() == QDialog.Accepted:
      return editableCopyOfStyle
    else:
      return None
    
    
  """
  OLD
  " Delegate serialization to my stylesheet"
                                 
  def getSerializable(self):
    return self._styleSheet.getSerializable()
  
  def resetFromSerializable(self, serializableStyle):
    '''
    Reset to an earlier state.
    
    !!! Assert parameter will be copied so user's subsequent changes do not alter the caller's instance of serializableStyle.
    '''
    self._styleSheet.resetFromSerializable(serializableStyle)
  """