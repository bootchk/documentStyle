'''
Copyright 2013 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''
import copy

from PySide.QtCore import QCoreApplication

from .styler import Styler


'''
TODO TemplateStyler not working.  Symptom: copied QPen is deleted.
Probably need to implement __deepcopy__ on all classes.
Note also that Qt uses shared objects that are "detached" on change: might need to touch objects such as the default QPen
so that they become unshared.
'''

class TemplateStyler(Styler):
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
