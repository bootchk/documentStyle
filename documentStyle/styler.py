'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

import copy

# Accesses QCoreApplication for global widgets and global stylesheet
from PySide.QtCore import QCoreApplication

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
  def formation(self):
    raise NotImplementedError, "Deferred"
    
  def setFormation(self, newFormation):
    raise NotImplementedError, "Deferred"

  

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
    target = self._styleSheet.stylingActSetCollection.getOrNew(newFormation.selector)
    newFormation.reflectToStylingActSet(target)
                             
  
  " Delegate serialization to my stylesheet"
                                 
  def getSerializable(self):
    return self._styleSheet.getSerializable()
  
  def resetFromSerializable(self, serializableStyle):
    '''
    Reset to an earlier state.
    
    !!! Assert parameter will be copied so user's subsequent changes do not alter the caller's instance of serializableStyle.
    '''
    self._styleSheet.resetFromSerializable(serializableStyle)
                                          

  