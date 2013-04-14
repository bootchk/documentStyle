'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

import copy

# Accesses QCoreApplication for global widgets and global stylesheet
from PySide.QtCore import QCoreApplication
from PySide.QtGui import QDialog

from documentStyle.styler import DynamicStyler
from documentStyle.selector import DETypeSelector
from documentStyle.userInterface.styleDialog.styleDialog import StyleDialog
                                                  


class Styleable(object):
  '''
  Behavior of DocumentElements.
  Mixin.
  
  Responsibilities:
  - create a styler
  - let user edit style using Dialog (for example on a context menu event for right mouse button.) 
  - polish: apply style
  
  
  No __init__: since mixin, let init pass up MRO.
  However, must initialize with a call to setStylingDocumentElementType()
  
  ADT algebra, i.e. API
  
  1. Exceptional case
  setStyle()-> raises exception, must be preceded by setStylingDocumentElementType()
  
  2. Idempotent case (document element is Styleable, but not styled by user.)
  draw()-> succeeds, (where draw() is a framework method) an element can be drawn without any styling (framework supplies default look)
  
  3. Exceptional case
  polish()-> raises exception, must be preceded by setStylingDocumentElementType()
  
  4. Common case, user edits style of document element
  setStylingDocumentElementType()
  foo = editStyle(self)
  if foo is not None:
    applyStyle(foo)
  getStyle() -> returns None (if user canceled) or foo, and visual style equivalent to foo
  
  
  5.  Common case, user edits stylesheet
  setStylingDocumentElementType()
  'user change style sheet'
  polish() -> every document element matching style sheet change has visual style equivalent to stylesheet
  except for document elements which user has styled (inline)
  
  6.  Explanatory case
  setStylingDocumentElementType()
  getStyle()-> returns a style equivalent to the default of the framework (since document element not styled by user.)
  
  7.  Undo case
  setStylingDocumentElementType()
  bar = getStyle(): returns current style
  foo = editStyle(self)
  if foo is not None:
    applyStyle(foo)
  setStyle(bar) -> visual style of document element restored to style prior to user edit of style
  TODO not working
  
  8. Undo past stylesheet change case
  setStylingDocumentElementType()
  bar = getStyle(): returns current style
  foo = editStyle(self)
  if foo is not None:
    applyStyle(foo)
  'user change style sheet'
  setStyle(bar) -> visual style of document element restored to style prior to user edit of style AND stylesheet
  '''
  
  def setStylingDocumentElementType(self, DEType):
    '''
    Initialize with a styler.
    Styler depends on document element type.
    A DocumentElement has style (lower case, not Style) but no Styler UNTIL user acts to style it.
    In other words, this can be done just before editStyle(), or earlier when DocumentElement is created.
    '''
    # Choose Dynamic or Template.  Defines the broad behaviour of app.  Need Factory?
    self.styler = DynamicStyler(DETypeSelector(DEType))
    #self.styler = TemplateStyler(self.selector)
  
    
  def contextMenuEvent2(self, event):
    ''' 
    Handler for Qt event.
    This for the demo, a real app might not use this.
    
    Let user style with RMB (context button). 
    '''
    newStyle = self.editStyle()
    if newStyle is None:
      return # canceled
    else:
      self.applyStyle(newStyle)
  
  
  def contextMenuEvent(self, event):
    ''' 
    Test handler for Qt event.
    Let user style with RMB (context button), but if cancels, revert document element to original.
    '''
    try:
      if self.oldStyle is None:
        pass
    except AttributeError:
      print ">>>capturing original Style"
      self.oldStyle = self.getSerializableStyle()
    
    newStyle = self.editStyle()
    if newStyle is None:
      # TEST
      print ">>>Restoring oldStyle"
      self.setStyleFromSerializable(self.oldStyle)
      self.styler.formation().applyTo(self)
      
      return # canceled
    else:
      self.applyStyle(newStyle)
  
  
  def setStyle(self, style):
    '''
    Set style of DocumentElement.  
    Hides implementation of Style (e.g. as a Formation derived by cascading.)
    !!! Styler (certain subclasses) may convert Formation into StylingActs on StyleSheet.
    !!! Does not apply style (i.e. send it to GraphicsFramework.
    '''
    self.styler.setFormation(style)
  """
  
  def getStyle(self):
    '''
    Get style of DocumentElement, as known by DocumentStyle subsystem.
    DocumentElements draw having a style defaulted by and cached by the GraphicsFramework,
    but that is not the same as a Style.
    '''
    return copy.deepcopy(self.styler.formation())
  """
  
  def getSerializableStyle(self):
    '''
    Object instance that is serializable e.g. via pickling.
    And suitable as parameter to setStyleFromSerializable.
    
    Object is StylingActSetCollection, but don't rely on that; that fact should remain hidden.
    '''
    result = copy.deepcopy(self.styler._styleSheet.stylingActSetCollection)
    print "Count get styling acts", len(result)
    return result
  
  
  def setStyleFromSerializable(self, serializableStyle):
    '''
    Set style of DocumentElement from an object instance that was returned by getSerializableStyle
    
    !!! The instance will be copied so that user's subsequent style changes do NOT affect the passed instance.
    '''
    print "Count set styling acts", len(serializableStyle)
    self.styler.replaceStylingActSetCollection(serializableStyle)
    
    
  def applyStyle(self, style):
    " Apply given style (to model, then from model to view.)"
    self.setStyle(style)
    self.styler.formation().applyTo(self)
    ##self.getStyle().applyTo(self)
    
  
  def editStyle(self):
    ''' 
    Let user edit style of DocumentElement.
    Return Style, or None if canceled.
    !!! Does not apply Style to DocumentElement
    '''
    ##editableCopyOfStyle = self.getStyle()
    editableCopyOfStyle = self.styler.formation()
    '''
    Parent to app's activeWindow.
    FUTURE, if a document element is its own window, parent to it?
    Or position the dialog closer to the document element.
    '''
    styleDialog = StyleDialog(parentWindow=QCoreApplication.instance().activeWindow(), formation=editableCopyOfStyle)
    styleDialog.exec_()
    if styleDialog.result() == QDialog.Accepted:
      return editableCopyOfStyle
    else:
      return None


  def polish(self):
    '''
    Apply style to DocumentElement.
    
    E.G. called on StyleSheet changed. 
    Renews style Formation via cascading and applies. 
    '''
    # print "Polish ", self.selector
    ## self.getStyle().applyTo(self)
    self.styler.formation().applyTo(self)


  