'''
Copyright 2013 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''
from copy import deepcopy

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QDialog

from .styler import Styler
from documentStyle.styleSheet.intermediateStyleSheet import IntermediateStyleSheet
from documentStyle.styleSheet.documentElementStyleSheet import DocumentElementStyleSheet
from documentStyle.formation.formation import Formation
from documentStyle.userInterface.styleDialog.styleDialog import EditableStyleSheetDialog

from documentStyle.debugDecorator import report


class DynamicStyler(Styler):
  '''
  Dynamic: cascades.
  User editing of DocumentStyleSheet changes set of DocumentElements that have not been individually styled (in-lined.)
  
  Note this is pickleable since attributes are pickleable.
  !!! Assert a deserialized self does NOT have _styleSheet parented; must call addToStyleCascade()
  '''
  
  def __init__(self, selector):
    self._styleSheet = DocumentElementStyleSheet(name="DocElement")
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
    
    # For now, user might not have touched a styling (since OK button on dialog is never disabled.)
    # If not touched, just return.
    # TODO assert styling.isTouched() and fix dialog so it cannot be OK'd if not touched.
    if not styling.isTouched():
      return
    
    targetStylingActSet = self._styleSheet.stylingActSetCollection.getMatchingOrNewStylingActSet(styling.selector)
    # targetStylingActSet refers to styling acts on the owning DocumentElement of this Styler
    #print("targetSASC", targetStylingActSet)
    styling.reflectToStylingActSet(targetStylingActSet)
  
  @report
  def styleDocElementFromStyleSheet(self, sourceStylesheet):
    '''
    Copy styling acts from stylesheet to self's stylesheet.
    '''
    assert isinstance(sourceStylesheet, DocumentElementStyleSheet), str(type(sourceStylesheet))
    # For now, SAS doesn't know its selector, so pass self.selector
    targetStylingActSet = self._styleSheet.stylingActSet(self.selector)
    # targetStylingActSet refers to styling acts on the owning DocumentElement of this Styler
    for each in sourceStylesheet.generateStylingActs(self.selector):
      # each is an original, not a copy from source
      targetStylingActSet.put(deepcopy(each))
    #print("out targetSASC", targetStylingActSet)
  
  
  def addToStyleCascade(self):
    '''
    Restore deserialized self to cascade, and check invariants.
    When deserializing (in general, using pickle) unpickling does not call __init__.
    Specifically, DocumentElementStyleSheet.__init__ is not called, and thus setParent() is not called.
    '''
    self._styleSheet.setParent(QCoreApplication.instance().cascadion.docStyleSheet)
    assert isinstance(self._styleSheet, DocumentElementStyleSheet), 'self is correct class for terminal stylesheet'
    # TODO rename parent->parentStyleSheet since parent and parent() are commonly used.
    assert self._styleSheet.parent is not None, 'self is parented'
    # TODO, 'Doc' is hardcoded elsewhere, this should be a weaker assertion that parent is subclass IntermediateStyleSheet
    assert self._styleSheet.parent.name == 'Doc', 'parent is a DocumentStyleSheet'
  
  
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