'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

# Accesses QCoreApplication for global widgets and global stylesheet
from PySide.QtCore import QCoreApplication
from PySide.QtGui import QDialog

from styler import DynamicStyler
from selector import DETypeSelector
from userInterface.styleDialog.styleDialog import StyleDialog
                                                  


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
  

  def editStyle(self):
    ''' 
    Let user edit style of DocumentElement. 
    '''
    editedFormation = self.styler.formation()
    '''
    Parent to app's activeWindow.
    FUTURE, if a document element is its own window, parent to it?
    Or position the dialog closer to the document element.
    '''
    styleDialog = StyleDialog(parentWindow=QCoreApplication.instance().activeWindow(), formation=editedFormation)
    styleDialog.exec_()
    if styleDialog.result() == QDialog.Accepted:
      editedFormation.applyTo(self)
    self.styler.setFormation(editedFormation)


  def polish(self):
    '''
    Apply style to DocumentElement.
    
    E.G. called on StyleSheet changed. 
    Renews style Formation via cascading and applies. 
    '''
    # print "Polish ", self.selector
    self.styler.formation().applyTo(self)


  