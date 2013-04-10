'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

# Accesses QCoreApplication for global widgets and global stylesheet
from PySide.QtCore import QCoreApplication
from PySide.QtGui import QDialog

from documentStyle.styler import DynamicStyler
from documentStyle.selector import DETypeSelector
from documentStyle.userInterface.styleDialog.styleDialog import StyleDialog
from documentStyle.formation.formation import Formation
                                                  


class Styleable(object):
  '''
  Behavior of DocumentElements.
  Mixin.
  
  Responsibilities:
  - let user edit style using Dialog (for example on a context menu event for right mouse button.) 
  - polish: apply style
  
  
  No __init__: since mixin, let init pass up MRO.
  However, must initialize with a call to setStylingDocumentElementType()
  '''
  
  def setStylingDocumentElementType(self, DEType):
    '''
    Initialize with a styler.
    Styler depends on document element type.
    '''
    # Choose one.  Defines the broad behaviour of app.  Need Factory?
    self.styler = DynamicStyler(DETypeSelector(DEType))
    #self.styler = TemplateStyler(self.selector)
  
    
  def contextMenuEvent(self, event):
    ''' 
    Handler for Qt event.
    This for the demo, a real app might not use this.
    
    Let user style with RMB (context button). 
    '''
    self.editStyle()
  
  
  def setStyle(self, style):
    "Set style of DocumentElement.  Hides implementation of Style as a Formation"
    #assert isinstance(style, Formation), str(type(style))
    self.styler.setFormation(style)
  
  
  def getStyle(self):
    "Get style of DocumentElement.  "
    return self.styler.formation()
  
  
  def editStyle(self):
    ''' 
    Let user edit style of DocumentElement.
    If not canceled, apply style and return True.
    Return False if canceled.
    '''
    editableCopyOfStyle = self.getStyle()
    '''
    Parent to app's activeWindow.
    FUTURE, if a document element is its own window, parent to it?
    Or position the dialog closer to the document element.
    '''
    styleDialog = StyleDialog(parentWindow=QCoreApplication.instance().activeWindow(), formation=editableCopyOfStyle)
    styleDialog.exec_()
    if styleDialog.result() == QDialog.Accepted:
      editableCopyOfStyle.applyTo(self)
      self.setStyle(editableCopyOfStyle)
      return True
    else:
      return False


  def polish(self):
    '''
    Apply style to DocumentElement.
    
    E.G. called on StyleSheet changed. 
    Renews style Formation via cascading and applies. 
    '''
    # print "Polish ", self.selector
    self.getStyle().applyTo(self)


  