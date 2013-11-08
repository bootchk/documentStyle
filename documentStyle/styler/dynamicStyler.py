'''
Copyright 2013 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''
from copy import deepcopy

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QDialog

from .styler import Styler
from ..styleSheet.documentElementStyleSheet import DocumentElementStyleSheet
from documentStyle.formation.formation import Formation
from documentStyle.userInterface.styleDialog.styleDialog import EditableStyleSheetDialog

from documentStyle.debugDecorator import report


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
    ''' Do cascade yielding a Formation. '''
    return self._styleSheet.getFormation(self.selector)
  
  def styleSheet(self):
    ''' Don't cascade. '''
    return self._styleSheet
    
    
  @report
  def styleDocElementFromStyling(self, styling):
    '''
    See docstring at super.
    '''
    assert isinstance(styling, Formation)
    assert styling.isTouched()  # was edited
    targetStylingActSet = self._styleSheet.stylingActSetCollection.getMatchingOrNewStylingActSet(styling.selector)
    # targetStylingActSet refers to styling acts on the owning DocumentElement of this Styler
    #print("targetSASC", targetStylingActSet)
    styling.reflectToStylingActSet(targetStylingActSet)
  
  @report
  def styleDocElementFromStyleSheet(self, sourceStylesheet):
    '''
    Copy styling acts from stylesheet to self's stylesheet.
    '''
    assert isinstance(sourceStylesheet, DocumentElementStyleSheet)
    # For now, SAS doesn't know its selector, so pass self.selector
    targetStylingActSet = self._styleSheet.stylingActSet(self.selector)
    # targetStylingActSet refers to styling acts on the owning DocumentElement of this Styler
    for each in sourceStylesheet.generateStylingActs(self.selector):
      # each is an original, not a copy from source
      targetStylingActSet.put(deepcopy(each))
    #print("out targetSASC", targetStylingActSet)
  
  
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