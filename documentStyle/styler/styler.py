'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from documentStyle.userInterface.styleDialog.styleDialog import EditableStyleSheetDialog


class Styler(object):
  '''
  Styles a DocumentElement or Tool (a Leaf of any cascade.)
  
  Responsibiliies:
  - get/set a Formation that can be applied to a DocumentElement or Tool.
  
  Subclasses:  Two designs for styling:
  - TemplateStyler: each DocumentElement has-a Formation, no cascading (but the Formation is created by AppStyleSheet)
  - DynamicStyler: each DocumentElement has-a StyleSheet (which returns a Formation) and StyleSheets cascade.

  Abstract.
  
  This has very similar API as a StyleSheet, but NOT is-a, has-a Stylesheet.
  The main difference is what happens after edit():
  - StyleSheet emits stylesheetChanged
  - Styler returns a Formation that a caller applies
  '''
  def formation(self):
    raise NotImplementedError("Deferred")
    
  def styleLeafFromFormation(self, editedFormation):
    ''' 
    Style leaf (DocumentElement or Tool) that owns this styler with the given editedFormation.
    (Template styling.)
    '''
    raise NotImplementedError("Deferred")
  
  def styleLeafFromStyleSheet(self, styleSheet):
    ''' 
    Style leaf (DocumentElement or Tool) that owns this styler with the given stylesheet.
    (Dynamic, cascaded styling.)
    '''
    raise NotImplementedError("Deferred")

  def addToStyleCascade(self):
    raise NotImplementedError("Deferred")


  '''
  '''
  
  #OLD def getEditedStyle(self, parentWindow, titleParts):
  # TODO really should be Leaf, also edits style of Tool
  def editStyleOfDocElement(self, parentWindow, titleParts, docElement):
    ''' 
    Let user edit style held by styler.
    If not canceled, apply Style to DocumentElement
    '''
    self._editedDocElement = docElement
    self.createGui(parentWindow, titleParts)
    self.dialog.converseAppModal() 
    '''
    Some implementations of EditableStyleSheetDialog (the QML implementation)
    do not stop event loop (e.g. for app modal dialog)
    so always use signals to continue with result.
    We can't assume dialog result exists here.
    '''
  
  def accept(self):
    " Subclasses must implement (DynamicStyler and ToolStyler)"
    raise NotImplementedError("Deferred")
  
  
  def cancel(self):
    self._editedDocElement = None
    
    
  def createGui(self, parentWindow, titleParts):
    '''
    Compare to IntermediateStyleSheet.
    '''
    self.editedFormation = self.formation()   # New copy
    assert self.editedFormation is not None
    '''
    Parent to app's activeWindow.
    FUTURE, if a document element is its own window, parent to it?
    Or position the dialog closer to the document element.
    '''
    self.dialog = EditableStyleSheetDialog(parentWindow = parentWindow,
                                      formation=self.editedFormation, 
                                      titleParts = titleParts)
                                      # WAS flags=Qt.Sheet)
                                      # but that is not needed if open() which is window modal
    self.dialog.connectSignals(acceptSlot=self.accept, 
                               cancelSlot=self.cancel)