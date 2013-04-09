'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

import copy

# Accesses QCoreApplication for global widgets and global stylesheet
from PySide.QtCore import QCoreApplication
from PySide.QtGui import QDialog

from selector import DETypeSelector
from userInterface.styleDialog.styleDialog import StyleDialog
from styleSheet.documentElementStyleSheet import DocumentElementStyleSheet




class Styler(object):
  '''
  Styles a DocumentElement.
  
  Responsibiliies:
  - get/set a Formation that can be applied to a DocumentElement
  
  Subclasses:  Two designs for styling:
  - TemplateStyler: each DocumentElement has-a Formation, no cascading (but the Formation is created by AppStyleSheet)
  - DynamicStyler: each DocumentElement has-a StyleSheet (which returns a Formation) and StyleSheets cascade.

  Abstract.
  '''
  pass

  

'''
TODO not working.  Symptom: copied QPen is deleted.
Probably need to implement __deepcopy__ on all classes.
Note also that Qt uses shared objects that are "detached" on change: might need to touch objects such as the default QPen
so that they become unshared.
'''

class TemplateStyler(object):
  '''
  Template kind of Formation:
  when created it snapshots the state of the DocumentStyleSheet.
  Subsequent user editing of DocumentStyleSheet does NOT change (cascade) to existing DocumentElements
  '''
  def __init__(self, selector):
    # !!! Copy, a snapshot.  Not updated by subsequent changes to DocumentStyleSheet
    self._formation = copy.deepcopy(self._selectFormationFromDocumentStyleSheet(selector))
    
    
  def _selectFormationFromDocumentStyleSheet(self, selector):
    ''' 
    Get Formation (that initially styles a DocumentElement) by selecting from DocumentElement's StyleSheet.
    
    Subsequently, changes to the DocumentElement's StyleSheet are then used to style DocumentElement.
    TODO
    '''
    # !!! DocumentElement gets Formation from document's stylesheet
    formation = QCoreApplication.instance().docStyleSheet.getFormation(selector)
    return formation
  
  def formation(self):
    return self._formation
    
  def setFormation(self, newFormation):
    self._formation = newFormation
    
    

class DynamicStyler(object):
  '''
  Dynamic: cascades.
  User editing of DocumentStyleSheet does change set of DocumentElements that have not been individually styled
  but changes the inverse set.
  '''
  def __init__(self, selector):
    self._styleSheet = DocumentElementStyleSheet()
    self.selector = selector
  
  def formation(self):
    return self._styleSheet.getFormation(self.selector)
    
  def setFormation(self, newFormation):
    '''
    Reflect newFormation into new SAS
    '''
    target = self._styleSheet.stylingActSetCollection.getOrNew(newFormation.selector())
    newFormation.reflectToStylingActSet(target)
                                                  


class Styleable(object):
  '''
  Behavior of DocumentElements: let user edit style using a context (RMB) Dialog.
  Mixin.
  
  No __init__: since mixin, let init pass up MRO.
  '''
  
  def setStylingDocumentElementType(self, DEType):
    " Styler depends on document element type."
    # Choose one.  Defines the broad behaviour of app.  Need Factory?
    self.styler = DynamicStyler(DETypeSelector(DEType))
    #self.styler = TemplateStyler(self.selector)
    
  
    
  def contextMenuEvent(self, event):
    ''' 
    Handler for Qt event.
    
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
    ''' On StyleSheet changed, renew style Formation and apply it to self. '''
    # print "Polish ", self.selector
    self.styler.formation().applyTo(self)


  